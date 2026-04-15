class Job:
    def __init__(
        self,
        id: int|None,
        type: str,
        payload: str,
        status: str,
        attempts: int,
        max_attempts: int = 5
    ):
        self.id = id
        self.type = type
        self.payload = payload
        self.status = status
        self.attempts = attempts
        self.max_attempts = max_attempts