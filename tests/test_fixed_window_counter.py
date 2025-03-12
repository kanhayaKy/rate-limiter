import pytest
from time import sleep

from rate_limiter.algorithms import FixedWindowCounter
from rate_limiter.exceptions import RateLimitExceeded


def test_fixed_window_counter__happy_path():
    algorithm = FixedWindowCounter(window=1, limit=2)

    assert algorithm.should_process("user_1") is True
    assert algorithm.should_process("user_1") is True

    with pytest.raises(RateLimitExceeded):
        algorithm.should_process("user_1")

    assert algorithm.should_process("user_2") is True

    sleep(1.1)

    assert algorithm.should_process("user_1") is True


def test_fixed_window_counter__tokens_added():
    algorithm = FixedWindowCounter(window=1, limit=2)

    algorithm.current_window_tokens["user_token_added_1"] = 1
    algorithm.current_window_tokens["user_token_added_2"] = 2
    algorithm.current_window_tokens["user_token_added_3"] = 3

    assert algorithm.should_process("user_token_added_1")

    assert algorithm.current_window_tokens.get("user_token_added_1") is 2

    sleep(1.1)

    assert algorithm.current_window_tokens.get("user_token_added_1", 0) is 0
    assert algorithm.current_window_tokens.get("user_token_added_2", 0) is 0
    assert algorithm.current_window_tokens.get("user_token_added_3", 0) is 0
