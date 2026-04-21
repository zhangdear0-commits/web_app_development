from flask import Blueprint

main_bp = Blueprint('main', __name__)

@main_bp.route('/', methods=['GET'])
def index():
    """
    首頁活動列表
    取得並顯示所有開放中活動 (呼叫 Event.get_all)
    輸出: 渲染 home.html
    """
    pass
