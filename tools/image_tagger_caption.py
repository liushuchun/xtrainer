import os
import base64
import asyncio
from io import BytesIO
from PIL import Image
from llama_cpp import Llama
from llama_cpp.llama_chat_format import Llava15ChatHandler
import numpy as np

# 设置模型和消息的默认配置
defaults = {
    "model": "llava-v1.5-7b-Q4_K",
    "mmproj": "llava-v1.5-7b-mmproj-Q4_0",
    "temperature": 0.2,
    "max_tokens": 40,
    "prompt": "Please describe this image in 10 to 20 words."
}

# 编码图像为 base64
def encode_image(image: Image.Image):
    with BytesIO() as output:
        image.save(output, format="PNG")
        image_bytes = output.getvalue()
    return base64.b64encode(image_bytes).decode("utf-8")

# 获取模型实例
async def get_llava_instance(model, mm_proj, n_gpu_layers=0):
    model_path = f"./models/{model}.gguf"  # 替换成实际路径
    mmproj_path = f"./models/{mm_proj}.gguf"  # 替换成实际路径

    if not os.path.exists(model_path) or not os.path.exists(mmproj_path):
        raise FileNotFoundError("模型文件未找到，请检查路径")

    chat_handler = Llava15ChatHandler(clip_model_path=mmproj_path)
    return Llama(model_path=model_path, n_gpu_layers=n_gpu_layers, chat_format="llava-1-5", chat_handler=chat_handler)

# 生成图像描述
async def generate_caption(llm: Llama, image: Image.Image, prompt, temp, max_tokens=40):
    image_url = f"data:image/png;base64,{encode_image(image)}"
    messages = [
        {"role": "system", "content": "You are an assistant who describes the content and composition of images."},
        {"role": "user", "content": [{"type": "image_url", "image_url": {"url": image_url}}, {"type": "text", "text": prompt}]}
    ]
    response = llm.create_chat_completion(messages=messages, temperature=temp, max_tokens=max_tokens)
    return response["choices"][0]["message"]["content"].strip()

# 等待异步调用
def wait_for_async(coro):
    return asyncio.run(coro)

# 遍历文件夹并生成标注文件
class ImageCaptioner:
    def __init__(self, folders, model=defaults["model"], mmproj=defaults["mmproj"], prompt=defaults["prompt"], temperature=defaults["temperature"]):
        self.folders = folders
        self.model = model
        self.mmproj = mmproj
        self.prompt = prompt
        self.temperature = temperature
        self.llm = wait_for_async(get_llava_instance(self.model, self.mmproj))

    def caption_images(self):
        for folder_path in self.folders:
            for root, _, files in os.walk(folder_path):
                for file_name in files:
                    file_path = os.path.join(root, file_name)
                    txt_path = f"{os.path.splitext(file_path)[0]}.caption"

                    # 如果txt文件已存在，则跳过
                    if os.path.exists(txt_path):
                        print(f"{txt_path} 已存在，跳过生成")
                        continue

                    try:
                        # 打开图像并生成描述
                        with Image.open(file_path) as img:
                            caption = wait_for_async(lambda: generate_caption(self.llm, img, self.prompt, self.temperature))
                        with open(txt_path, "w") as txt_file:
                            txt_file.write(caption)
                        print(f"生成 {txt_path} 成功")
                    except Exception as e:
                        print(f"处理文件 {file_path} 时出错: {e}")

# 使用示例
if __name__ == "__main__":
    folders = ["/path/to/folder1"]  # 指定文件夹路径
    captioner = ImageCaptioner(folders)
    captioner.caption_images()
