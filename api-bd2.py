import json
import decimal
import os
from flask import Flask, request, render_template, jsonify, current_app


from werkzeug.security import safe_str_cmp
from jwt import encode, decode, ExpiredSignatureError, InvalidTokenError
from functools import wraps
import datetime

import database2 as db



APP = Flask(__name__)
APP.config['SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'chave_super_secreta')


@APP.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get("username", "NULL")
    password = data.get("password", "NULL")

    user = db.get_user_by_name(username)  #CHANGE
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
            user = db.get_user_by_name(data['sub']) #CHANGE
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
def user_list():
    user_list = [{'id': u.u_id, 'username': u.username} for u in db.get_users()] #CHANGE
    response = jsonify({'users': user_list})
    return response, 200
        


@APP.route('/movies', methods=['GET'])
def movie_list():
    movie_list = [{'id': m.m_id, 'name': m.name} for m in db.get_movies()] 
    response = jsonify({'movies': movie_list})
    return response, 200
        


@APP.route('/user_info/<int:user_id>', methods=['GET'])
def user(user_id):
    def get_user_info(user):
        response = jsonify({'user': user.username})
        return response
        
    user = db.get_user_by_id(user_id) #CHANGE
    if user is None:
        response = jsonify({'status': 'failed', 'fail reason': 'User not found'})
        return response, 404
    if request.method == 'GET':
        return get_user_info(user)
    else:
        response = jsonify({'status': 'failed', 'fail reason': 'Wrong method, only POST and GET available'})
        return response, 401


@APP.route('/user_info/<int:user_id>/movies', methods=['GET', 'POST'])
def user_movies(user_id):
    def get_user_movies(u_id):
        results = db.get_movies_for_user(user_id)
        if not results:
            response = jsonify({'Movies': []})
        else:
            response = jsonify({'Movies': [{'movieID': movie.m_id, 'movieName': movie.name} for movie in results]})
        return response, 200
    def new_user_movie(u_id):
        try:
            req_json = request.get_json()
            new_favorite = req_json['movie']
            movie = db.get_movie_by_name(new_favorite)
            if not movie:
                return jsonify({'status': 'failed', 'fail reason': 'Movie not found'})
            db.create_user_movie(u_id, movie.m_id)
            response = jsonify({'status': 'success'})
            return response
        except:
            response = jsonify({'status': 'failed', 'fail reason': 'Wrong arguments'})
            return response, 500
    
    if request.method == 'GET':
        return get_user_movies(user_id)
    elif request.method == 'POST':
        return new_user_movie(user_id)
    else:
        response = jsonify({'status': 'failed', 'fail reason': 'Wrong method, only POST and GET available'})
        return response, 401


@APP.route('/user_info/<int:user_id>/movies/<int:movie_id>', methods=['GET'])
def movies_info(user_id, movie_id):
    movie = db.get_movie_by_id(movie_id)
    return jsonify({'Name': movie.name, 'Author': movie.author, 'IMDB Rating': movie.imdb_rating})

        
if __name__ == '__main__':
    users = db.get_users() #CHANGE
    if not users:
        db.create_user('admin_user', 'admin_pass', 'Padrinho')
        db.create_user('readonly_user', 'readonly_pass', 'Jurassic World')
        db.create_user('readwrite_user', 'readwrite_pass', 'Jurassic Park')
        db.create_movie('Padrinho', 'Mario Puzo', 10)
        db.create_movie('Padrinho 2', 'Mario Puzo', 9)
        db.create_movie('Padrinho 3', 'Mario Puzo', 1)
        db.create_movie('Jurassic Park', 'Michael Crichton', 8)
        db.create_movie('Jurassic World', 'Derek Connolly, Colin Trevorrow', 0)
        db.create_movie('Gladiator', 'David Franzoni', 8)
    APP.run(port='5050')