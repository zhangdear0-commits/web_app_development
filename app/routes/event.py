from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from app.models.event import Event
from app.models.registration import Registration
import datetime
import uuid

event_bp = Blueprint('event', __name__)

@event_bp.route('/events/create', methods=['GET', 'POST'])
def create_event():
    """
    建立新活動 (主辦方專用)
    """
    if 'user_id' not in session or session.get('role') != 'organizer':
        flash("請先以主辦方身分登入", "error")
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        title = request.form.get('title')
        capacity = request.form.get('capacity')
        location = request.form.get('location')
        start_time = request.form.get('start_time')
        end_time = request.form.get('end_time')

        if not all([title, capacity, location, start_time, end_time]):
            flash("請填寫所有標示必填的活動資訊", "error")
            return redirect(url_for('event.create_event'))

        try:
            capacity = int(capacity)
        except ValueError:
            flash("名額限制必須為數字", "error")
            return redirect(url_for('event.create_event'))

        data = {
            'organizer_id': session['user_id'],
            'title': title,
            'description': request.form.get('description', ''),
            'capacity': capacity,
            'location': location,
            'start_time': start_time,
            'end_time': end_time,
            'custom_form_schema': request.form.get('custom_form_schema', '{}'),
            'created_at': datetime.datetime.now().isoformat()
        }

        event_id = Event.create(data)
        if event_id:
            flash("活動建立成功！", "success")
            return redirect(url_for('event.event_detail', event_id=event_id))
        else:
            flash("建立活動時發生錯誤", "error")
            return redirect(url_for('event.create_event'))

    return render_template('events/create.html')

@event_bp.route('/events/<int:event_id>', methods=['GET'])
def event_detail(event_id):
    """
    活動詳情預覽
    """
    event = Event.get_by_id(event_id)
    if not event:
        flash("找不到該活動", "error")
        return redirect(url_for('main.index'))
    return render_template('events/detail.html', event=event)

@event_bp.route('/events/<int:event_id>/register', methods=['GET', 'POST'])
def register_event(event_id):
    """
    活動報名 (參加者專用)
    """
    if 'user_id' not in session:
        flash("請先登入後再報名", "warning")
        return redirect(url_for('auth.login'))

    event = Event.get_by_id(event_id)
    if not event:
        flash("找不到該活動", "error")
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        # 簡單的名額判斷機制
        all_regs = Registration.get_all()
        current_regs = [r for r in all_regs if r['event_id'] == event_id and r['status'] in ('success', 'checked_in')]
        
        status = 'success'
        if len(current_regs) >= event['capacity']:
            status = 'waitlist'
            
        qr_code_token = str(uuid.uuid4())
        
        data = {
            'event_id': event_id,
            'user_id': session['user_id'],
            'status': status,
            'custom_form_data': request.form.get('custom_form_data', '{}'),
            'qr_code_token': qr_code_token,
            'created_at': datetime.datetime.now().isoformat()
        }
        
        reg_id = Registration.create(data)
        if reg_id:
            if status == 'success':
                flash("報名成功！專屬 QR 票券已產生", "success")
            else:
                flash("名額已滿，您已自動進入候補名單", "warning")
            return redirect(url_for('event.event_detail', event_id=event_id))
        else:
            flash("報名發生錯誤，請稍後再試", "error")
            return redirect(url_for('event.register_event', event_id=event_id))

    return render_template('events/register.html', event=event)

@event_bp.route('/dashboard/<int:event_id>', methods=['GET'])
def event_dashboard(event_id):
    """
    活動管理儀表板 (主辦方專用)
    """
    if 'user_id' not in session or session.get('role') != 'organizer':
        flash("無權限存取", "error")
        return redirect(url_for('main.index'))

    event = Event.get_by_id(event_id)
    if not event or event['organizer_id'] != session['user_id']:
        flash("找不到活動或您沒有管理權限", "error")
        return redirect(url_for('main.index'))

    all_regs = Registration.get_all()
    registrations = [r for r in all_regs if r['event_id'] == event_id]
    
    return render_template('events/dashboard.html', event=event, registrations=registrations)

@event_bp.route('/events/<int:event_id>/export', methods=['GET'])
def export_registrations(event_id):
    """
    匯出活動報名名單為 Excel 檔案 (範例)
    """
    if 'user_id' not in session or session.get('role') != 'organizer':
        flash("無權限存取", "error")
        return redirect(url_for('main.index'))
    
    # MVC 實作省略匯出 library，以 flash 提示替代
    flash("名單匯出功能已被觸發（測試用）", "success")
    return redirect(url_for('event.event_dashboard', event_id=event_id))

@event_bp.route('/events/<int:event_id>/check-in', methods=['POST'])
def event_checkin(event_id):
    """
    QR Code 現場簽到 API
    """
    token = request.json.get('qr_code_token') if request.is_json else request.form.get('qr_code_token')
    if not token:
        return jsonify({'error': 'Missing QR code token'}), 400

    all_regs = Registration.get_all()
    target_reg = next((r for r in all_regs if r['event_id'] == event_id and r['qr_code_token'] == token), None)
    
    if not target_reg:
        return jsonify({'error': '無效的票券'}), 404
        
    if target_reg['status'] == 'checked_in':
        return jsonify({'message': '票券已使用並簽到'}), 200
        
    if target_reg['status'] in ('waitlist', 'cancelled'):
        return jsonify({'error': '不在正取成功名單內，無法簽到'}), 400
        
    # 如果找到了，更新這筆 Registration的屬性
    success = Registration.update(target_reg['id'], {'status': 'checked_in'})
    if success:
        return jsonify({'message': '簽到成功'}), 200
    else:
        return jsonify({'error': '伺服器內部錯誤'}), 500
