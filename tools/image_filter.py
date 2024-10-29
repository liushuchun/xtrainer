import os
from PIL import Image, UnidentifiedImageError
import imquality.brisque as brisque

def delete_unidentified_small_or_low_quality_images(folders):
    for folder_path in folders:
        print(f"正在处理文件夹: {folder_path}")
        # 使用 os.walk 遍历所有子文件夹和文件
        for root, _, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    # 尝试打开文件
                    with Image.open(file_path) as img:
                        img.verify()  # 验证文件是否为有效的图像
                        
                    # 重新打开图像以获取大小和质量（verify不会加载图像尺寸）
                    with Image.open(file_path) as img:
                        width, height = img.size
                        # 检查分辨率是否小于512x512
                        if width < 512 or height < 512:
                            print(f"删除分辨率低于512的图像文件: {file_path} (尺寸: {width}x{height})")
                            os.remove(file_path)
                            continue
                        
                        # 计算图像质量评分
                        score = brisque.score(img)
                        if score < 4:
                            print(f"删除质量评分低于4的图像文件: {file_path} (评分: {score})")
                            os.remove(file_path)
                except UnidentifiedImageError:
                    # 如果文件不是图像，删除它
                    print(f"删除无法识别的图像文件: {file_path}")
                    os.remove(file_path)
                except Exception as e:
                    # 处理其他异常
                    print(f"其他错误 ({file_path}): {e}")

# 使用示例：指定多个文件夹路径
folders = [
    "/path/to/folder1",
    "/path/to/folder2",
    "/path/to/folder3"
]

delete_unidentified_small_or_low_quality_images(folders)
