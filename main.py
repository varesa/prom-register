import datetime
import os
import sys
import json

from flask import Flask, request

# Initialize app

app = Flask(__name__)

if 'TOKEN' not in os.environ.keys():
    authenticate = False
else:
    token = os.environ['TOKEN']
    authenticate = True

if 'CONFIG_PATH' not in os.environ.keys():
    print('You need to pass in the path to store config files in as environment variable "CONFIG_PATH"')
    sys.exit(1)
path = os.environ['CONFIG_PATH']


def get_config(targets):
    return json.dumps([
        {
            "targets": targets,
        }
    ])


@app.route('/')
def root():
    return 'Please POST {"hostname": "...", "targets": ["..."], "token": "(optional)"]} to /register'


@app.route('/register', methods=['POST'])
def register():
    if authenticate:
        if request.json['token'] != token:
            return "Authentication error"

    host = request.json['hostname']
    file = os.path.join(path, host)

    if 'targets' not in request.json.keys():
        return "Error: targets missing"
    targets = request.json['targets']
    if not isinstance(targets, list):
        return "Error: targets should be an array"

    exists = os.path.isfile(file)

    with open(os.path.join(path, host), 'w') as hostfile:
        hostfile.write(get_config(targets))

    if exists:
        return "OK"
    else:
        return "Created"


# Basic healthcheck for orchestration and monitoring

@app.route('/health')
def healthcheck():
    return 'OK'

