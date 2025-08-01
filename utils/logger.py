# utils/logger.py

import logging

def configure_logger(name: str = "prompt_manager", level: int = logging.INFO) -> logging.Logger:
    """
    Erstellt und konfiguriert einen Logger mit Konsolenausgabe.

    :param name: Name des Loggers (meist Modulname)
    :param level: Logging-Level (z. B. logging.INFO)
    :return: Konfigurierter Logger
    """
    logger = logging.getLogger(name)
    if not logger.handlers:  # Mehrfache Konfiguration vermeiden
        logger.setLevel(level)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('[%(asctime)s] %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger



