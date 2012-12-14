# -*- coding: utf-8 -*-

import json
import logging
import os
import shutil

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
log = logging.getLogger('projectmill')


def process_mml(sourcefile, config):
    output = config.get('mml')
    with open(sourcefile) as f:
        output.update(json.loads(f.read()))
    return json.dumps(output, indent=2)


def process_mss(sourcefile, config):
    raise NotImplementedError()


def mill(dest, config):
    for fname in os.listdir(config.get('source')):
        try:
            destfile = os.path.join(config.get('destination'), fname)
            destdir = os.path.dirname(destfile)
            sourcefile = os.path.join(config.get('source'), fname)

            # In the future the 'mml' file will always be called 'project.mml',
            # but currently this isn't the case.
            # TODO delete this when https://github.com/mapbox/tilemill/pull/970
            # is merged.
            if fname.endswith('.mml') and fname != 'project.mml':
                destfile = os.path.join(
                    config.get('destination'), '%s.mml' % dest
                )

            if not os.path.exists(destdir):
                os.mkdir(destdir)

            if os.path.islink(sourcefile):
                os.symlink(os.path.realpath(sourcefile), destfile)
            elif 'mml' in config and fname.endswith('.mml'):
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
