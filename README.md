Py-ProjectMill
==============

Python port of https://github.com/mapbox/projectmill

Currently only support `--mill` and `--render`.

The only Python requirement so far are is `testify` (for running tests).
To run tests, first `pip install -r requirements.txt` and then just run `testify tests`.

The remainder of the documentation is adapted from the original project.

- - -

Need to generate a bunch of TileMill projects that are nearly identical and
then render them all out? What to script that? We gotcha covered.

Usage: `projectmill <command> [options]`

Example: `projectmill --mill -c config.example.json -t ../tilemill/`

## Installation

Install with `pip install -e .` or `python setup.py install`.
If you're using Python 2.7, there are no dependencies unless you want to run the tests.
If you're using Python 2.6, you will need to `pip install -r requirements-2.6.txt` (2.6 doesn't include `argparse`, which is required).

Not yet tested with 2.5 or 3.x.

## Configuration

Configuration is expected as a json file which contains an array as the root
object. See `config.example.json` for an example. Each element in the array
should be an object which can have the following keys:

`source`        REQUIRED The source project, generally the name of folder it
                lives in.

`destination`   REQUIRED The destination project name.

`mml`           A json snippet which will be merged on top of the project's mml
                file. To clear out an option set it to 'null'

`cartoVars`     A json object containing key value pairs which can be use to
                override variables in in carto stylesheets.

`MBmeta`        MBTiles: A json object containing key value pairs which will be added to
                a rendered MBtiles export.

Additionally, the following options will be passed to TileMill's export commnd

`format`        Export format (png|pdf|svg|mbtiles). (Default: undefined)

`bbox`          Array containing coordinates of bounding box to export. (Default: undefined)

`minzoom`       MBTiles: minimum zoom level to export. (Default: undefined)

`maxzoom`       MBTiles: maximum zoom level to export. (Default: undefined)

`width`         Image: image width in pixels. (Default: 400)

`height`        Image: image height in pixels. (Default: 400)

`bufferSize`    Mapnik render buffer size. (Default: 128)


## Commands

ProjectMill accepts the following commands. They can be issued either
individually or together.

`--mill`      Generates new tilemill projects based on configuration.

`--render`    Renders projects that are present in configuration and have been milled.

`--upload`    Uploads projects that are present in configuration and have been rendered.


## Options

-t      Path to the TileMill install

-c      specify a configuration file. (Defaults: `./config.json`)

-p      Path to TileMill project folder. (Defaults: `~/Documents/Mapbox`)

-f      Replace existing projects (together with `mill`) or existing projects and exports (together with `render`).
