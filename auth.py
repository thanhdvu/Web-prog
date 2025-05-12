from flask import Blueprint, request, jsonify, redirect
from werkzeug.security import generate_password_hash, check_password_hash
from db import users_table
import jwt, datetime
import traceback

auth_bp = Blueprint('auth', __name__)
SECRET_KEY = 'yonseiuni'

@auth_bp.route('/ko/signup', methods=['GET','POST'])
def signup_ko():
    try:
        data = request.form
        email = data.get('email')
        raw_password = data.get('password')

        if not email or not raw_password:
            return "<script>alert('이메일과 비밀번호를 입력해주세요.'); history.back();</script>"

        response = users_table.get_item(Key={'email': email})
        if 'Item' in response:
            return "<script>alert('이미 등록된 이메일입니다.'); history.back();</script>"

        hashed_pw = generate_password_hash(raw_password)
        users_table.put_item(Item={
            'email': email,
            'password': hashed_pw
        })

        print(f"✅ Saved to DynamoDB: {email}")
        return redirect('/ko/login')

    except Exception as e:
        print("❌ Signup error:", e)
        traceback.print_exc()
        return "<script>alert('회원가입 중 오류가 발생했습니다.'); history.back();</script>"

@auth_bp.route('/ko/login', methods=['POST'])
def login_ko():
    data = request.form
    email = data['email']
    password = data['password']

    response = users_table.get_item(Key={'email': email})
    user = response.get('Item')

    if not user or not check_password_hash(user['password'], password):
        return "<script>alert('이메일 또는 비밀번호가 잘못되었습니다.'); history.back();</script>"

    token = jwt.encode({
        'email': email,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }, SECRET_KEY, algorithm='HS256')

    return jsonify({'token': token})