import cv2
import numpy as np
import requests
import os

SERVER_URL = "http://127.0.0.1:5000/register"
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Khởi tạo thuật toán LBPH của OpenCV
recognizer = cv2.face.LBPHFaceRecognizer_create()

def main():
    print("=== HỆ THỐNG ĐĂNG KÝ FACEID CHỦ XE (LBPH) ===")
    owner_name = input("Nhập tên chủ xe: ")
    
    # ID dùng để gắn nhãn khuôn mặt trong mô hình AI (phải là số nguyên)
    try:
        face_id = int(input("Nhập ID chủ xe (chỉ dùng số nguyên, ví dụ: 1): "))
    except:
        print("ID không hợp lệ, tự động gán ID = 1")
        face_id = 1

    print("\n[INFO] Đang mở camera. Hãy nhìn vào ống kính và xoay nhẹ đầu...")
    cap = cv2.VideoCapture(0)

    face_samples = []
    ids = []
    count = 0

    while True:
        ret, frame = cap.read()
        if not ret: break
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
            
            # Cắt khuôn mặt và đưa vào mảng huấn luyện
            face_samples.append(gray[y:y+h, x:x+w])
            ids.append(face_id)
            count += 1
            
            cv2.putText(frame, f"Dang quet du lieu... {count}/50", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)

        cv2.imshow('ITS FaceID - Thu thap du lieu', frame)

        # Dừng sau khi thu thập đủ 50 frame ảnh
        if count >= 50:
            break
        if cv2.waitKey(100) & 0xFF == 27: # Nhấn ESC để thoát sớm
            break

    cap.release()
    cv2.destroyAllWindows()

    if count > 0:
        print("\n[INFO] Đang huấn luyện AI mô hình LBPH. Vui lòng đợi...")
        # Bắt đầu Train thuật toán
        recognizer.train(face_samples, np.array(ids))
        
        # Xuất ra file mô hình "não bộ"
        recognizer.write('trainer.yml')
        print("[INFO] Huấn luyện thành công! Đã sinh ra file 'trainer.yml'.")

        # Đồng bộ thông tin lên Web Dashboard của Server
        # Truyền mảng [face_id, 0, 0, 0] để Server không bị lỗi cấu trúc dữ liệu cũ
        payload = {"name": owner_name, "vector": [face_id, 0, 0, 0]}
        try:
            res = requests.post(SERVER_URL, json=payload)
            if res.status_code == 201:
                print("✅ Đã đồng bộ dữ liệu với Máy chủ Trung tâm!")
        except:
            print("⚠️ Cảnh báo: Huấn luyện Offline xong nhưng không kết nối được Server.")
    else:
        print("\n[ERROR] Không quét được khuôn mặt nào.")

if __name__ == "__main__":
    main()