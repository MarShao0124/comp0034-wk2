from markupsafe import escape
from flask import current_app as app

@app.route('/')
def Hello():
    return "Hello, World!"

@app.route("/<name>")
def hello(name=None):
    return f"Hello, {escape(name)}!"
