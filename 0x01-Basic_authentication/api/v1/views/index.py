#!/usr/bin/env python3
""" """
from flask import Flask, abort

app = Flask(__name__)


@app.route('/api/v1/unauthorized', methods=['GET'])
def unauthorized():
    abort(401)
