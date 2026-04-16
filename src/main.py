import typer
from worker import Worker
from queue import Queue
from jobs import job_registry
from failure_policy import FailurePolicy

app = typer.Typer()


w = Worker(Queue(), job_registry, FailurePolicy())


@app.command()
def enqueue(type: str, payload: str, max_attempts: int = 3):
    w.enqueue(type, payload, max_attempts)

@app.command()
def worker_run_once():
    w.run_once()

@app.command()
def worker():
    w.run_forever()

if __name__ == "__main__":
    app()