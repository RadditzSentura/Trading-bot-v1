# src/config_loader.py

import yaml
import os
import logging
from dotenv import load_dotenv

class ConfigLoader:
    def __init__(self, config_path: str = "config/config.yml"):
        self.logger = logging.getLogger(__name__)
        self.config_path = config_path
        load_dotenv()  # Load .env file if present
        self.config = self.load_config()
        self.override_with_env()

    def load_config(self) -> dict:
        if not os.path.exists(self.config_path):
            self.logger.error(f"Configuration file {self.config_path} not found.")
            raise FileNotFoundError(f"Configuration file {self.config_path} not found.")

        try:
            with open(self.config_path, 'r') as file:
                config = yaml.safe_load(file)
                self.logger.info(f"Configuration loaded successfully from {self.config_path}.")
                return config
        except yaml.YAMLError as e:
            self.logger.error(f"Error parsing the configuration file: {e}")
            raise

    def override_with_env(self):
        # Override configuration with environment variables if they exist
        self.config['exchange']['api_key'] = os.getenv('EXCHANGE_API_KEY', self.config['exchange'].get('api_key'))
        self.config['exchange']['api_secret'] = os.getenv('EXCHANGE_API_SECRET', self.config['exchange'].get('api_secret'))
        self.logger.info("Configuration overridden with environment variables if present.")

    def get_exchange_config(self) -> dict:
        return self.config.get('exchange', {})

    def get_trading_config(self) -> dict:
        return self.config.get('trading', {})

    def get_logging_config(self) -> dict:
        return self.config.get('logging', {})

    def get_performance_config(self) -> dict:
        return self.config.get('performance', {})