#!/usr/bin/env python3
"""Basic Flask app script
"""
from flask import Flask, jsonify

app = Flask(__name__)
""" flask instance"""

@app.route('/', methods=['GET'])
def welcome():
    """ Defines a route for the root URL ("/")"""
    return jsonify({"message": "Bienvenue"})

if __name__ == "__main__":
    """ ensures script is run directly """
    app.run(host="0.0.0.0", port="5000")