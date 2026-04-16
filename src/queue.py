from models import Job
from repository import Database

class Queue:
    def __init__(self):
        self.db = Database("app.db")

    def enqueue(self, type: str, payload: str, max_attempts: int = 3):
        job = Job(
            id=None,
            type=type,
            payload=payload,
            status="pending",
            attempts=0,
            max_attempts=max_attempts,
        )
        self.db.create_job(job)

    def dequeue(self):
        return self.db.get_next_pending()

    def mark_running(self, job: Job):
        self.db.increment_attempts(job.id)
        self.db.update_status(job.id, "running")

    def mark_done(self, job: Job):
        self.db.update_status(job.id, "done")

    def handle_failure(self, job: Job):
        updated_job = self.db.get_job(job.id)

        if updated_job.attempts >= updated_job.max_attempts:
            self.db.update_status(job.id, "failed")
        else:
            self.db.update_status(job.id, "pending")