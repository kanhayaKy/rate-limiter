from .base import RateLimitingAlgorithm

from threading import Timer


class TokenBucketAlgorithm(RateLimitingAlgorithm):
    def __init__(self, capacity=10, interval=1, tokens=1):
        super().__init__()

        self.capacity = capacity
        self.interval = interval
        self.tokens = tokens

        # self.bucket = defaultdict(lambda: self.capacity)
        self.bucket = {}
        self.add_token()

    def should_process(self, request_user):
        if not request_user in self.bucket:
            self.bucket[request_user] = self.capacity

        if self.bucket[request_user] > 0:
            self.bucket[request_user] -= 1
            return True

        return False

    def add_token(self):
        for key, value in self.bucket.items():
            self.bucket[key] = min(value + 1, 10)

        Timer(self.interval, self.add_token, args=()).start()
