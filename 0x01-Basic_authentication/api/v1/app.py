#!/usr/bin/env python3
""" Error handler: Unauthorized script"""
from flask import Flask, jsonify
""" """

app = Flask(__name__)


@app.errorhandler(401)
def unauthorized(error):
    """ function to handle the error"""
    return jsonify({"error": "Unauthorized"}), 401
