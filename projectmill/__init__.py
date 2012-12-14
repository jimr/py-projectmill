# -*- coding: utf-8 -*-

"""
projectmill
~~~~~~~~

:copyright: (c) 2012 by James Rutherford
:license: ISC, see LICENSE for more details.

"""

__title__ = 'projectmill'
__version__ = '0.0.1'
__description__ = 'Python port of https://github.com/mapbox/projectmill'
__url__ = 'https://github.com/Maplecroft/py-projectmill'
__build__ = 0
__author__ = 'James Rutherford'
__license__ = 'ISC'
__copyright__ = 'Copyright 2012 James Rutherford'


import argparse
import json
import logging
import os
import shutil
import sys

from projectmill import utils

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
log = logging.getLogger('projectmill')


def main():
    parser = argparse.ArgumentParser(prog="projectmill")
    parser.add_argument("--mill", action="store_true")
    parser.add_argument("--render", action="store_true")
    parser.add_argument("--upload", action="store_true")
    parser.add_argument("-c", "--config", help="./config.json")
    parser.add_argument("-t", "--tilemill", help="/path/to/tilemill")
    parser.add_argument("-p", "--project_dir", help="Where to drop the output")
    parser.add_argument("-f", "--replace_existing", action="store_true")
    args = parser.parse_args()

    if not (args.mill or args.render or args.upload):
        print 'Missing command. One of --mill --render or --upload required.'
        parser.print_usage()
        sys.exit(1)

    project_dir = args.project_dir or os.path.join(
        os.environ.get('HOME'), 'Documents', 'MapBox',
    )
    tilemill_path = args.tilemill or '/usr/share/tilemill'
    replace_existing = args.replace_existing

    if not os.path.exists(tilemill_path):
        raise IOError("Can't find tilemill at %s" % tilemill_path)

    if not os.path.isfile(args.config):
        raise IOError("Can't find config at %s" % args.config)

    with open(args.config) as f:
        raw_config = json.loads(f.read())

    config = dict()
    for cfg in raw_config:
        assert 'source' in cfg and 'destination' in cfg, (
            "'source' and 'destination' attributes are required: %s" %
            str(cfg)
        )
        config[cfg.get('destination')] = cfg

        for path in ['source', 'destination']:
            cfg[path] = os.path.join(project_dir, 'projects', cfg.get(path))

    
    if args.mill:
        count = 0
        for k, v in config.items():
            count += 1
            dest = v.get('destination')
            if os.path.exists(dest) and replace_existing:
                shutil.rmtree(dest)

            if os.path.exists(dest):
                log.warn('Skipping project %s' % k)
            else:
                utils.mill(k, v)

            if count == 10:
                break


if __name__ == '__main__':
    main()
