import os
from src.core import query_vision_model

def main():
    # 获取data/raw文件夹下的所有图片文件
    raw_dir = "data/raw"
    image_files = [f for f in os.listdir(raw_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp'))]
    
    if not image_files:
        print("错误：data/raw文件夹中没有找到图片文件")
        return
    
    # 使用第一个图片文件
    idx = 1
    image_path = os.path.join(raw_dir, image_files[idx])
    print(f"使用图片: {image_files[idx]}")
    
    # 自定义提示词（可选）
    custom_prompt = input("请输入提示词(直接回车使用默认提示): ")
    if not custom_prompt:
        custom_prompt = "请描述这张图片"
    
    # 调用VLM接口
    print("正在处理请求...")
    response = query_vision_model(image_path, custom_prompt)
    
    # 显示结果
    print("\n模型回复:")
    print(response)

if __name__ == "__main__":
    main()
