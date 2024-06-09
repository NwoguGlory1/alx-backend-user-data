#!/usr/bin/env python3
""" Session authentication view """
from flask import jsonify, request, make_response
from api.v1.views import app_views
from os import getenv
from models.user import User  # Import User model here


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login():
    """ Define a route /auth_session/login that accepts POST requests """

    # Retrieve email and password from the form data
    email = request.form.get('email')
    password = request.form.get('password')

    # Check if email is missing or empty
    if not email:
        return jsonify({"error": "email missing"}), 400

    # Check if password is missing or empty
    if not password:
        return jsonify({"error": "password missing"}), 400

    # Try to find users with the provided email
    try:
        users = User.search({'email': email})
    except Exception:
        return jsonify({"error": "no user found for this email"}), 404

    # Check if no users were found
    if not users:
        return jsonify({"error": "no user found for this email"}), 404

    # Validate the provided password
    user = users[0]  # Assuming we take the first user found
    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    # Import auth only where it's needed to avoid circular imports
    from api.v1.app import auth

    # Create a session ID for the user
    session_id = auth.create_session(user.id)

    # Get the session name from the environment variable
    SESSION_NAME = getenv("SESSION_NAME")

    # Create a response object and set the session cookie
    response = jsonify(user.to_json())
    response.set_cookie(SESSION_NAME, session_id)

    return response


@app_views.route('/auth_session/logout',
                 methods=['DELETE'], strict_slashes=False)
def logout():
    """ DELETE /auth_session/logout
    Return:
        - Empty dictionary if succesful
    """
    from api.v1.app import auth

    deleted = auth.destroy_session(request)

    if not deleted:
        abort(404)

    return jsonify({}), 200
