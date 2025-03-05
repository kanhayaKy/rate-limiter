from collections import defaultdict

from .base import RateLimitingAlgorithm

from rate_limiter.exceptions import RateLimitExceeded

from threading import Timer, Lock

"""
The fixed window counter algorithm works like this:

    A window size of N seconds is used to track the request rate. Each incoming request increments the counter for the window.
    If the counter exceeds a threshold, the request is discarded.
    The windows are typically defined by the floor of the current timestamp, so 17:47:13 with a 60 second window length, would be in the 17:47:00 window.

"""


class FixedWindowCounter(RateLimitingAlgorithm):
    def __init__(self, window=60, limit=10):
        super().__init__()

        self.window = window
        self.window_limit = limit

        self.current_window_tokens = defaultdict(int)

        self.lock = Lock()

        self.reset_window()

    def should_process(self, request_user):
        with self.lock:
            if self.current_window_tokens[request_user] >= self.window_limit:
                raise RateLimitExceeded

            self.current_window_tokens[request_user] += 1

    def reset_window(self):
        with self.lock:
            self.current_window_tokens.clear()

        timer = Timer(self.window, self.reset_window, args=())
        timer.daemon = True
        timer.start()
