#!/usr/bin/env python3

"""
Basic Flask app module.

This module sets up a simple Flask web application with a single route.
It demonstrates how to create a basic JSON API endpoint using Flask.

The app responds to GET requests at the root URL with a JSON message.
"""

from typing import Union
from flask import Flask, request, jsonify, abort, make_response, redirect
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


@app.route('/sessions', methods=['POST'])
def login():
    """
    Log in a user.

    Expects form data with 'email' and 'password' fields.
    If the login information is incorrect, returns a 401 status.
    Otherwise, creates a new session for the user, sets a 'session_id' cookie,
    and returns a 200 status with a JSON payload containing the user's email
    and a 'logged in' message.
    """
    email = request.form.get('email')
    password = request.form.get('password')

    if not AUTH.valid_login(email, password):
        abort(401)

    session_id = AUTH.create_session(email)
    response = make_response(
            jsonify({"email": email, "message": "logged in"}),
            200
        )
    response.set_cookie('session_id', session_id)
    return response


@app.route('/sessions', methods=['DELETE'])
def logout() -> Union[redirect, abort]:
    """
    Logout the user by destroying the session.

    Returns:
        Union[redirect, abort]: Redirects to the root route if the session is
        successfully destroyed, otherwise returns a 403 HTTP status.
    """
    session_id = request.cookies.get('session_id')

    if session_id is None:
        abort(403)

    user = AUTH.get_user_from_session_id(session_id)

    if user is None:
        abort(403)

    AUTH.destroy_session(user.id)

    return redirect('/')


@app.route('/profile', methods=['GET'])
def profile() -> Union[jsonify, abort]:
    """
    Retrieve the user's profile information.

    Returns:
        Union[jsonify, abort]: A JSON response with the user's email if the
        session ID is valid, otherwise an abort with a 403 HTTP status.
    """
    session_id = request.cookies.get('session_id')

    if session_id is None:
        abort(403)

    user = AUTH.get_user_from_session_id(session_id)

    if user is None:
        abort(403)

    return jsonify({"email": user.email}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
