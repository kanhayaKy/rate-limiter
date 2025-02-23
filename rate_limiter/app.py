from flask import Flask
from rate_limiter.decorator import rate_limit

app = Flask("rate_limiter")


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@rate_limit
@app.route("/limited")
def limited():
    return "Limited, don't over use me!"


@app.route("/unlimited")
def unlimited():
    return "Unlimited! Let's Go!"
