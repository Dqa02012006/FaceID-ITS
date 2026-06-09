import cv2
import requests
import json

# Tải bộ nhận diện khuôn mặt mặc định của OpenCV (không cần Mediapipe)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

SERVER_URL = "http://127.0.0.1:5000/register"

def get_face_features(frame):
    """Trích xuất tọa độ khuôn mặt làm đặc trưng giả lập"""
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Phát hiện khuôn mặt
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    
    if len(faces) > 0:
        # Lấy khuôn mặt đầu tiên: x, y là tọa độ, w, h là kích thước
        x, y, w, h = faces[0]
        # Tạo một vector đơn giản để gửi về Server
        return [float(x), float(y), float(w), float(h)]
    return None

def main():
    cap = cv2.VideoCapture(0)
    owner_name = input("Nhập tên chủ xe để đăng ký FaceID: ")

    print(f"Đang mở camera... Nhấn 'S' để lưu, 'Q' để thoát.")

    while cap.isOpened():
        success, frame = cap.read()
        if not success: break

        # Vẽ khung xanh quanh mặt để biết AI đang chạy
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        cv2.putText(frame, f"User: {owner_name} | 'S' to Save", (10, 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.imshow('ITS FaceID - Register (OpenCV Mode)', frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('s'):
            vector = get_face_features(frame)
            if vector:
                payload = {"name": owner_name, "vector": vector}
                try:
                    res = requests.post(SERVER_URL, json=payload)
                    if res.status_code == 201:
                        print("✅ Đăng ký thành công!")
                        break
                    else:
                        print(f"❌ Lỗi: {res.text}")
                except Exception as e:
                    print(f"❌ Không kết nối được Server: {e}")
            else:
                print("⚠️ Không tìm thấy mặt!")

        elif key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()