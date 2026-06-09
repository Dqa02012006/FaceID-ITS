import json
import numpy as np

def encode_vector(vector_ndarray):
    """Chuyển mảng Numpy thành chuỗi JSON để lưu vào DB"""
    return json.dumps(vector_ndarray.tolist())

def decode_vector(vector_string):
    """Chuyển chuỗi JSON từ DB ngược lại thành mảng Numpy để AI so sánh"""
    return np.array(json.loads(vector_string))