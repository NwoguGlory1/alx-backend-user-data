#!/usr/bin/env python3
"""Basic Flask app script
"""
from flask import Flask, jsonify, request
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


if __name__ == "__main__":
    """ ensures script is run directly """
    app.run(host="0.0.0.0", port="5000")
