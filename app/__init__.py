from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Khởi tạo đối tượng DB nhưng chưa gắn với app nào
db = SQLAlchemy()

def create_app():
    # Chỉ định rõ template và static nằm ở ngoài thư mục app/
    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    
    # Cấu hình SQLite tự động lưu vào thư mục instance/database.db
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    
    # Đăng ký Blueprint xử lý API và Giao diện
    from app.routes import main_bp
    app.register_blueprint(main_bp)
    
    return app