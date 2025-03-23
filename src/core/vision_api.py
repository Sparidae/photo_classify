import os
from dotenv import load_dotenv
from openai import OpenAI
from .image_utils import convert_image_to_webp_base64

# 加载环境变量
load_dotenv()

# 初始化OpenAI客户端
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_API_BASE", "https://api.siliconflow.cn/v1")
)

# 获取模型名称
model_name = os.getenv("OPENAI_MODEL", "deepseek-ai/deepseek-vl2")

def query_vision_model(image_path, prompt="请描述这张图片", detail="low"):
    """调用VLM接口并获取回复
    
    Args:
        image_path (str): 图片文件路径
        prompt (str): 提示词
        detail (str): 处理详细程度，可选值为 "high" 或 "low"，默认为 "low"
        
    Returns:
        str: 模型的回复内容
    """
    if detail not in ["high", "low"]:
        raise ValueError("detail参数必须是 'high' 或 'low'")
    
    # 编码图片
    base64_image = convert_image_to_webp_base64(image_path)
    
    try:
        # 使用OpenAI客户端发送请求
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}",
                                "detail": detail,
                            }
                        }
                    ]
                }
            ],
            max_tokens=1024,
            temperature=0.7,
            top_p=0.7,
            frequency_penalty=0.0,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"错误: {str(e)}" 