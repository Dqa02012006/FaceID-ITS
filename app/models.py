from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Owner(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    # Lưu vector khuôn mặt dưới dạng chuỗi (String) hoặc Blob
    # Sau này khi dùng sẽ convert ngược lại thành mảng Numpy
    face_vector = db.Column(db.Text, nullable=False) 
    created_at = db.Column(db.DateTime, server_default=db.func.now())

class AlertLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(50)) # "Unauthorized Access" hoặc "Successful Login"
    image_path = db.Column(db.String(200)) # Đường dẫn ảnh kẻ gian chụp được
    timestamp = db.Column(db.DateTime, server_default=db.func.now())