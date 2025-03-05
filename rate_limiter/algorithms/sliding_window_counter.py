from collections import defaultdict
from time import time

from .base import RateLimitingAlgorithm

from rate_limiter.exceptions import RateLimitExceeded

from threading import Timer, Lock

"""
It is a hybrid approach that combines the low processing cost of the fixed window algorithm, and the improved boundary conditions of the sliding log algorithm.

    Like the fixed window algorithm, we maintain a counter for each fixed window. But we will need to store the current and the previous windows counts.
    We use a weighted count of the current and previous windows counts to determine the count for the sliding window. This helps smooth out the impact of burst of traffic. For example, if the current window is 40% through, then we weight the previous window’s count by 60% and add that to the current window count.

"""


class SlidingWindowCounterAlgorithm(RateLimitingAlgorithm):
    def __init__(self, window=10, limit=10):
        super().__init__()

        self.window = window
        self.window_limit = limit

        self.current_window_start = None
        self.current_window_tokens = defaultdict(int)
        self.previous_window_tokens = defaultdict(int)

        self.lock = Lock()

        self.reset_window()

    def should_process(self, request_user):
        with self.lock:
            current_window_token_count = self.current_window_tokens[request_user]
            previous_window_token_count = self.previous_window_tokens[request_user]

            current_time = time()
            elapsed_time = (current_time - self.current_window_start) / self.window

            effective_current_window_token = current_window_token_count * elapsed_time
            effective_previous_window_token = previous_window_token_count * (
                1 - elapsed_time
            )

            combined_window_token = (
                effective_current_window_token + effective_previous_window_token
            )

            print(combined_window_token, "################")
            if combined_window_token >= self.window_limit:
                raise RateLimitExceeded

            self.current_window_tokens[request_user] += 1

    def reset_window(self):
        with self.lock:
            self.current_window_start = time()
            self.previous_window_tokens = self.current_window_tokens
            self.current_window_tokens.clear()

        timer = Timer(self.window, self.reset_window, args=())
        timer.daemon = True
        timer.start()
