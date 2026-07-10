import logging
import sys

LOGGER_NAME = "retailfish"


def configure_logging() -> None:
    """
    Configure application logging.
    """

    logging.basicConfig(
        level=logging.INFO,
        format=(
            "%(asctime)s | "
            "%(levelname)-8s | "
            "%(name)s | "
            "%(message)s"
        ),
        handlers=[
            logging.StreamHandler(sys.stdout),
        ],
        force=True,
    )


configure_logging()

logger = logging.getLogger(LOGGER_NAME)

# from app.core.logger import logger
# logger.info("RetailFish backend started.")