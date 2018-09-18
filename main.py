import datetime
import os
import json

from flask import Flask, redirect, render_template, request

# Initialize app

app = Flask(__name__)

if 'TOKEN' not in os.environ.keys():
    authenticate = False
else:
    token = os.environ['TOKEN']
    authenticate = True

@app.route('/')
def root():
    return 'Please POST {"hostname": "..." [, "token": "..."]} to /register'

@app.route('/register', methods=['POST'])
def register():
    host = request.json('hostname')
    print(host)
    return "OK"


# Basic healthcheck for orchestration and monitoring

@app.route('/health')
def healthcheck():
    return 'OK'

