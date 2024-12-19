import logging
#логгер в консоль
def setup_logger(log_file="app.log"):
    """Настраивает логгер."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger()

logger = setup_logger()

def log_event(event_message, level="info"):
    """Логирует событие."""
    if level == "info":
        logger.info(event_message)
    elif level == "error":
        logger.error(event_message)
    elif level == "warning":
        logger.warning(event_message)
