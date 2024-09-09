import logging
import yaml
import os
from logging.config import dictConfig
from datetime import datetime

# Load cấu hình logger từ YAML
def setup_logger():
    log_filename = datetime.now().strftime("logs_%d_%m_%Y.log")
    yaml_file = './app/utils/log_config.yml'

    # Load cấu hình từ file YAML
    with open(yaml_file, 'r') as f:
        config = yaml.safe_load(f)

    # Cập nhật tên file log trong cấu hình
    for handler in config['handlers'].values():
        if 'filename' in handler:
            handler['filename'] = os.path.join("app/logs", log_filename)

    # Áp dụng cấu hình logger từ YAML
    dictConfig(config)

# Khởi tạo logger
setup_logger()
logger = logging.getLogger('app_logger')
