#!/usr/bin/env python3

"""
Basic Flask app module.

This module sets up a simple Flask web application with a single route.
It demonstrates how to create a basic JSON API endpoint using Flask.

The app responds to GET requests at the root URL with a JSON message.
"""

from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/", methods=["GET"])
def welcome() -> str:
    """Route handler for the root URL."""
    return jsonify({"message": "Bienvenue"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
