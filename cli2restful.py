#!/usr/bin/env python
# encoding: utf-8

from flask import Flask, request, Response
from flask_cors import CORS
import subprocess
import argparse
import json

HOST = '0.0.0.0'  # '127.0.0.1'
PORT = '8001'

app = Flask(__name__)
CORS(app)

RUN = None

def urlQuery2argumentList(url_query_parameter):
    args = []

    for q in url_query_parameter:
        k, v = q
        args.append('--' + k)
        args.append(v)

    return args


@app.route("/")
def hello():
    query = urlQuery2argumentList(request.args.items())

    cmd = RUN + query
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            stdin=subprocess.PIPE)
    out, err = p.communicate()

    try:
        out = json.dumps(eval(out.strip()))
    except Exception, e:
        out = json.dumps({'stdout': out})

    return Response(
        response=out,
        mimetype="application/json",
        status=200
    )

def main(run):
    global RUN
    RUN = run.split()

    return app

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('--run', nargs='+', type=str)

    args = parser.parse_args()

    RUN = args.run

    app.run(host=HOST, port=PORT)
