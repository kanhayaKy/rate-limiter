from .base import RateLimitingAlgorithm

from rate_limiter.exceptions import RateLimitExceeded

from threading import Timer, Lock


"""
The token bucket algorithm works like this:

    There is a 'bucket' that has capacity for N tokens. Usually this is a bucket per user or IP address.
    Every time period a new token is added to the bucket, if the bucket is full the token is discarded.
    When a request arrives and the bucket contains tokens, the request is handled and a token is removed from the bucket.
    When a request arrives and the bucket is empty, the request is declined.

"""


class TokenBucketAlgorithm(RateLimitingAlgorithm):
    def __init__(self, capacity=10, interval=1, tokens=1):
        super().__init__()

        self.capacity = capacity
        self.interval = interval
        self.tokens = tokens

        # self.bucket = defaultdict(lambda: self.capacity)
        self.bucket = {}
        self.lock = Lock()

        self.add_token()

    def should_process(self, request_user):
        with self.lock:
            if not request_user in self.bucket:
                self.bucket[request_user] = self.capacity

            if self.bucket[request_user] <= 0:
                raise RateLimitExceeded

            self.bucket[request_user] -= 1
        return True

    def add_token(self):
        with self.lock:
            for key, value in self.bucket.items():
                self.bucket[key] = min(value + 1, self.capacity)

        timer = Timer(self.interval, self.add_token, args=())
        timer.daemon = True
        timer.start()
