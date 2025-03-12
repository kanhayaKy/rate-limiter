from time import time

from .base import RateLimitingAlgorithm

from rate_limiter.exceptions import RateLimitExceeded


"""
It is a hybrid approach that combines the low processing cost of the fixed window algorithm, and the improved boundary conditions of the sliding log algorithm.

    Like the fixed window algorithm, we maintain a counter for each fixed window. But we will need to store the current and the previous windows counts.
    We use a weighted count of the current and previous windows counts to determine the count for the sliding window. This helps smooth out the impact of burst of traffic. For example, if the current window is 40% through, then we weight the previous window’s count by 60% and add that to the current window count.

"""


class SlidingWindowCounterAlgorithm(RateLimitingAlgorithm):
    def __init__(self, store, window=10, limit=10):
        super().__init__()

        self.window = window
        self.window_limit = limit

        self.store = store

    def should_process(self, request_user):
        current_time = time()
        window_start = current_time // self.window

        current_window_key = f"rate_limit:{request_user}:{window_start}"
        previous_window_key = f"rate_limit:{request_user}:{window_start-1}"

        current_window_token_count = int(self.store.get(current_window_key) or 0)
        previous_window_token_count = int(self.store.get(previous_window_key) or 0)

        current_time = time()
        elapsed_time = min(1.0, ((window_start * (self.window)) / self.window))

        effective_current_window_token = current_window_token_count * elapsed_time
        effective_previous_window_token = previous_window_token_count * (
            1 - elapsed_time
        )

        combined_window_token = (
            effective_current_window_token + effective_previous_window_token
        )

        if combined_window_token >= self.window_limit:
            raise RateLimitExceeded

        self.store.incr(current_window_key)

        if current_window_token_count == 0:
            # Set expire only if new expiry is less than existing expiry
            self.store.expire(current_window_key, self.window * 2, lt=True)
