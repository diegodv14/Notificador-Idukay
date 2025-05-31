import logging
import colorlog

def setup_logger():
    console_handler = colorlog.StreamHandler()
    console_handler.setFormatter(colorlog.ColoredFormatter(
        '%(log_color)s%(asctime)s - %(levelname)s - %(message)s',
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'bold_red',
        }
    ))

    file_handler = logging.FileHandler("mi_log.log")
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

    logger = colorlog.getLogger("mi_logger")
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    logger.setLevel(logging.DEBUG)

    return logger

logger = setup_logger()
