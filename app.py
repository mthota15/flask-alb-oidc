from flask import Flask, request, jsonify, abort, g
from functools import wraps
import jwt
import requests
import os
import base64
import json

application = Flask(__name__)

def auth_required(f):
    '''
    This decorator checks the header to ensure a valid token is set
    '''
    @wraps(f)
    def func(*args, **kwargs):
        try:
            if 'X-Amzn-Oidc-Data' not in request.headers:
                abort(401)
            token = request.headers.get('X-Amzn-Oidc-Data')
            region = os.getenv('REGION', 'us-east-1')
            decoded_jwt_headers = base64.b64decode(token.split('.')[0])
            kid = json.loads(decoded_jwt_headers)['kid']
            url = 'https://public-keys.auth.elb.' + region + '.amazonaws.com/' + kid
            pub_key = requests.get(url).text
            g.user = jwt.decode(token, pub_key, algorithms=['ES256'])
            return f(*args, **kwargs)
        except (jwt.DecodeError, jwt.ExpiredSignatureError) as e:
            print(e)
            abort(401)
    return func

@application.route("/")
@auth_required
def index():
    return jsonify(g.user)

@application.route("/health")
def health():
    return 'ok'
