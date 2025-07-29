import logging
from time import time
from functools import wraps

logging.basicConfig(
    filename="app.log",
    format="%(asctime)s | %(levelname)s | %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def log_execution_time(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start = time()
        result = await func(*args, **kwargs)
        end = time()
        duration = round((end - start) * 1000, 2)
        logger.info(f"{func.__name__} executed in {duration} ms")
        return {"Execution Time": f"{duration} ms", "data": result}
    return wrapper
