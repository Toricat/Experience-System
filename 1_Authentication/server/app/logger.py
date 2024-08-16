import logging
import yaml
import os
from logging.config import dictConfig
from datetime import datetime

log_filename = datetime.now().strftime("logs_%d_%m_%Y.log")

yaml_file =  './app/log_config.yml'

with open(yaml_file, 'r') as f:
    config = yaml.safe_load(f)

for handler in config['handlers'].values():
    if 'filename' in handler:
        handler['filename'] = os.path.join("app/logs", log_filename)

dictConfig(config)
logger = logging.getLogger(__name__)
