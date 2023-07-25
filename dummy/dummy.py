import logging
from typing import Any

from fastapi import Body, FastAPI
from fastapi.staticfiles import StaticFiles

logger = logging.getLogger()
app = FastAPI()

app.mount("/media", StaticFiles(directory="/var/media"), name="media")


@app.post("/")
def webhook(body: dict[str, Any] = Body(...)) -> None:
    logger.error(f"Dummy webhook request received:\n{body}")
