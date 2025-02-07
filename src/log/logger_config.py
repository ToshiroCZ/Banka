import logging
import sys


def setup_logger(log_filename='bank.log', log_level=logging.INFO):
    """
    Nastaví logování pro celou aplikaci. Logy se budou zapisovat jak do souboru,
    tak na konzoli ve formátu:
    YYYY-MM-DD HH:MM:SS,mmm - LEVEL - Message
    """
    logger = logging.getLogger()
    logger.setLevel(log_level)

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    # File handler: logování do souboru s UTF-8 kódováním
    file_handler = logging.FileHandler(log_filename, mode='a', encoding='utf-8')
    file_handler.setLevel(log_level)
    file_handler.setFormatter(formatter)

    # Console handler: logování na konzoli (stdout)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)

    # Vyčistíme existující handlery, aby se zprávy neduplikovaly
    if logger.hasHandlers():
        logger.handlers.clear()

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
