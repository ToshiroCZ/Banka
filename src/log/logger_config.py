import logging
import sys


def setup_logger(log_filename='bank.log', log_level=logging.INFO):
    """
    Nastaví logování pro celou aplikaci. Logy se budou zapisovat jak do souboru,
    tak na konzoli ve formátu:
    YYYY-MM-DD HH:MM:SS,mmm - LEVEL - Message

    :param log_filename: Název souboru pro logování (default 'bank.log').
    :param log_level: Log úroveň, např. logging.INFO (default INFO).
    :return: Root logger.
    """
    # Získáme root logger
    logger = logging.getLogger()
    logger.setLevel(log_level)

    # Vytvoříme formatter podle požadovaného formátu
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    # File handler: logování do souboru
    file_handler = logging.FileHandler(log_filename, mode='a')
    file_handler.setLevel(log_level)
    file_handler.setFormatter(formatter)

    # Console handler: logování na konzoli (stdout)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)

    # Vyčistíme případné existující handlery, aby se zprávy neduplikovaly
    if logger.hasHandlers():
        logger.handlers.clear()

    # Přidáme oba handlery
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

# Pokud chcete, aby se logger okamžitě nastavil při importu, můžete odkomentovat následující řádek:
# setup_logger()
