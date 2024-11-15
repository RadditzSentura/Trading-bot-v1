import logging
import sys
from src.config_loader import ConfigLoader
from src.advanced_grid_trading_bot import AdvancedGridTradingBot

def setup_logging(log_config: dict):
    log_level = getattr(logging, log_config.get('level', 'INFO').upper(), logging.INFO)
    log_file = log_config.get('file', 'logs/bot.log')

    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(sys.stdout)
        ]
    )
    logging.info("Logging is set up.")

def main():
    # Load configurations
    config_loader = ConfigLoader()
    config = config_loader.config

    # Setup logging
    setup_logging(config.get('logging', {}))

    # Initialize and run the bot
    try:
        bot = AdvancedGridTradingBot(config)
        bot.run()
    except Exception as e:
        logging.error(f"Failed to start the bot: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()