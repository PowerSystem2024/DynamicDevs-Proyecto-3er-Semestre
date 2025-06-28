import logging
from logging.handlers import RotatingFileHandler
import os


class AppLogger:
    def __init__(self):
        pass

    @staticmethod
    def setup_logger(logger_name: str, log_dir: str = "logs") -> logging.Logger:
        """Configura el sistema de logging con archivos separados

        Args:
            logger_name: Nombre identificador del logger (usado para el archivo)
            log_dir: Directorio donde se guardarán los logs (por defecto 'logs')

        Returns:
            Logger configurado
        """
        # Crear directorio si no existe
        os.makedirs(log_dir, exist_ok=True)

        logger = logging.getLogger(logger_name)

        # Evitar agregar handlers múltiples si el logger ya existe
        if logger.handlers:
            return logger

        logger.setLevel(logging.DEBUG)

        # Formato de los mensajes
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        # Handler para consola
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)

        # Handler para archivo (con rotación)
        log_file = os.path.join(log_dir, f"{logger_name}.log")
        file_handler = RotatingFileHandler(
            log_file,
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
