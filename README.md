# 🚗 ITS FaceID Security System
**Hệ thống Giám sát An ninh và Bãi đỗ xe thông minh (V2I) tích hợp Edge AI**

Dự án ứng dụng công nghệ nhận diện khuôn mặt (Local Binary Patterns Histograms - LBPH) xử lý trực tiếp tại trạm biên (Edge AI) để giảm độ trễ, kết hợp với Máy chủ Trung tâm (Flask) để quản lý và cảnh báo xâm nhập theo thời gian thực.

## 🛠️ PHẦN 1: CÀI ĐẶT MÔI TRƯỜNG (BẮT BUỘC)

Để hệ thống chạy ổn định và không xung đột với các dự án khác trên máy, bạn cần tạo một môi trường ảo (Virtual Environment) trước khi chạy code.

Bước 1: Tạo và kích hoạt môi trường ảo:
Mở Terminal/Command Prompt tại thư mục dự án và chạy các lệnh sau tùy theo hệ điều hành:
**Đối với Windows:**
bash
python -m venv .venv
.venv\Scripts\activate
Đối với MacOS/Linux:
python3 -m venv .venv
source .venv/bin/activate

Bước 2: Cài đặt thư viện
Sau khi kích hoạt môi trường ảo, tiến hành cài đặt các thư viện cần thiết:
"pip install Flask Flask-SQLAlchemy opencv-python opencv-contrib-python requests"
PHẦN 2: TRÌNH TỰ VẬN HÀNH HỆ THỐNG:
Vui lòng chạy tuần tự các bước dưới đây ở các cửa sổ Terminal khác nhau (nhớ kích hoạt lại .venv cho mỗi Terminal mới).
1.Khởi động Máy chủ Trung tâm (Server Backend)
python run_server.py
Mở trình duyệt và truy cập http://127.0.0.1:5000/ để xem bảng điều khiển giám sát Real-time.
2.Đăng ký FaceID & Huấn luyện AI (Trên Xe)
python run_vehicle.py
Nhập Tên và ID (dùng số, ví dụ: 1) khi được yêu cầu.
Nhìn thẳng vào Camera và xoay nhẹ đầu. Hệ thống sẽ tự động chụp 50 bức ảnh và tiến hành huấn luyện.
Sau khi có thông báo thành công, file trainer.yml sẽ được sinh ra và dữ liệu được đồng bộ lên Web Dashboard.
3.Chạy thử nghiệm:
Hệ thống An ninh Chống trộm trên xe:
python run_recognition.py
Trạm kiểm soát Bãi đỗ xe thông minh (V2I)
python run_smart_parking.py

📁 CẤU TRÚC THƯ MỤC CHÍNH
app/: Nơi chứa mã nguồn khởi tạo Server, Database Models và các API Routes.
templates/ & static/: Giao diện và hiệu ứng của Web Dashboard.
run_server.py: Kịch bản khởi chạy máy chủ Flask.
run_vehicle.py: Kịch bản thu thập dữ liệu & Train AI.
run_recognition.py: Kịch bản nhận diện an ninh cục bộ.
run_smart_parking.py: Kịch bản giả lập hạ tầng bãi đỗ.
