import os
import shutil

# 设置文件夹路径
folder_a = r'Z:\TGY2023\AI_pig\25h_datas\val\imgs'
folder_b = r'Z:\TGY2023\AI_pig\25h_datas\train\txt'
folder_c = r'Z:\TGY2023\AI_pig\25h_datas\val\txt'

# 确保目标文件夹C存在
if not os.path.exists(folder_c):
    os.makedirs(folder_c)

# 获取文件夹A中所有文件的文件名（不包括扩展名）
files_in_a = {os.path.splitext(file)[0] for file in os.listdir(folder_a)}

# 遍历文件夹B中的所有文件
for file in os.listdir(folder_b):
    # 检查文件名（不包括扩展名）是否在文件夹A中
    if os.path.splitext(file)[0] in files_in_a:
        # 构建原始文件和目标文件的完整路径
        src_file = os.path.join(folder_b, file)
        dst_file = os.path.join(folder_c, file)

        # 移动文件
        shutil.move(src_file, dst_file)
        print(f'Moved: {file}')

print('Finished moving matching files.')