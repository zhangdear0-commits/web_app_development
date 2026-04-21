from flask import Blueprint

event_bp = Blueprint('event', __name__)

@event_bp.route('/events/create', methods=['GET', 'POST'])
def create_event():
    """
    建立新活動 (主辦方專用)
    GET: 渲染 create.html 表單，包含自定義欄位編輯器
    POST: 接收表單並建立 Event 資料錄，重導向至活動詳情頁
    """
    pass

@event_bp.route('/events/<int:event_id>', methods=['GET'])
def event_detail(event_id):
    """
    活動詳情預覽
    依據 event_id 查詢 Event 資料，渲染 detail.html
    """
    pass

@event_bp.route('/events/<int:event_id>/register', methods=['GET', 'POST'])
def register_event(event_id):
    """
    活動報名 (參加者專用)
    GET: 查詢 Event 的自訂欄位 Schema，渲染動態報名表單 (register.html)
    POST: 接收報名資料、執行並行防護與扣除名額或進入候補、產生 QR Token 並觸發 Email、重導回報名結果頁
    """
    pass

@event_bp.route('/dashboard/<int:event_id>', methods=['GET'])
def event_dashboard(event_id):
    """
    活動管理儀表板 (主辦方專用)
    查詢特定 Event 及其所有 Registrations 來產生報名圖表資料與名單，渲染 dashboard.html
    """
    pass

@event_bp.route('/events/<int:event_id>/export', methods=['GET'])
def export_registrations(event_id):
    """
    匯出活動報名名單為 Excel 檔案
    讀取所有該活動的 Registrations 並轉換為 downloadable CSV/Excel
    """
    pass

@event_bp.route('/events/<int:event_id>/check-in', methods=['POST'])
def event_checkin(event_id):
    """
    QR Code 現場簽到 (主辦方針對票券 QR Code 的 API endpoint)
    接收包含 QR Code Token 的 Payload，驗證與更新 Registration 的狀態
    回傳 JSON 結果
    """
    pass
