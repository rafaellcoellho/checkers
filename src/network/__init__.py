import logging

log_format = logging.Formatter(
    '%(levelname)s -> [%(asctime)s][%(module)s:%(filename)s]: %(message)s',
    datefmt='%d/%m/%Y %H:%M'
)

log_handler = logging.StreamHandler()
log_handler.setLevel(logging.INFO)
log_handler.setFormatter(log_format)

logger = logging.getLogger(__name__)
logger.addHandler(log_handler)
logger.setLevel(logging.INFO)
