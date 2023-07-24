from celery_app import app
from exceptions import RetriableNetworkError
from services import download_audio, send_result_to_webhook
from transcribers import transcriber


@app.task(autoretry_for=(RetriableNetworkError,))
def run_asr(file_url: str, webhook_url: str) -> None:
    filename, content = download_audio(file_url)
    result = transcriber.run(filename=filename, content=content)
    send_asr_result.delay(result=result, url=webhook_url)


@app.task(autoretry_for=(RetriableNetworkError,))
def send_asr_result(result: dict[str, str], url: str) -> None:
    send_result_to_webhook(result, url)
