#!/usr/bin/env python3
"""Basic Flask app script
"""
from flask import Flask, abort, jsonify, request
from auth import Auth
from sqlalchemy.orm.exc import NoResultFound

AUTH = Auth()
""" instance of the Auth class
    used to handle use autheticatn & registratn
"""

app = Flask(__name__)
""" flask instance"""


@app.route('/', methods=['GET'])
def welcome():
    """ Defines a route for the root URL ("/")"""
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'])
def users():
    """ Registers a new user """
    email = request.form['email']
    password = request.form['password']
    try:
        new_user = AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "User already exists"}), 400


@app.route('/sessions', methods=['POST'])
def login():
    """Handles user login"""
    # Get the request data fields
    email = request.form['email']
    password = request.form['password']

    # Validate the login credentials
    if AUTH.valid_login(email, password):
        # If credentials are valid, create a new session
        session_id = AUTH.create_session(email)

        # Set the session ID as a cookie on the response
        response = jsonify({"email": email, "message": "logged in"})
        response.set_cookie("session_id", session_id)

        # Return the JSON payload
        return response
    else:
        # If credentials are invalid, return 401 error
        abort(401)

@app.route('/sessions', methods=['DELETE'])
def log_out() -> str:
    """Find the user with the requested session ID.
    If the user exists destroy the session and redirect the user to GET /.
    If the user does not exist, respond with a 403 HTTP status.
    """
    session_id = request.cookies.get("session_id", None)

    if session_id is None:
        abort(403)

    user = AUTH.get_user_from_session_id(session_id)

    if user is None:
        abort(403)

    AUTH.destroy_session(user.id)

    return redirect('/')

if __name__ == "__main__":
    """ ensures script is run directly """
    app.run(host="0.0.0.0", port="5000")
