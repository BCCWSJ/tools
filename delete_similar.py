import os
from PIL import Image
import hashlib

def calculate_hash(img, hash_size=8):
    # 缩小图片为8x8，减少细节，只保留结构信息
    img = img.resize((hash_size, hash_size), Image.Resampling.LANCZOS)
    # 转换为灰度图像
    img = img.convert("L")
    # 计算所有像素的平均值
    pixels = list(img.getdata())
    avg = sum(pixels) / len(pixels)
    # 计算哈希值（每个像素的灰度值大于平均值为1，否则为0）
    bits = "".join(['1' if (pixel >= avg) else '0' for pixel in pixels])
    # 将位字符串转换为十六进制字符串
    hex_representation = '{:0>16x}'.format(int(bits, 2))
    return hex_representation

def find_duplicates(images):
    hashes = {}
    for img_path in images:
        img = Image.open(img_path)
        img_hash = calculate_hash(img)
        if img_hash in hashes:
            print(f"Duplicate found: {img_path} and {hashes[img_hash]}")
            os.remove(img_path)  # 删除找到的重复图片
        else:
            hashes[img_hash] = img_path

# 假设你的图片都在同一个文件夹里
image_dir = r'D:\fei_shu_file\test\111'
image_paths = [os.path.join(image_dir, f) for f in os.listdir(image_dir) if f.endswith(('.jpg', '.png'))]

find_duplicates(image_paths)