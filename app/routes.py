from flask import Blueprint, request, jsonify, render_template
from .models import db, Owner, AlertLog
import json

# Khởi tạo Blueprint
app_routes = Blueprint('app_routes', __name__)

# --- CẬP NHẬT: TRẢ VỀ GIAO DIỆN WEB THAY VÌ JSON ---
@app_routes.route('/')
def dashboard():
    try:
        # Lấy danh sách chủ xe mới nhất
        owners_raw = Owner.query.order_by(Owner.id.desc()).all()
        alerts = AlertLog.query.order_by(AlertLog.timestamp.desc()).all()
        
        formatted_owners = []
        for owner in owners_raw:
            formatted_owners.append({
                "id": owner.id, # Giữ ID để hiển thị dạng #ID công khai
                "name": owner.name
            })
            
        return render_template(
            "dashboard.html",
            owners=formatted_owners,
            alerts=alerts,
            total_owners=len(owners_raw),
            total_alerts=len(alerts)
        )
    except Exception as e:
        return f"Lỗi hiển thị Dashboard: {str(e)}", 500

# 1. API Đăng ký chủ xe (Giữ nguyên)
@app_routes.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        if not data: return jsonify({"error": "Không nhận được dữ liệu"}), 400
            
        name = data.get('name')
        vector = data.get('vector') 
        
        if not name or not vector: return jsonify({"error": "Thiếu tên hoặc dữ liệu"}), 400
        if Owner.query.filter_by(name=name).first(): return jsonify({"error": "Tên chủ xe đã tồn tại"}), 409

        new_owner = Owner(name=name, face_vector=json.dumps(vector))
        db.session.add(new_owner)
        db.session.commit()
        return jsonify({"message": f"Đã đăng ký thành công chủ xe: {name}"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 2. API Lấy danh sách khuôn mặt (Giữ nguyên)
@app_routes.route('/get_owners', methods=['GET'])
def get_owners():
    try:
        owners = Owner.query.all()
        output = [{"id": o.id, "name": o.name, "vector": json.loads(o.face_vector)} for o in owners]
        return jsonify(output), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 3. API Nhận cảnh báo xâm nhập (Giữ nguyên logic của bạn)
@app_routes.route('/alert', methods=['POST'])
def receive_alert():
    try:
        data = request.get_json()
        if not data: return jsonify({"error": "Không có dữ liệu cảnh báo"}), 400

        status = data.get('status', 'Unauthorized Access')
        image_path = data.get('image', 'no_image.jpg')
        
        new_alert = AlertLog(status=status, image_path=image_path)
        db.session.add(new_alert)
        db.session.commit()
        
        print(f"\n[!!!] CẢNH BÁO AN NINH: {status}")
        return jsonify({"message": "Cảnh báo đã được hệ thống ghi nhận"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500