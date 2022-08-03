from holofood.config import EnaConfig
from holofood.settings import *

UNIT_TESTING = True

HOLOFOOD_CONFIG = HolofoodConfig(
    _env_file=holofood_config_env,
    ena=EnaConfig(
        projects=["PRJTESTING"], systems={"8030": "salmon", "9031": "chicken"}
    ),
)
