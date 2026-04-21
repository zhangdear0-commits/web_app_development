from flask import Blueprint

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    註冊會員
    GET: 渲染 register.html 表單
    POST: 接收註冊資料、驗證並建立 User、重導回到登入頁
    """
    pass

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    登入會員
    GET: 渲染 login.html 表單
    POST: 接收登入提交、驗證信箱與密碼、寫入 session 並導向首頁
    """
    pass
