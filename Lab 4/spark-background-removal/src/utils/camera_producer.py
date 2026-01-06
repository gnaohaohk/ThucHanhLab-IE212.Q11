import socket
import cv2
import json
import base64
import time
import sys

HOST = 'localhost'
PORT = 6100

def start_camera_server():
    # 1. Khởi tạo Socket Server
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)
    print(f"Camera Server đang chờ kết nối tại {HOST}:{PORT}...")

    conn, addr = server_socket.accept()
    print(f"Spark đã kết nối từ: {addr}")

    # 2. Mở Camera
    cap = cv2.VideoCapture(0) # 0 là webcam mặc định
    
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # Resize ảnh nhỏ lại để gửi nhanh hơn (tùy chọn)
            frame = cv2.resize(frame, (640, 480))

            # 3. Encode ảnh sang JPEG -> Base64
            _, buffer = cv2.imencode('.jpg', frame)
            jpg_as_text = base64.b64encode(buffer).decode('utf-8')

            # 4. Tạo gói tin JSON
            # Spark socketTextStream đọc theo dòng, nên cần loại bỏ ký tự xuống dòng trong base64 nếu có
            payload = {
                "timestamp": time.time(),
                "image": jpg_as_text,
                "width": frame.shape[1],
                "height": frame.shape[0]
            }
            
            message = json.dumps(payload) + "\n" # Quan trọng: Phải có \n để Spark nhận biết hết 1 tin
            
            conn.sendall(message.encode('utf-8'))
            print("Đã gửi 1 frame...")
            time.sleep(0.1) # Giới hạn tốc độ gửi (khoảng 10 fps)

    except Exception as e:
        print(f"Lỗi: {e}")
    except KeyboardInterrupt:
        print("Dừng server.")
    finally:
        cap.release()
        conn.close()
        server_socket.close()

if __name__ == "__main__":
    start_camera_server()