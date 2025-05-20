
from flask import Blueprint, request, jsonify, redirect, render_template
from werkzeug.security import generate_password_hash, check_password_hash
from db import users_table
import jwt, datetime
import traceback

auth_bp = Blueprint('auth', __name__)
SECRET_KEY = 'yonseiuni'

@auth_bp.route('/signup_ko', methods=['POST'])
def signup_ko_post():
    print("✅ POST /auth/signup_ko 요청 수신됨")
    
    try:
        data = request.form
        email = data.get('email')
        raw_password = data.get('password')
        
        print(f"📩 입력된 이메일: {email}, 비밀번호: {raw_password}")
        
        if not email or not raw_password:
            print("❌ 이메일 또는 비밀번호 누락")
            return "<script>alert('이메일과 비밀번호를 입력해주세요.'); history.back();</script>"
        
        response = users_table.get_item(Key={'email': email})
        print("🗃️ DynamoDB 조회 결과:", response)
        
        if 'Item' in response:
            print("⚠️ 이미 등록된 이메일입니다")
            return "<script>alert('이미 등록된 이메일입니다.'); history.back();</script>"
        
        hashed_pw = generate_password_hash(raw_password)
        print("🔐 암호화된 비밀번호:", hashed_pw)
        
        users_table.put_item(Item={
            'email': email,
            'password': hashed_pw
        })
        
        print("✅ DynamoDB에 사용자 정보 저장 완료:", email)
        return redirect('/ko/login')
    
    except Exception as e:
        print("❌ DynamoDB 저장 중 오류 발생:", str(e))
        traceback.print_exc()
        return "<script>alert('회원가입 중 오류가 발생했습니다: " + str(e) + "'); history.back();</script>"

@auth_bp.route('/login_ko', methods=['POST'])
def login_ko_post():
    print("✅ POST /auth/login_ko 요청 수신됨")
    
    try:
        data = request.form
        email = data.get('email')
        password = data.get('password')
        
        print(f"📩 입력된 이메일: {email}")
        
        response = users_table.get_item(Key={'email': email})
        print("🗃️ DynamoDB 조회 결과:", response)
        
        user = response.get('Item')
        
        if not user:
            print("❌ 사용자를 찾을 수 없음:", email)
            return "<script>alert('이메일 또는 비밀번호가 잘못되었습니다.'); history.back();</script>"
        
        if not check_password_hash(user['password'], password):
            print("❌ 비밀번호 불일치:", email)
            return "<script>alert('이메일 또는 비밀번호가 잘못되었습니다.'); history.back();</script>"
        
        token = jwt.encode({
            'email': email,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }, SECRET_KEY, algorithm='HS256')
        
        print("✅ 로그인 성공:", email)
        
        return redirect('/ko')
    
    except Exception as e:
        print("❌ 로그인 중 오류 발생:", str(e))
        traceback.print_exc()
        return "<script>alert('로그인 중 오류가 발생했습니다: " + str(e) + "'); history.back();</script>"