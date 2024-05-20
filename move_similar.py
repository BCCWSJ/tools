import os
import shutil
import random
from PIL import Image
import imagehash

# 设置文件夹路径
source_folder = r'Z:\TGY2023\AI_pig\25h_datas\images'
destination_folder = r'Z:\TGY2023\AI_pig\25h_datas\train\imgs'

# 创建目标文件夹如果它不存在
if not os.path.exists(destination_folder):
    os.makedirs(destination_folder)

# 设置图像哈希的大小
hash_size = 8

# 读取所有图片并计算哈希值
hashes = {}
for subdir, dirs, files in os.walk(source_folder):
    for filename in files:
        file_path = os.path.join(subdir, filename)
        try:
            with Image.open(file_path) as img:
                # 计算哈希值
                hash_value = imagehash.average_hash(img, hash_size)
                print(f'compute hash {file_path}')
                # 存储哈希值和对应的文件路径
                if hash_value in hashes:
                    hashes[hash_value].append(file_path)
                else:
                    hashes[hash_value] = [file_path]
        except (IOError, OSError):
            print(f'Error processing file {file_path}')

# 遍历哈希值，找到相似的图片，并移动80%到目标文件夹
for hash_value, files in hashes.items():
    if len(files) > 1:  # 如果有相似的图片
        # 计算要移动的图片数量，确保至少移动一张图片
        num_files_to_move = max(1, int(len(files) * 0.2))
        # 随机选择要移动的图片
        files_to_move = random.sample(files, num_files_to_move)
        for file_path in files_to_move:
            # 移动文件到目标文件夹
            shutil.move(file_path, os.path.join(destination_folder, os.path.basename(file_path)))
            print(f'Moved {file_path} to {destination_folder}')