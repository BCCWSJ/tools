import os
import random
import shutil

# 设置源文件夹和目标文件夹
source_dir = r'Z:\TGY2023\AI_pig\25h_datas\train\imgs'
destination_dir = r'Z:\TGY2023\AI_pig\25h_datas\val\imgs'

# 设置想要移动的文件数量
n = 200

# 获取源文件夹中的所有文件列表
files = [os.path.join(source_dir, f) for f in os.listdir(source_dir) if os.path.isfile(os.path.join(source_dir, f))]

# 如果文件数量少于n，则移动所有文件
if len(files) < n:
    n = len(files)

# 随机选择n个文件
selected_files = random.sample(files, n)

# 移动选中的文件到目标文件夹
for file_path in selected_files:
    shutil.move(file_path, destination_dir)
    print(f'Moved file {file_path} to {destination_dir}')
