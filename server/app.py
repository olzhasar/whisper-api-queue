from celery import Celery
from fastapi import FastAPI
from pydantic import BaseModel, HttpUrl

ASR_TASK_NAME = "run_asr"

celery_app = Celery()
app = FastAPI(title="Whisper API")


class PostData(BaseModel):
    file_url: HttpUrl
    webhook_url: HttpUrl


@app.post("/")
async def root(data: PostData):
    celery_app.send_task(ASR_TASK_NAME, kwargs=data.model_dump(mode="json"))
