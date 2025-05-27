from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import sqlite3
import os
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

auth_bp = Blueprint('auth_bp', __name__)

DB_PATH = 'users.db'
DB_PATH = 'instance/yonsei.db'

UPLOAD_FOLDER = os.path.join('static', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def get_db_connection():
    db_path = os.path.join(os.path.dirname(__file__), 'users.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        hashed_pw = generate_password_hash(password)

        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        try:
            cursor.execute(
                'INSERT INTO users (email, password) VALUES (?, ?)',
                (email, hashed_pw)
            )
            conn.commit()
        except sqlite3.IntegrityError:
            flash('이미 존재하는 이메일입니다.')
            return redirect(url_for('auth_bp.signup'))
        finally:
            conn.close()

        flash('회원가입에 성공했습니다!')
        return redirect(url_for('auth_bp.login'))

    return render_template('ko/auth/login_ko.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
        user = cursor.fetchone()
        conn.close()

        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            flash('로그인에 성공했습니다!')
            return redirect(url_for('register_ko'))  
        else:
            flash('이메일 또는 비밀번호가 올바르지 않습니다.')
            return redirect(url_for('auth_bp.login'))
    
    return render_template('ko/auth/login_ko.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('로그아웃되었습니다.')
    return redirect(url_for('auth_bp.login'))

@auth_bp.route('/register_item', methods=['POST'])
def register_item():
    prdt_cl_nm = request.form.get('PRDT_CL_NM')
    start_ymd = request.form.get('START_YMD')
    prdt_nm = request.form.get('PRDT_NM')
    ubuilding = request.form.get('uBuilding')
    description = request.form.get('description')
    image = request.files.get('itemImage')

    image_path = None
    if image and image.filename != '':
        filename = secure_filename(image.filename)
        image_path = os.path.join(UPLOAD_FOLDER, filename)
        image.save(image_path)

    db_path = os.path.abspath('instance/yonsei.db')
    print("💡 DB path used:", db_path)
 
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO found_items (prdt_cl_nm, start_ymd, prdt_nm, ubuilding, description, image_path)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (prdt_cl_nm, start_ymd, prdt_nm, ubuilding, description, image_path))
    conn.commit()
    conn.close()

    flash("습득물이 성공적으로 등록되었습니다.")
    return redirect(url_for('index_ko'))
