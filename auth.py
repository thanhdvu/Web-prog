from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth', __name__)

DB_PATH = 'users.db'

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        hashed_pw = generate_password_hash(password)

        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('INSERT INTO users (username, email, password) VALUES (?, ?, ?)',
                           (username, email, hashed_pw))
            conn.commit()
        except sqlite3.IntegrityError:
            flash('Username hoặc email đã tồn tại!')
            return redirect(url_for('auth.signup'))
        finally:
            conn.close()

        flash('Đăng ký thành công!')
        return redirect(url_for('auth.login'))
    
    return render_template('signup_ko.html')

@auth.route('/login', methods=['GET', 'POST'])
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
            flash('Đăng nhập thành công!')
            return redirect(url_for('main.profile'))  # hoặc route khác tùy bạn
        else:
            flash('Email hoặc mật khẩu không đúng!')
            return redirect(url_for('auth.login'))
    
    return render_template('login_ko.html')

@auth.route('/logout')
def logout():
    session.clear()
    flash('Đăng xuất thành công!')
    return redirect(url_for('auth.login'))
