class HistoryLock:
    def __init__(self):
        self.locked = False

    def acquire(self):
        while self.locked:
            pass
        self.locked = True

    def release(self):
        self.locked = False

    def __enter__(self):
        self.acquire()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release()

    