#!/usr/bin/env python
# encoding: utf-8

from flask import Flask, request, Response
import subprocess
import argparse
import json

HOST = '127.0.0.1'  # '0.0.0.0'
PORT = '5000'

app = Flask(__name__)


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

    cmd = args.run + query
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

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('--run', nargs='+', type=str)

    args = parser.parse_args()

    app.run(host=HOST, port=PORT)
