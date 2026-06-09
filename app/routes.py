from flask import Blueprint, request, jsonify
from .models import db, Owner, AlertLog
import json

# Khởi tạo Blueprint
app_routes = Blueprint('app_routes', __name__)

@app_routes.route('/')
def index():
    return jsonify({
        "status": "online",
        "message": "Hệ thống Backend FaceID ITS đang hoạt động"
    })

# 1. API Đăng ký chủ xe (Gửi từ App hoặc thiết bị thiết lập)
@app_routes.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Không nhận được dữ liệu"}), 400
            
        name = data.get('name')
        vector = data.get('vector') # Đây là mảng 128 số thực
        
        if not name or not vector:
            return jsonify({"error": "Thiếu tên hoặc dữ liệu khuôn mặt"}), 400
        
        # Kiểm tra xem tên đã tồn tại chưa
        existing_owner = Owner.query.filter_by(name=name).first()
        if existing_owner:
            return jsonify({"error": "Tên chủ xe đã tồn tại"}), 409

        # Lưu vào Database (chuyển mảng vector thành chuỗi JSON)
        new_owner = Owner(name=name, face_vector=json.dumps(vector))
        db.session.add(new_owner)
        db.session.commit()
        
        return jsonify({"message": f"Đã đăng ký thành công chủ xe: {name}"}), 201
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 2. API Lấy danh sách khuôn mặt đã lưu (Để xe tải về so khớp offline)
@app_routes.route('/get_owners', methods=['GET'])
def get_owners():
    try:
        owners = Owner.query.all()
        output = []
        for owner in owners:
            output.append({
                "id": owner.id,
                "name": owner.name,
                "vector": json.loads(owner.face_vector) # Chuyển ngược từ chuỗi sang mảng
            })
        return jsonify(output), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 3. API Nhận cảnh báo xâm nhập (Gửi từ xe khi phát hiện trộm)
@app_routes.route('/alert', methods=['POST'])
def receive_alert():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Không có dữ liệu cảnh báo"}), 400

        status = data.get('status', 'Unauthorized Access')
        image_path = data.get('image', 'no_image.jpg')
        
        # Lưu nhật ký cảnh báo vào DB
        new_alert = AlertLog(status=status, image_path=image_path)
        db.session.add(new_alert)
        db.session.commit()
        
        # Log ra console của Server để theo dõi
        print(f"\n[!!!] CẢNH BÁO AN NINH: {status}")
        print(f"[!] Ảnh bằng chứng: {image_path}\n")
        
        return jsonify({"message": "Cảnh báo đã được hệ thống ghi nhận"}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 4. API Xem nhật ký cảnh báo (Dành cho App quản lý)
@app_routes.route('/logs', methods=['GET'])
def get_logs():
    logs = AlertLog.query.order_by(AlertLog.timestamp.desc()).all()
    output = []
    for log in logs:
        output.append({
            "id": log.id,
            "status": log.status,
            "image": log.image_path,
            "time": log.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        })
    return jsonify(output), 200