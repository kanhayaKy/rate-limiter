from rate_limiter.algorithms import (
    SlidingWindowCounterAlgorithm,
    TokenBucketAlgorithm,
    FixedWindowCounter,
    SlidingWindowLogAlgorithm,
)


valid_algorithm_map = {
    "sliding_window_counter": SlidingWindowCounterAlgorithm,
    "token_bucket": TokenBucketAlgorithm,
    "fixed_window_counter": FixedWindowCounter,
    "sliding_window_log": SlidingWindowLogAlgorithm,
}


def get_algorithm_from_name(algorithm_name):
    if algorithm_name.lower() not in valid_algorithm_map:
        print("ERR: Invalid algorithm name provided, falling back to default")
        algorithm_name = "sliding_window_counter"

    return valid_algorithm_map[algorithm_name]()
