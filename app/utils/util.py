from datetime import datetime, timezone, timedelta #we want the token to have an expiration date
from jose import jwt
import jose
from functools import wraps
from flask import request, jsonify

SECRET_KEY = "super secret secrets"

def encode_token(mechanic_id):
    '''Payload is all the info packed into token'''
    payload = { 
        'exp': datetime.now(timezone.utc) + timedelta(days=0, hours=1), #sets expiration date
        'iat': datetime.now(timezone.utc), #issued at date
        'sub': str(mechanic_id) #who does the token belong to
        
    }
    
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token

def token_required(f):
    @wraps(f)
    def decoration(*args, **kwargs):
        token = None
        
        if "Authorization" in request.headers:
            #gives us Bearer token
            token = request.headers["Authorization"].split()[1]
            
            if not token:
                return jsonify({"error": "missing token"}), 401
            
            try: 
                data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
                print(data)
                request.logged_in_mechanic_id = data['sub']
            except jose.exceptions.ExpiredSignatureError:
                return jsonify({"message": "token is expired"}), 403
            except jose.exceptions.JWTError:
                return jsonify({"message": "Invalid token"}), 401
            
        return f(*args, **kwargs)
    return decoration 