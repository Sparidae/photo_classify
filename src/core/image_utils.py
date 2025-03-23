import base64
from PIL import Image
import io

def convert_image_to_webp_base64(input_image_path):
    """将图片转换为webp格式的base64编码
    
    Args:
        input_image_path (str): 输入图片的路径
        
    Returns:
        str: base64编码的图片数据，如果转换失败则返回None
    """
    try:
        with Image.open(input_image_path) as img:
            byte_arr = io.BytesIO()
            img.save(byte_arr, format='webp')
            byte_arr = byte_arr.getvalue()
            base64_str = base64.b64encode(byte_arr).decode('utf-8')
            return base64_str
    except IOError:
        print(f"Error: Unable to open or convert the image {input_image_path}")
        return None 