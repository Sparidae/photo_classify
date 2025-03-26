import os
from core import query_vision_model
from core.report_generator import generate_report

def main():
    """命令行入口函数"""
    # 获取data/raw文件夹下的所有图片文件
    raw_dir = "data/raw"
    image_files = [f for f in os.listdir(raw_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp'))]
    
    if not image_files:
        print("错误：data/raw文件夹中没有找到图片文件")
        return
    
    # 自定义提示词（可选）
    custom_prompt = input("请输入提示词(直接回车使用默认提示): ")
    if not custom_prompt:
        custom_prompt = "请用中文尽可能详细的描述这张图片"
    
    # 用于存储图片路径和回复
    processed_images = []
    responses = []
    
    # 遍历所有图片文件
    for idx, image_file in enumerate(image_files):
        image_path = os.path.join(raw_dir, image_file)
        print(f"\n处理第 {idx + 1}/{len(image_files)} 张图片: {image_file}")
        
        # 调用VLM接口
        print("正在处理请求...")
        response = query_vision_model(image_path, custom_prompt)
        
        # 显示结果
        print("\n模型回复:")
        print(response)
        print("-" * 50)  # 添加分隔线，使输出更清晰
        
        # 记录处理结果
        processed_images.append(image_path)
        responses.append(response)
    
    # 生成HTML报告
    print("\n正在生成HTML报告...")
    report_path = generate_report(processed_images, responses)
    print(f"报告已生成: {os.path.abspath(report_path)}")

if __name__ == "__main__":
    main() 