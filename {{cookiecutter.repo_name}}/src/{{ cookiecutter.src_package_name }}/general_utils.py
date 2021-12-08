import logging
import logging.config
import yaml


def setup_logging(logging_config_path="./conf/base/logging.yml",
                  default_level=logging.INFO):
    """Set up configuration for logging utilities.

    Parameters
    ----------
    logging_config_path : str, optional
        Path to YAML file containing configuration for Python logger,
        by default "./config/logging_config.yaml"
    default_level : logging object, optional, by default logging.INFO
    """
    logger = logging.getLogger(__name__)

    try:
        with open(logging_config_path, 'rt') as file:
            log_config = yaml.safe_load(file.read())
        logging.config.dictConfig(log_config)

    except Exception as e:
        logging.basicConfig(
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            level=default_level)
        logger.info(e)
        logger.info(
            'Logging config file is not found. Basic config is being used.')
