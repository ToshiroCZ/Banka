import json
import logging
import os


class ConfigManager:
    def __init__(self, config_file):
        # Pokud config file není absolutní cesta, pokusíme se ji hledat relativně
        if not os.path.isabs(config_file):
            base_path = os.path.dirname(os.path.abspath(__file__))
            config_file = os.path.join(base_path, "..", config_file)
        self.config_file = config_file

    def load_config(self):
        try:
            with open(self.config_file, "r", encoding="utf-8") as f:
                config = json.load(f)
                logging.info("Konfigurační soubor načten.")
                return config
        except Exception as e:
            logging.error(f"Chyba při načítání konfiguračního souboru: {e}")
            return {}
