from models import Job

import sqlite3
class Database:
    def __init__(self, file_name):
        self.file_name = file_name
        self.recreate_db()

    def recreate_db(self):
        try:
            conn = sqlite3.connect(self.file_name)

            conn.execute("""
                CREATE TABLE IF NOT EXISTS jobs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    type TEXT NOT NULL,
                    payload TEXT NOT NULL,
                
                    status TEXT NOT NULL CHECK (
                        status IN ('pending', 'running', 'done', 'failed')
                    ),
                
                    attempts INTEGER NOT NULL DEFAULT 0,
                    max_attempts INTEGER NOT NULL DEFAULT 3,
                
                    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
                );
            """)

            conn.commit()
        except Exception as e:
            print(e)
        finally:
            conn.close()

    def create_job(self, job: Job):
        try:
            conn = sqlite3.connect(self.file_name)

            conn.execute(f"""
                        INSERT INTO jobs(type, payload, status, max_attempts) VALUES (?, ?, ?, ?)
                        """,
                         (job.type, job.payload, job.status, job.max_attempts))

            conn.commit()
        except Exception as e:
            print(e)
        finally:
            conn.close()

    def get_next_pending(self):
        try:
            conn = sqlite3.connect(self.file_name)

            cursor = conn.execute("SELECT * FROM jobs WHERE status = ? ORDER BY updated_at ASC LIMIT 1",
                                  ("pending", ))

            row = cursor.fetchone()

            if not row:
                return None

            return Job(
                id=row[0],
                type=row[1],
                payload=row[2],
                status=row[3],
                attempts=row[4],
                max_attempts=row[5]
            )
        except Exception as e:
            print(e)
            return None
        finally:
            conn.close()

    def update_status(self, job_id, status):
        try:
            conn = sqlite3.connect(self.file_name)

            conn.execute("UPDATE jobs SET status = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
                         (status, job_id))

            conn.commit()
        except Exception as e:
            print(e)
        finally:
            conn.close()

    def increment_attempts(self, job_id):
        try:
            conn = sqlite3.connect(self.file_name)

            conn.execute("UPDATE jobs SET attempts = attempts + 1 WHERE id = ?",
                         (job_id, ))
            conn.commit()
        except Exception as e:
            print(e)
        finally:
            conn.close()

    def get_job(self, job_id):
        try:
            conn = sqlite3.connect(self.file_name)

            cursor = conn.execute("SELECT * FROM jobs WHERE id = ?",
                                  (job_id, ))

            row = cursor.fetchone()

            if not row:
                return None

            return Job(
                id=row[0],
                type=row[1],
                payload=row[2],
                status=row[3],
                attempts=row[4],
                max_attempts=row[5]
            )
        except Exception as e:
            print(e)

        finally:
            conn.close()