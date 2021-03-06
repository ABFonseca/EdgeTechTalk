import json
import decimal
import os
from flask import Flask, request, render_template, jsonify, current_app


from werkzeug.security import safe_str_cmp
from jwt import encode, decode, ExpiredSignatureError, InvalidTokenError
from functools import wraps
import datetime

class User(object):
    """
    Class User
        used for API authentication
    """

    def __init__(self, id, username, password):
        """
        Contructor for User class
        :param id: id of the user
        :param username: username for the user
        :param password: password for the user
        """
        self.id = id
        self.username = username
        self.password = password
        self.favorite_movie = 'Padrinho'

    def __str__(self):
        return "User(id='%s')" % self.id


USERS = [
    User(1, os.getenv('API_ADMIN_USER', 'admin_user').strip().strip('"'), os.getenv('API_ADMIN_PASS', 'admin_pass').strip().strip('"')),
    User(2, "readonly_user", "readonly_pass"),
    User(3, "readwrite_user", "readwrite_pass"),
]

USERNAME_TABLE = {u.username: u for u in USERS}
USERID_TABLE = {u.id: u for u in USERS}


APP = Flask(__name__)
APP.config['SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'chave_super_secreta')


@APP.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get("username", "NULL")
    password = data.get("password", "NULL")

    user = USERNAME_TABLE.get(username, None)
    if user and safe_str_cmp(user.password.encode('utf-8'), password.encode('utf-8')):
        token = encode({
            'sub': user.username,
            'iat': datetime.datetime.utcnow(),
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
            current_app.config['SECRET_KEY'])
        response = jsonify({'token': token.decode('UTF-8')})
        return response
    response = jsonify({'message': 'Invalid credentials', 'authenticated': False})
    return response

def token_required(f):
    @wraps(f)
    def _verify(*args, **kwargs):
        print(request.headers)
        auth_headers = request.headers.get('Authorization', '').split()

        invalid_msg = {
            'message': 'Invalid token. Registeration and / or authentication required',
            'authenticated': False
        }
        expired_msg = {
            'message': 'Expired token. Reauthentication required.',
            'authenticated': False
        }

        if len(auth_headers) != 2:
            response = jsonify(invalid_msg)
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response, 401

        try:
            token = auth_headers[1]
            data = decode(token, current_app.config['SECRET_KEY'])
            user = USERNAME_TABLE.get(data['sub'], None)
            if not user:
                raise RuntimeError('User not found')
            return f(*args, **kwargs)
        except ExpiredSignatureError:
            response = jsonify(expired_msg)
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response, 401  # 401 is Unauthorized HTTP status code
        except (InvalidTokenError, Exception) as e:
            print(e)
            response = jsonify(invalid_msg)
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response, 401

    return _verify

@APP.route('/user_info', methods=['GET'])
def user_info():
    user_list = [{'id': u.id, 'username': u.username} for u in USERS]
    print(user_list)
    response = jsonify({'users': user_list})
    return response, 200
        


@APP.route('/user_info/<int:user_id>', methods=['GET', 'POST'])
@token_required
def user(user_id):
    def get_user_info(user):
        """
        Get the axis configured values
        :return: json
        """
        response = jsonify({'user': user.username, 'movie': user.favorite_movie})
        return response

    def post_user_info(user):
        """
        Update the axis configured values
        :return: json
        """
        try:
            req_json = request.get_json()
            new_favorite = req_json['movie']
            user.favorite_movie = new_favorite
            response = jsonify({'status': 'success'})
            return response
        except:
            response = jsonify({'status': 'failed', 'fail reason': 'Wrong arguments'})
            return response, 500
        
    user = USERID_TABLE.get(user_id, None)
    if user is None:
        response = jsonify({'status': 'failed', 'fail reason': 'User not found'})
        return response, 404
    if request.method == 'GET':
        return get_user_info(user)
    elif request.method == 'POST':
        return post_user_info(user)
    else:
        response = jsonify({'status': 'failed', 'fail reason': 'Wrong method, only POST and GET available'})
        return response, 401
        
        
        
if __name__ == '__main__':
    APP.run(port='5050')