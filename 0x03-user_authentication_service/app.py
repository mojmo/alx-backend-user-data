#!/usr/bin/env python3

"""
Basic Flask app module.

This module sets up a simple Flask web application with a single route.
It demonstrates how to create a basic JSON API endpoint using Flask.

The app responds to GET requests at the root URL with a JSON message.
"""

from flask import Flask, request, jsonify
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route("/", methods=["GET"])
def welcome() -> str:
    """Route handler for the root URL."""
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'])
def register_user() -> tuple:
    """
    Register a new user.

    Returns:
        tuple: A tuple containing the JSON response and the HTTP status code.
    """
    email = request.form.get('email')
    password = request.form.get('password')

    try:
        user = AUTH.register_user(email, password)
        return jsonify({"email": user.email, "message": "user created"}), 200
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
