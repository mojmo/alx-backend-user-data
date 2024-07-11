#!/usr/bin/env python3

"""Handles all routes for the Session authentication."""

from api.v1.views import app_views
from flask import request, jsonify, make_response
from models.user import User
import os


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login():
    """
    Handles the user login for session authentication
    """
    email = request.form.get('email')
    password = request.form.get('password')

    if not email:
        return jsonify({"error": "email missing"}), 400
    if not password:
        return jsonify({"error": "password missing"}), 400

    try:
        users = User.search({'email': email})
    except Exception:
        return jsonify({"error": "no user found for this email"}), 404

    if not users:
        return jsonify({"error": "no user found for this email"}), 404

    for user in users:
        if not user.is_valid_password(password):
            return jsonify({"error": "wrong password"}), 401

    user = users[0]

    from api.v1.app import auth

    session_id = auth.create_session(user.id)
    user_json = user.to_json()

    response = make_response(jsonify(user_json))
    session_name = os.getenv('SESSION_NAME')
    response.set_cookie(session_name, session_id)

    return response
