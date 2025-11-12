import logging
import sys

logger = logging.getLogger("my-logger")
print("Default logging format:")
logger.error("Default to warning?")
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s"
)
logger.info("level changed to info")

from pythonjsonlogger.json import JsonFormatter

print("\nCustom logging format:")
log_handler = logging.StreamHandler(sys.stdout)
formatter = JsonFormatter(
    fmt="%(asctime)s %(levelname)s %(name)s %(message)s",
    rename_fields={"levelname": "severity", "asctime": "timestamp"},
)
log_handler.setFormatter(formatter)

# Now I have 2 handlers, one with default format and one with custom format
logger.addHandler(log_handler)

logger.info(dict(foo="bar"))

try:
    1 / 0
except ZeroDivisionError:
    logger.exception(dict(foo="bar"))


logger.info("Done")
