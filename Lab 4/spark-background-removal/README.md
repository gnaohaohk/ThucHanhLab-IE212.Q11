# Hệ Thống Xóa Phông Nền Sử Dụng Spark

Dự án này triển khai hệ thống xóa phông nền ảnh trực tuyến sử dụng Apache Spark và MediaPipe. Hệ thống thu thập các frame hình ảnh từ camera, xử lý để xóa phông nền, và truyền tải các frame đã được sửa đổi.

## Cấu Trúc Dự Án

```
spark-background-removal
├── src
│   ├── main.py               # Điểm khởi chạy cũ (Không sử dụng cho bài lab Spark)
│   ├── background_remover.py  # Chức năng xóa phông nền
│   ├── spark_streaming_job.py  # Job Spark để xử lý các frame (File chính)
│   └── utils
│       └── camera_producer.py  # Giả lập server camera
├── models
│   └── selfie_segmenter.tflite # Model TensorFlow Lite cho phân đoạn ảnh
├── requirements.txt           # Các thư viện phụ thuộc
├── .gitignore                 # Các file bị bỏ qua trong Git
└── README.md                  # Tài liệu dự án
```

## Hướng Dẫn Cài Đặt

1. **Clone Repository**

   ```bash
   git clone <link-repo-cua-ban>
   cd spark-background-removal
   ```

2. **Cài Đặt Thư Viện**
   Đảm bảo bạn đã cài đặt Python và pip. Sau đó, cài đặt các gói cần thiết:

   ```bash
   pip install -r requirements.txt
   ```

3. **Chạy Ứng Dụng**

   Bắt đầu server camera (Producer):
   Mở terminal thứ nhất:

   ```bash
   python src/utils/camera_producer.py
   ```

   Trong một terminal riêng biệt, chạy Spark Streaming job (Consumer):
   Mở terminal thứ hai:

   ```bash
   # KHÔNG chạy main.py, hãy chạy file này để đáp ứng yêu cầu dùng Spark
   python src/spark_streaming_job.py
   ```

## Sử Dụng

- Ứng dụng sẽ bắt đầu thu thập các frame từ server camera giả lập.
- Quá trình xóa phông nền sẽ được áp dụng cho từng frame sử dụng ngữ cảnh Spark.
- Các frame kết quả sẽ được lưu dưới dạng file ảnh trong thư mục `output_frames`.

## Đóng Góp

Đừng ngần ngại fork repository và gửi pull requests cho bất kỳ cải tiến hoặc sửa lỗi nào.

## Giấy Phép

Dự án này được cấp phép theo MIT License. Xem file LICENSE để biết thêm chi tiết.
