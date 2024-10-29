"""
Configuration handler for the Be My Reply Guy application.
This file is responsible for reading and parsing the YAML configuration file.
"""

import yaml
import logging
from pprint import pformat
from utils.logger import Logger

logger = Logger().get_logger(__name__)

def load_config(config_path='config/config.yaml'):
    try:
        with open(config_path, 'r') as config_file:
            config = yaml.safe_load(config_file)
        
        # Log the loaded configuration
        logger.info("Configuration loaded successfully:")
        logger.info("\n" + pformat(config))
        
        return config
    except FileNotFoundError:
        logger.error(f"Configuration file not found at {config_path}")
        return None
    except yaml.YAMLError as e:
        logger.error(f"Error parsing YAML configuration: {e}")
        return None
