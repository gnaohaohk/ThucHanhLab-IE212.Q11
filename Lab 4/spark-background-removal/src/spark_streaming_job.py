from pyspark import SparkContext
from pyspark.streaming import StreamingContext
import numpy as np
import json
import base64
import cv2
import os
import uuid
from background_remover import remove_background

# Tạo thư mục output nếu chưa có
OUTPUT_DIR = "output_frames"
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

def process_partition(iter):
    # Hàm này chạy trên các worker (hoặc local thread)
    for record in iter:
        try:
            if not record: continue
            
            # 1. Parse JSON
            data = json.loads(record)
            b64_string = data['image']
            
            # 2. Decode Base64 -> Image
            img_bytes = base64.b64decode(b64_string)
            nparr = np.frombuffer(img_bytes, np.uint8)
            frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
            if frame is None: continue

            # 3. Xóa phông nền
            # Lưu ý: remove_background đã được sửa để khởi tạo model bên trong
            output_frame = remove_background(frame)
            
            # 4. Lưu ảnh kết quả
            filename = os.path.join(OUTPUT_DIR, f"frame_{data['timestamp']}_{uuid.uuid4().hex[:4]}.jpg")
            cv2.imwrite(filename, output_frame)
            print(f"Đã lưu: {filename}")
            
        except Exception as e:
            print(f"Lỗi xử lý frame: {e}")

def main():
    # Khởi tạo Spark Context
    sc = SparkContext(appName="BackgroundRemovalStreaming", master="local[2]")
    sc.setLogLevel("ERROR") # Giảm bớt log rác
    
    # Batch interval 1 giây
    ssc = StreamingContext(sc, 1)

    # Kết nối đến Camera Server
    lines = ssc.socketTextStream("localhost", 6100)

    # Xử lý từng RDD trong DStream
    lines.foreachRDD(lambda rdd: rdd.foreachPartition(process_partition))

    print("Spark Streaming đang chạy...")
    ssc.start()
    ssc.awaitTermination()

if __name__ == "__main__":
    main()