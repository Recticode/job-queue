import time

class Worker:
    def __init__(self, queue, job_registry, failure_policy):
        self.queue = queue
        self.jobs = job_registry
        self.policy = failure_policy

    def enqueue(self, type: str, payload: str, max_attempts: int = 3):
        self.queue.enqueue(type, payload, max_attempts)

    def run_once(self):
        job = self.queue.dequeue()

        if not job:
            print("no jobs available")
            return None

        self.queue.mark_running(job)

        try:
            if self.policy.should_fail(job.type, job.attempts):
                raise Exception("simulated failure")

            handler = self.jobs.get(job.type)
            if not handler:
                print("unknown job type:", job.type)
                self.queue.handle_failure(job)
                return False

            handler(job.payload)

            self.queue.mark_done(job)
            return True

        except Exception as e:
            print("job failed:", e)
            self.queue.handle_failure(job)
            return False

    def run_forever(self):
        while True:
            job = self.queue.dequeue()

            if not job:
                time.sleep(1)
                print("no jobs available")
                continue

            self.queue.mark_running(job)

            try:
                if self.policy.should_fail(job.type, job.attempts):
                    raise Exception("simulated failure")

                handler = self.jobs.get(job.type)
                if not handler:
                    print("unknown job type:", job.type)
                    self.queue.handle_failure(job)
                    continue

                handler(job.payload)
                self.queue.mark_done(job)

            except Exception as e:
                print("job failed:", e)
                self.queue.handle_failure(job)