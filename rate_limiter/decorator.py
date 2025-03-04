from functools import wraps
from flask import jsonify, request

from rate_limiter.algorithms import TokenBucketAlgorithm
from rate_limiter.exceptions import RateLimitExceeded


default_rate_limiter = TokenBucketAlgorithm()


def rate_limit(rate_limiter=default_rate_limiter):
    """Decorator to limit requests."""

    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):
            request_ip = request.remote_addr

            try:
                rate_limiter.should_process(request_ip)
                return func(*args, **kwargs)
            except RateLimitExceeded:
                return jsonify({"error": "Too many requests"}), 429

        return wrapper

    return decorator
