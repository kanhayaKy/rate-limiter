import os

from flask import Flask
from redis import Redis

from rate_limiter.algorithms import SlidingWindowCounterAlgorithm
from rate_limiter.decorator import rate_limit
from rate_limiter.util import get_algorithm_from_name

# Environment variables
ALGORITHM = os.getenv("RATE_LIMIT_ALGORITHM", "sliding_window_counter")


app = Flask("rate_limiter")

rate_limiter = get_algorithm_from_name(ALGORITHM)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/limited")
@rate_limit(rate_limiter=rate_limiter)
def limited():
    return "Limited, don't over use me!"


@app.route("/unlimited")
def unlimited():
    return "Unlimited! Let's Go!"
