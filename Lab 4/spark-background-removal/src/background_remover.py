import numpy as np
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import os

BG_COLOR = (192, 192, 192)  # gray
MASK_COLOR = (255, 255, 255)  # white

# Sử dụng đường dẫn tuyệt đối hoặc tương đối chính xác
# Giả sử file .tflite nằm trong thư mục models ngang hàng với src
MODEL_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../models/selfie_segmenter.tflite"))

def get_segmenter():
    # Hàm này khởi tạo segmenter. Việc đặt trong hàm giúp tránh lỗi pickle của Spark
    base_options = python.BaseOptions(model_asset_path=MODEL_PATH)
    options = vision.ImageSegmenterOptions(base_options=base_options, output_category_mask=True)
    return vision.ImageSegmenter.create_from_options(options)

def remove_background(frame: np.ndarray) -> np.ndarray:
    # Tạo segmenter mới cho mỗi lần gọi (hoặc mỗi partition) để an toàn trên Spark
    segmenter = get_segmenter()
    
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
    segmentation_result = segmenter.segment(mp_image)
    category_mask = segmentation_result.category_mask

    image_data = mp_image.numpy_view()
    fg_image = np.zeros(image_data.shape, dtype=np.uint8)
    fg_image[:] = MASK_COLOR
    bg_image = np.zeros(image_data.shape, dtype=np.uint8)
    bg_image[:] = BG_COLOR
    condition = np.stack((category_mask.numpy_view(),) * 3, axis=-1) > 0.2
    output_frame = np.where(condition, bg_image, image_data)
    
    segmenter.close() # Giải phóng tài nguyên
    return output_frame