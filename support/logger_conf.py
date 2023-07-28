from sys import stdout
from loguru import logger


async def start(debug: bool):
    """Apply custom loguru settings"""
    logger.remove()
    logger.add(
        "logs/log_{time}.log", rotation="1 day", level="DEBUG" if debug else "INFO"
    )

    logger.add(
        stdout,
        colorize=True,
        format="<green>{time:DD.MM.YY H:mm:ss}</green> "
        "| <yellow><b>{level}</b></yellow> | <magenta>{file}</magenta> | <cyan>{"
        "message}</cyan>",
        level="DEBUG" if debug else "INFO",
    )

    logger.debug("Logger configs updated")
