import cv2
import requests
import json
import numpy as np

# Cấu hình
SERVER_URL = "http://127.0.0.1:5000"
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def main():
    # 1. Tải dữ liệu chủ xe từ Server về
    print("--- Đang tải dữ liệu chủ xe từ Server... ---")
    try:
        response = requests.get(f"{SERVER_URL}/get_owners")
        known_owners = response.json()
        print(f"Đã tải {len(known_owners)} chủ xe.")
    except:
        print("Không thể kết nối Server!")
        return

    cap = cv2.VideoCapture(0)

    while cap.isOpened():
        success, frame = cap.read()
        if not success: break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)

        for (x, y, w, h) in faces:
            # Vẽ khung nhận diện
            color = (0, 0, 255) # Mặc định là Đỏ (Người lạ)
            name = "Unknown - Unauthorized!"

            # Logic so khớp đơn giản cho chuyên đề: 
            # So sánh kích thước khung mặt (w, h) với sai số 20%
            for owner in known_owners:
                o_x, o_y, o_w, o_h = owner['vector']
                if abs(w - o_w) < (o_w * 0.2) and abs(h - o_h) < (o_h * 0.2):
                    color = (0, 255, 0) # Xanh lá (Chủ xe)
                    name = f"Welcome, {owner['name']}!"
                    break
            
            # Gửi cảnh báo nếu là người lạ (Chỉ gửi 1 lần khi phát hiện)
            if name == "Unknown - Unauthorized!":
                 # Gửi cảnh báo về server
                 requests.post(f"{SERVER_URL}/alert", json={"status": "Intruder Detected", "image": "alert.jpg"})

            cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
            cv2.putText(frame, name, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

        cv2.imshow('ITS FaceID - Security System', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'): break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()