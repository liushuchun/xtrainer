import os
import base64
import asyncio
from io import BytesIO
from PIL import Image

import numpy as np
from lmdeploy import pipeline,ChatTemplateConfig
from lmdeploy.vl import load_image 
# 获取模型实例



# 遍历文件夹并生成标注文件
class ImageCaptioner:
    def __init__(self):
        self.llm=pipeline("local_model_folder",chat_template_config=ChatTemplateConfig(model="llava-v1.6-vicuna-7b"))
        

    def caption_images(self):
        for folder_path in self.folders:
            for root, _, files in os.walk(folder_path):
                for file_name in files:
                    file_path = os.path.join(root, file_name)
                    if not file_name.lower().endswith((".png", ".jpg", ".jpeg")):
                        continue 
                    txt_path = f"{os.path.splitext(file_path)[0]}.caption"

                    # 如果txt文件已存在，则跳过
                    if os.path.exists(txt_path):
                        print(f"{txt_path} 已存在，跳过生成")
                        continue

                    # try:
                        # 打开图像并生成描述
                    image=load_image(file_path)
                    response=self.llm('describe this image',image)
                    print(response)
                    with open(txt_path, "w") as txt_file:
                        txt_file.write(response)
                    print(f"生成 {txt_path} 成功")
                    # except Exception as e:
                    #     print(f"处理文件 {file_path} 时出错: {e}")

# 使用示例
if __name__ == "__main__":
    folders = ["/media/shuchun/data/jewellry/basement"]  # 指定文件夹路径
    captioner = ImageCaptioner(folders)
    captioner.caption_images()
