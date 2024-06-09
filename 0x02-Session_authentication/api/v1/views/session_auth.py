#!/usr/bin/env python3
""" Session authentication view """
from flask import Flask
from flask import jsonify, request, make_response
from api.v1.views import app_views
from os import getenv


app = Flask(__name__)


@app.route('/auth_session/login', methods=['POST'], strict_slashes=False)
""" setting strict-slash as False makes url slash tolerant"""
def login():
    """ define a route /login that accepts POST requests """
    email = request.form.get('email')
    password = request.form.get('password')
    
    if not email:
        return jsonify({"error": "email missing"}), 400
    
    if not password:
        return jsonify({"error": "password missing"}), 400

    try:
        users = User.search('email': email)
    except Exception:
        return jsonify({"error": "no user found for this email"}), 404

    if not users:
        return jsonify({"error": "no user found for this email"}), 404

    for user in users:
        if not user.is_valid_password(password):
            return jsonify({"error": "wrong password"}), 401

    from api.v1.app import auth

    user = found_users[0]
    session_id = auth.create_session(user.id)

    SESSION_NAME = getenv("SESSION_NAME")

    response = jsonify(user.to_json())
    response.set_cookie(SESSION_NAME, session_id)

    return response
