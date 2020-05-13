from flask import Flask, request, abort
from functools import wraps
import sys
import json
from jose import jwt
from urllib.request import urlopen

app = Flask(__name__)

AUTH0_DOMAIN = 'loay96.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'Image'

class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


def get_token_auth_header():
    
    if 'Authorization' not in request.headers:
        abort(401)

    auth_header = request.headers['Authorization']
    header_parts = auth_header.split(' ')
    
    if len(header_parts) != 2:
       abort(401)
    elif header_parts[0].lower() != 'bearer':
       abort(401)

    return header_parts[1]

def verify_decode_jwt(token):
    # GET THE PUBLIC KEY FROM AUTH0
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())
    
    # GET THE DATA IN THE HEADER
    unverified_header = jwt.get_unverified_header(token)
    
    # CHOOSE OUR KEY
    rsa_key = {}
    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed.'
        }, 401)

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    
    # Finally, verify!!!
    if rsa_key:
        try:
            # USE THE KEY TO VALIDATE THE JWT
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer=f'https://{AUTH0_DOMAIN}/'
            )

            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired.'
            }, 401)

        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims. Please, check the audience and issuer.'
            }, 401)
        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 400)
    raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to find the appropriate key.'
            }, 400)



def requires_auth(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        jwt = get_token_auth_header()
        try:
            payload = verify_decode_jwt(jwt)
        except:
            abort(401)
        return f(payload, *args, **kwargs)
    return wrapper



@app.route('/headers')
@requires_auth
def headers(jwt):
    jwt = get_token_auth_header()
    print(jwt)
    return 'not implemented'