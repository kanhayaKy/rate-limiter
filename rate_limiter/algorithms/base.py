from rate_limiter.exceptions import RateLimitExceeded


class RateLimitingAlgorithm:
    def __init__(self):
        pass

    def __call__(self, *args, **kwds):
        if self.should_process(*args, **kwds):
            return True
        else:
            raise RateLimitExceeded()

    def should_process(self, *args, **kwargs):
        raise NotImplementedError("Subclasses must implement `should_process` method")
