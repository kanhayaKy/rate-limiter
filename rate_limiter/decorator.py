from functools import wraps
from flask import jsonify, request

from rate_limiter.algorithms import TokenBucketAlgorithm
from rate_limiter.exceptions import RateLimitExceeded


# algorithm = {"token_bucket": TokenBucketAlgorithm()}

selected_algorithm = TokenBucketAlgorithm()


def rate_limit():
    """Decorator to limit requests."""

    def decorator(f):
        def wrapper(*args, **kwargs):
            request_ip = request.remote_addr

            try:
                selected_algorithm.should_process(request_ip)
            except RateLimitExceeded:
                return jsonify({"error": "Too many requests"}), 429
            return f(*args, **kwargs)

        return wrapper

    return decorator
