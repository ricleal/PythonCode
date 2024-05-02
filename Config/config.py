from pyaml_env import parse_config, BaseConfig
import os
from pprint import pprint
import logging
from logging import Logger

def settings(logger: Logger) -> BaseConfig:
    env = os.getenv("ENV", "dev")
    logger.info("Loading settings for environment: " + env)  

    current_dir = os.path.dirname(os.path.realpath(__file__))

    config_common_path = os.path.join(current_dir, "common.yaml")
    config_common = parse_config(config_common_path)

    config_specific = parse_config(env + ".yaml")

    config_common.update(config_specific)
    base_config = BaseConfig(config_common)
    return base_config

log = logging.getLogger(__name__)
base_config = settings(log)

print("==>", base_config.cluster.name)
print("==>", base_config.cluster.host)
print("==>", base_config.database.name)
print("==>", base_config.database.url)
