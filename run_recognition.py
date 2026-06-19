import cv2
import requests
import time

SERVER_URL = "http://127.0.0.1:5000"
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
recognizer = cv2.face.LBPHFaceRecognizer_create()

def main():
    # 1. Nạp mô hình AI đã huấn luyện
    try:
        recognizer.read('trainer.yml')
        print("[INFO] Đã nạp thành công mô hình FaceID (trainer.yml).")
    except:
        print("[ERROR] Không tìm thấy file trainer.yml. Chạy run_vehicle.py trước!")
        return

    # 2. Tải danh sách ID chủ xe từ Server
    print("--- Đang kết nối Server lấy danh sách chủ xe... ---")
    owner_dict = {}
    try:
        response = requests.get(f"{SERVER_URL}/get_owners")
        known_owners = response.json()
        for owner in known_owners:
            # Gỡ ID ra từ mảng vector giả lập lúc đăng ký
            face_id = int(owner['vector'][0])
            owner_dict[face_id] = owner['name']
        print(f"✅ Đã tải dữ liệu {len(known_owners)} chủ xe hợp pháp.")
    except:
        print("⚠️ Không kết nối được Server. Chạy Offline Mode.")

    cap = cv2.VideoCapture(0)
    last_alert_time = 0
    cooldown_seconds = 5 # Thời gian chờ giữa 2 lần gửi báo động liên tiếp

    print("\n[INFO] HỆ THỐNG AN NINH ĐANG TRỰC CHIẾN...")
    while cap.isOpened():
        start_time = time.time()
        
        success, frame = cap.read()
        if not success: break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.2, 5)

        for (x, y, w, h) in faces:
            # Cắt lấy riêng vùng khuôn mặt
            face_roi = gray[y:y+h, x:x+w]
            
            # Đưa vào LBPH dự đoán
            id_, confidence = recognizer.predict(face_roi)

            # NGƯỠNG AN TOÀN (Confidence < 65 là chủ xe, >= 65 là kẻ gian)
            # Bạn có thể tinh chỉnh số 65 này. Nếu nhận sai chủ xe thành kẻ gian, hãy tăng nó lên 75.
            if confidence < 65:
                color = (0, 255, 0)
                name = owner_dict.get(id_, f"User-{id_}")
                match_text = f"Welcome, {name}!"
            else:
                color = (0, 0, 255)
                name = "Unknown"
                match_text = "KE GIAN XAM NHAP!"
                
                # Gửi báo động lên Server
                current_time = time.time()
                if current_time - last_alert_time > cooldown_seconds:
                     print(f"🚨 Đột nhập (Mức độ khác biệt: {confidence:.0f}) -> Đang báo về Server...")
                     try:
                         requests.post(f"{SERVER_URL}/alert", json={"status": "⚠️ Kẻ gian xâm nhập"})
                     except:
                         pass
                     last_alert_time = current_time 
                     
            cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
            cv2.putText(frame, match_text, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

        # Benchmark đo độ trễ API
        latency = time.time() - start_time
        if len(faces) > 0:
            print(f"[Metrics] Latency: {latency:.4f}s - Kẻ gian hay Chủ: {name}")

        cv2.imshow('ITS FaceID - Security System (LBPH Mode)', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'): break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()