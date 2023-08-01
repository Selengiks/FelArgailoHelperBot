from sys import stdout
from loguru import logger


async def start(mode: str):
    """Apply custom loguru settings"""
    logger.remove()
    logger.add("logs/log_{time}.log", rotation="1 day", level=mode)

    logger.add(
        stdout,
        colorize=True,
        format="<green>{time:DD.MM.YY H:mm:ss}</green> "
        "| <yellow><b>{level}</b></yellow> | <magenta>{file}</magenta> | <cyan>{"
        "message}</cyan>",
        level=mode,
    )

    logger.debug("Logger configs updated")
