# -*- coding: utf-8 -*-

import copy
import json
import logging
import os
import re
import shutil
import types

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
log = logging.getLogger('projectmill')

MSS_VAR_RE = re.compile('^@([\w-]+):([\W]?[^;]+);$')


def dict_merge(merge_left, merge_right):
    """Recursively merge two dicts, returning a new dict as the result.

    The base of the merge is `merge_left`, and the values to merge in are taken
    recursively from `merge_right`. Both inputs are left unmodified by the
    process, and the result is a new dictionary.

    """
    if not isinstance(merge_right, dict):
        return merge_right

    result = copy.deepcopy(merge_left)
    for k, v in merge_right.iteritems():
        if k in result and isinstance(result[k], dict):
            result[k] = dict_merge(result[k], v)
        else:
            result[k] = copy.deepcopy(v)
    return result


def process_mml(sourcefile, config):
    """Merge base + custom configurations"""
    source_dict = dict()
    with open(sourcefile) as f:
        source_dict = json.loads(f.read())

    assert isinstance(source_dict, types.DictType), (
        "Base of config merges must be a dictionary: %s" % str(source_dict)
    )

    assert 'mml' in config

    return json.dumps(dict_merge(source_dict, config.get('mml')), indent=2)


def process_mss(sourcefile, config):
    """Read the MSS file line by line & substitute out variables from config"""
    with open(sourcefile) as f:
        in_lines = f.read().decode('utf8').splitlines()

    subs = config.get('cartoVars')

    out_lines = []
    for line in in_lines:
        match = MSS_VAR_RE.search(line)
        if match:
            var_name, orig_value = match.groups()
            if var_name in subs:
                line = '@%s: %s;' % (var_name, subs.get(var_name, orig_value))

        out_lines.append(line)

    return '\n'.join(out_lines)


def mill(dest, config):
    for fname in os.listdir(config.get('source')):
        try:
            destfile = os.path.join(config.get('destination'), fname)
            destdir = os.path.dirname(destfile)
            sourcefile = os.path.join(config.get('source'), fname)

            if not os.path.exists(destdir):
                os.mkdir(destdir)

            if os.path.islink(sourcefile):
                # Symlinks are just reproduced
                os.symlink(os.path.realpath(sourcefile), destfile)
            elif 'mml' in config and fname == 'project.mml':
                # project.mml files are recursively merged with config before
                # copying
                with open(destfile, 'wb') as f:
                    f.write(process_mml(sourcefile, config))
            elif 'cartoVars' in config and fname.endswith('.mss'):
                # map stylesheets have variables substituted from config before
                # copying
                with open(destfile, 'wb') as f:
                    f.write(process_mss(sourcefile, config))
            else:
                # everything else, we just copy as-is
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
