from flask import Flask
from redis import Redis

from rate_limiter.algorithms import SlidingWindowCounterAlgorithm
from rate_limiter.decorator import rate_limit

app = Flask("rate_limiter")

redis_store = Redis(host="localhost", port=6379, decode_responses=True)
rate_limiter = SlidingWindowCounterAlgorithm(store=redis_store)


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
