import pytest
from time import sleep

from rate_limiter.algorithms import TokenBucketAlgorithm
from rate_limiter.exceptions import RateLimitExceeded


def test_token_bucket__happy_path():
    algorithm = TokenBucketAlgorithm(capacity=1, interval=1)

    assert algorithm.should_process("user_1") is True

    with pytest.raises(RateLimitExceeded):
        algorithm.should_process("user_1")

    assert algorithm.should_process("user_2") is True

    sleep(1.1)

    assert algorithm.should_process("user_1") is True
