import os
from datetime import datetime
import base64
from pathlib import Path
from PIL import Image
import io

def generate_report(image_files, responses, output_dir="data/reports"):
    """生成包含图片和模型回复的HTML报告
    
    Args:
        image_files (list): 处理过的图片文件路径列表
        responses (list): 每张图片对应的模型回复
        output_dir (str): 报告输出目录
        
    Returns:
        str: 生成的报告文件路径
    """
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)
    
    # 创建报告文件名（使用当前时间戳）
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_filename = f"report_{timestamp}.html"
    report_path = os.path.join(output_dir, report_filename)
    
    # 创建HTML内容
    html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>图像分析报告 - {timestamp}</title>
    <style>
        body {{
            font-family: "Microsoft YaHei", "Helvetica Neue", Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }}
        h1 {{
            color: #2c3e50;
            text-align: center;
            border-bottom: 2px solid #eee;
            padding-bottom: 10px;
        }}
        .report-item {{
            display: flex;
            margin-bottom: 30px;
            border: 1px solid #ddd;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }}
        .image-container {{
            flex: 1;
            padding: 15px;
            display: flex;
            align-items: center;
            justify-content: center;
            background-color: #f9f9f9;
            border-right: 1px solid #eee;
        }}
        .image-container img {{
            max-width: 100%;
            max-height: 400px;
            object-fit: contain;
        }}
        .response-container {{
            flex: 1;
            padding: 15px 20px;
        }}
        .filename {{
            font-weight: bold;
            color: #2980b9;
            margin-bottom: 10px;
        }}
        .response {{
            white-space: pre-wrap;
            line-height: 1.7;
        }}
        .footer {{
            text-align: center;
            font-size: 0.9em;
            color: #7f8c8d;
            margin-top: 30px;
            border-top: 1px solid #eee;
            padding-top: 15px;
        }}
    </style>
</head>
<body>
    <h1>图像分析报告</h1>
"""

    # 添加每个图片和对应回复
    for i in range(len(image_files)):
        image_path = image_files[i]
        response_text = responses[i]
        filename = os.path.basename(image_path)
        
        # 获取图片的base64编码用于内嵌到HTML中
        try:
            with Image.open(image_path) as img:
                # 调整图片大小如果太大
                max_size = (800, 800)
                if img.width > max_size[0] or img.height > max_size[1]:
                    img.thumbnail(max_size, Image.LANCZOS)
                
                # 转换为base64
                buffer = io.BytesIO()
                img.save(buffer, format='JPEG')
                img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
                img_data_uri = f"data:image/jpeg;base64,{img_base64}"
                
                # 添加到HTML中
                html_content += f"""
    <div class="report-item">
        <div class="image-container">
            <img src="{img_data_uri}" alt="图片 {i+1}">
        </div>
        <div class="response-container">
            <div class="filename">{filename}</div>
            <div class="response">{response_text}</div>
        </div>
    </div>
"""
        except Exception as e:
            html_content += f"""
    <div class="report-item">
        <div class="image-container">
            <div>无法加载图片: {filename}</div>
        </div>
        <div class="response-container">
            <div class="filename">{filename}</div>
            <div class="response">{response_text}</div>
        </div>
    </div>
"""
    
    # 添加页脚和结束标签
    html_content += f"""
    <div class="footer">
        <p>报告生成时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
        <p>共处理 {len(image_files)} 张图片</p>
    </div>
</body>
</html>
"""

    # 写入文件
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    return report_path 