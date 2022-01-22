# -*- coding: utf8 -*-
import base64
import re
import requests

def main_handler(event, context):
    event['headers'] = {k.lower(): v for k, v in event['headers'].items()}
    event['headers'].pop('host', '')
    response = requests.request(
        event['httpMethod'],
        event['headers'].pop('x-src', event['queryString'].pop('x-src', 'https://httpbin.org/anything')),
        params=event['queryString'],
        data=event.get('body'),
        headers=event['headers'],
        verify=False,
    )
    response.headers.pop('content-length', None)
    base64_encoded = not bool(re.match(r'(^$)|(^text$)|(^text/)|(^application.*[/+-.](xml|json|yaml|javascript|html|text|wbxml)([/+-.]|$))', response.headers['content-type']))
    return {
        'isBase64Encoded': base64_encoded,
        'statusCode': response.status_code,
        'headers': dict(response.headers),
        'body': base64.b64encode(response.content).decode() if base64_encoded else response.text,
    }
