#!/usr/bin/env python3
import logging
import logging.config

import yamlconf
from ores.score_processors import Celery

with open("ores.wmflabs.org.yaml") as f:
    config = yamlconf.load(f)

with open("logging_config.yaml") as f:
    logging_config = yamlconf.load(f)
    logging.config.dictConfig(logging_config)

if 'data_paths' in config['ores'] and \
    'nltk' in config['ores']['data_paths']:
    import nltk
    nltk.data.path.append(config['ores']['data_paths']['nltk'])

score_processor = Celery.from_config(config, config['ores']['score_processor'])
application = score_processor.application

if __name__ == '__main__':
    application.worker_main(argv=["celery_worker", "--loglevel=INFO"])
