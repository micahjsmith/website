import json
import os

from pelican import logger, signals
from pelican.utils import pelican_open

def generator_init(generator):
    logger.debug('my plugin called')
    if 'data' not in generator.env.globals:
        generator.env.globals['data'] = {}
    else:
        logger.debug(repr(generator.env.globals['data']))
        #raise RuntimeError

    # load data files into global context
    files = generator.get_files(
        generator.settings['DATA_PATHS'], extensions=False)
    logger.debug('files: {files!r}'.format(files=files))
    for f in files:
        root, file = os.path.split(f)
        name, ext = os.path.splitext(file)
        if ext == '.json':
            with pelican_open(os.path.join(generator.path, f)) as text:
                data = json.loads(text)

            generator.env.globals['data'][name] = data
            logger.debug('Loaded json data from {name}'.format(name=name))
        else:
            logger.debug('Skipped non-json file {file}'.format(file=file))

def register():
    signals.generator_init.connect(generator_init)
