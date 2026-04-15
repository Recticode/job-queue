import random

class FailurePolicy:
    def __init__(self):
        pass

    def should_fail(self, type, attempts):
        num = random.randint(1, 10)
        if num == 10:
            return True
        else:
            return False
