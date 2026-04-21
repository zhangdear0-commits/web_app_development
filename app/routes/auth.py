from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models.user import User
import datetime
import hashlib

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    註冊會員
    """
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        name = request.form.get('name')
        role = request.form.get('role', 'participant')
        phone = request.form.get('phone', '')

        if not email or not password or not name:
            flash("請填寫所有必填欄位 (Email, 密碼, 姓名)", "error")
            return redirect(url_for('auth.register'))

        password_hash = hashlib.sha256(password.encode()).hexdigest()
        data = {
            'email': email,
            'password_hash': password_hash,
            'name': name,
            'role': role,
            'phone': phone,
            'created_at': datetime.datetime.now().isoformat()
        }

        user_id = User.create(data)
        if user_id:
            flash("註冊成功！請登入", "success")
            return redirect(url_for('auth.login'))
        else:
            flash("該 Email 可能已被註冊或發生錯誤", "error")
            return redirect(url_for('auth.register'))

    return render_template('auth/register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    登入會員
    """
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if not email or not password:
            flash("請輸入 Email 與密碼", "error")
            return redirect(url_for('auth.login'))
            
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        # 自訂實作：取得所有 User 進行比對
        users = User.get_all()
        user = next((u for u in users if u['email'] == email and u['password_hash'] == password_hash), None)

        if user:
            session['user_id'] = user['id']
            session['role'] = user['role']
            session['name'] = user['name']
            flash(f"登入成功！歡迎 {user['name']}", "success")
            
            return redirect(url_for('main.index'))
        else:
            flash("Email 或密碼錯誤", "error")
            return redirect(url_for('auth.login'))

    return render_template('auth/login.html')

@auth_bp.route('/logout')
def logout():
    """
    登出會員
    """
    session.clear()
    flash("已成功登出", "success")
    return redirect(url_for('main.index'))
