import os
import requests
import logging
from flask import Flask, request

app = Flask(__name__)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    params = request.args.to_dict()
    headers = dict(request.headers)
    headers.pop('Host', None)
    headers.pop('X-Api-Requestid', None)
    headers.pop('X-Forwarded-For', None)
    headers.pop('X-Client-Proto', None)
    headers.pop('X-Client-Proto-Ver', None)
    headers.pop('X-Real-Ip', None)
    headers.pop('X-Scf-Appid', None)
    headers.pop('X-Scf-Memory', None)
    headers.pop('X-Scf-Name', None)
    headers.pop('X-Scf-Namespace', None)
    headers.pop('X-Scf-Region', None)
    headers.pop('X-Scf-Request-Id', None)
    headers.pop('X-Scf-Timeout', None)
    headers.pop('X-Scf-Uin', None)
    headers.pop('X-Scf-Version', None)
    url = headers.pop('X-Src', params.pop('x-src', 'https://httpbin.org/anything'))
    response = requests.request(
        request.method,
        url,
        params=params,
        data=request.data,
        headers=headers,
        stream=True,
    )
    response.headers.pop('Transfer-Encoding', None)
    return (response.raw.read(), response.status_code, response.headers.items())

app.run(port=9000, host='0.0.0.0')
