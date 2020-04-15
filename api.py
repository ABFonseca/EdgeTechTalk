import json
import decimal
import os
from flask import Flask, request, render_template, jsonify, current_app

USERNAME = 'you'

APP = Flask(__name__)

@APP.route('/user_info', methods=['GET', 'POST'])
def user():
    def get_user_info():
        """
        Get the axis configured values
        :return: json
        """
        response = jsonify({'user': USERNAME})
        return response

    def post_user_info():
        """
        Update the axis configured values
        :return: json
        """
        try:
            req_json = request.get_json()
            new_name = req_json['user']
            global USERNAME
            USERNAME = new_name
            response = jsonify({'status': 'success'})
            return response
        except:
            response = jsonify({'status': 'failed', 'fail reason': 'Wrong arguments'})
            return response, 500
        

    if request.method == 'GET':
        return get_user_info()
    elif request.method == 'POST':
        return post_user_info()
    else:
        response = jsonify({'status': 'failed', 'fail reason': 'Wrong method, only POST and GET available'})
        return response, 401
        
        
        
if __name__ == '__main__':
    APP.run(port='5050')