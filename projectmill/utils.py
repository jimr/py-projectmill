# -*- coding: utf-8 -*-

import copy
import json
import logging
import os
import shutil
import types

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
log = logging.getLogger('projectmill')


def dict_merge(merge_left, merge_right):
    """Recursively merge two dicts, returning a new dict as the result.

    The base of the merge is `merge_left`, and the values to merge in are taken
    recursively from `merge_right`. Both inputs are left unmodified by the
    process, and the result is a new dictionary.

    """
    if type(merge_left) != types.DictType:
        raise TypeError("merge_left must be a dictionary")

    if type(merge_right) != types.DictType:
        return merge_right

    result = copy.deepcopy(merge_left)
    for k, v in merge_right.iteritems():
        if k in result and type(result[k]) == types.DictType:
            result[k] = dict_merge(result[k], v)
        else:
            result[k] = copy.deepcopy(v)
    return result


def process_mml(sourcefile, config):
    """Merge base + custom configurations"""
    source_dict = dict()
    with open(sourcefile) as f:
        source_dict = json.loads(f.read())

    assert type(source_dict) == types.DictType, (
        "Base of config merges must be a dictionary: %s" % str(source_dict)
    )

    assert 'mml' in config

    return json.dumps(dict_merge(source_dict, config.get('mml')), indent=2)


def process_mss(sourcefile, config):
    raise NotImplementedError()


def mill(dest, config):
    for fname in os.listdir(config.get('source')):
        try:
            destfile = os.path.join(config.get('destination'), fname)
            destdir = os.path.dirname(destfile)
            sourcefile = os.path.join(config.get('source'), fname)

            if not os.path.exists(destdir):
                os.mkdir(destdir)

            if os.path.islink(sourcefile):
                os.symlink(os.path.realpath(sourcefile), destfile)
            elif 'mml' in config and fname == 'project.mml':
                with open(destfile, 'wb') as f:
                    f.write(process_mml(sourcefile, config))
            elif 'cartoVars' in config and fname.endswith('.mss'):
                with open(destfile, 'wb') as f:
                    f.write(process_mss(sourcefile, config))
            else:
                if os.path.isfile(sourcefile):
                    shutil.copy(sourcefile, destfile)
                else:
                    shutil.copytree(sourcefile, destfile)
            
            log.info('Created project: %s' % config.get('destination'))
        except Exception, ex:
            log.exception(
                'Error processing project: %s (%s)' %
                (config.get('destination'), ex)
            )
