import logging
from pascua import config

logging_log_level = getattr(logging, config.log_level)

logger = logging.getLogger('framework-logger')
logger.setLevel(logging_log_level)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging_log_level)

# create formatter
formatter = logging.Formatter('[%(asctime)s] [%(process)d] [%(levelname)s] %(message)s', '%Y-%m-%d %H:%M:%S %z')

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)

logger.info('Set logger level as "' + config.log_level + '"')
