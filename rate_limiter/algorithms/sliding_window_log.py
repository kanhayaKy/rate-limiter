from time import time
from collections import defaultdict, deque
from threading import Timer, Lock

from .base import RateLimitingAlgorithm
from rate_limiter.exceptions import RateLimitExceeded


"""
The sliding log algorithm involves:

    Tracking a time stamped log for each consumer request. These logs are usually stored in a hash set or table that is sorted by time.
    Logs with timestamps beyond a threshold are discarded.
    When a new request comes in, we calculate the sum of logs to determine the request rate.
    If the request when added to the log would exceed the threshold rate, then it is declined.

"""


class SlidingWindowLogAlgorithm(RateLimitingAlgorithm):
    def __init__(self, window=60, limit=10):
        super().__init__()

        self.window = window
        self.window_limit = limit

        self.window_log = defaultdict(deque)

        self.lock = Lock()

        self.remove_expired_logs()

    def should_process(self, request_user):
        with self.lock:
            current_time = time()
            user_tokens = 0

            for log in self.window_log[request_user]:
                if current_time - log < self.window:
                    user_tokens += 1

            if user_tokens >= self.window_limit:
                raise RateLimitExceeded

            self.window_log[request_user].append(current_time)

    def remove_expired_logs(self):
        with self.lock:
            current_time = time()
            for user, logs in self.window_log.items():
                while logs[0] - current_time >= self.window:
                    logs.popleft()

        timer = Timer(self.window, self.remove_expired_logs, args=())
        timer.daemon = True
        timer.start()
