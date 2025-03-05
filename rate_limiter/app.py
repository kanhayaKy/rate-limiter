from flask import Flask

from rate_limiter.algorithms import FixedWindowCounter
from rate_limiter.decorator import rate_limit

app = Flask("rate_limiter")
rate_limiter = FixedWindowCounter()


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
