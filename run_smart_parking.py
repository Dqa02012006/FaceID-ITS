import cv2
import requests
import time

# Cấu hình kết nối tới Máy chủ trung tâm (Server Backend)
SERVER_URL = "http://127.0.0.1:5000"
# Gọi trực tiếp bộ lọc khuôn mặt có sẵn của OpenCV
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def main():
    print("==================================================")
    print("🚧 HỆ THỐNG SMART PARKING (V2I) ĐANG KHỞI ĐỘNG 🚧")
    print("==================================================")
    
    # Đồng bộ dữ liệu từ Server
    try:
        response = requests.get(f"{SERVER_URL}/get_owners")
        known_owners = response.json()
        print(f"✅ Đã đồng bộ danh sách {len(known_owners)} chủ xe từ hệ thống trung tâm.")
    except Exception as e:
        print("❌ Lỗi kết nối Server! Vui lòng bật run_server.py trước.")
        return

    # Khởi động camera của bãi xe (Barrier Camera)
    cap = cv2.VideoCapture(0)
    
    # Biến kiểm soát trạng thái cổng (tránh cổng mở/đóng liên tục gây lỗi)
    gate_open_time = 0
    GATE_HOLD_SECONDS = 5 # Giữ cổng mở trong 5 giây cho xe đi qua

    while cap.isOpened():
        success, frame = cap.read()
        if not success: break

        current_time = time.time()
        gate_status_text = "TRANG THAI: DONG (CLOSED)"
        gate_color = (0, 0, 255) # Đỏ (Đóng)

        # Nếu cổng đang trong thời gian mở
        if current_time - gate_open_time < GATE_HOLD_SECONDS:
            gate_status_text = "TRANG THAI: DANG MO (OPENED) - MOI XE QUA"
            gate_color = (255, 255, 0) # Xanh lơ (Đang mở)
        else:
            # Chỉ quét khuôn mặt khi cổng đang đóng
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.1, 4)

            for (x, y, w, h) in faces:
                is_authorized = False
                driver_name = "Khach vang lai"

                # Đối chiếu tọa độ vector với DB
                for owner in known_owners:
                    o_x, o_y, o_w, o_h = owner['vector']
                    # Sai số cho phép 20% khoảng cách khung mặt
                    if abs(w - o_w) < (o_w * 0.2) and abs(h - o_h) < (o_h * 0.2):
                        is_authorized = True
                        driver_name = owner['name']
                        break
                
                # Hiển thị khung quét
                if is_authorized:
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                    cv2.putText(frame, f"V2I Matched: {driver_name}", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                    
                    # Phát lệnh mở cổng bãi xe
                    print(f"[V2I] Nhận diện thành công chủ xe: {driver_name}. ĐANG MỞ BARRIER...")
                    gate_open_time = current_time # Kích hoạt bộ đếm thời gian mở cổng
                else:
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
                    cv2.putText(frame, "Khong xac dinh", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

        # Vẽ bảng LED trạng thái cổng giả lập lên màn hình Camera
        cv2.rectangle(frame, (10, 10), (500, 50), (0,0,0), -1)
        cv2.putText(frame, gate_status_text, (20, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.7, gate_color, 2)

        cv2.imshow('Smart Parking Gate - V2I Simulation', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'): break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()