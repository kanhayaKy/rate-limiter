import pytest
from time import sleep, time
from collections import deque

from rate_limiter.algorithms import SlidingWindowLogAlgorithm
from rate_limiter.exceptions import RateLimitExceeded


def test_sliding_window_log__happy_path():
    algorithm = SlidingWindowLogAlgorithm(window=1, limit=2)

    assert algorithm.should_process("user_1")
    assert algorithm.should_process("user_1")

    assert len(algorithm.window_log.get("user_1")) == 2

    with pytest.raises(RateLimitExceeded):
        algorithm.should_process("user_1")

    sleep(1.1)
    assert algorithm.should_process("user_1")


# def test_sliding_window_log__token_added():
#     algorithm = SlidingWindowLogAlgorithm(window=1, limit=2)

#     current_time = time()
#     algorithm.window_log["user_token_add_1"] = deque(
#         [current_time - 1, current_time, current_time-0.1]
#     )
#     algorithm.window_log["user_token_add_2"] = deque(
#         [
#             current_time - 0.5,
#             current_time,
#             current_time + 1.1,
#         ]
#     )

#     print(algorithm.window_log)
#     with pytest.raises(RateLimitExceeded):
#         algorithm.should_process("user_token_add_1")

#     sleep(1.1)
#     assert len(algorithm.window_log.get("user_token_add_1")) == 0
#     assert len(algorithm.window_log.get("user_token_add_2")) == 1
