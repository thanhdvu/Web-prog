from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
#encrypt
import jwt, datetime

auth_bp = Blueprint('auth', __name__)
SECRET_KEY = 'supersecret'
users = {} 

@auth_bp.route('/register', methods=['POST'])
def register():
    ...

@auth_bp.route('/login', methods=['POST'])
def login():