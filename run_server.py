import sys
import os

# Thêm dòng này để đảm bảo Python tìm thấy thư mục hiện tại
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask
from app.models import db
from app.routes import app_routes

app = Flask(__name__)

# Cấu hình Database SQLite
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data', 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Đăng ký routes
app.register_blueprint(app_routes)

if __name__ == '__main__':
    with app.app_context():
        # Tạo folder data nếu chưa có
        if not os.path.exists('data'):
            os.makedirs('data')
        db.create_all() # Tạo file database.db
    
    app.run(debug=True, port=5000)