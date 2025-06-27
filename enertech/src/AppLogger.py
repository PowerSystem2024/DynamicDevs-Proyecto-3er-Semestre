import logging
from logging.handlers import RotatingFileHandler


class AppLogger:
    def __init__(self):
        pass

    @staticmethod
    def setup_logger(logger_name: str) -> logging.Logger:
        """Configura el sistema de logging"""
        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.DEBUG)

        # Formato de los mensajes
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        # Handler para consola
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)

        # Handler para archivo (con rotación)
        file_handler = RotatingFileHandler(
            logger_name + '.log',
            maxBytes=1024 * 1024,  # 1MB
            backupCount=5,
            encoding='utf-8'
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)

        # Añadir handlers al logger
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

        return logger
