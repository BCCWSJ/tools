import json
import os
from PIL import Image

# 设置文件夹路径
folder_json = r'D:\fei_shu\pig_datas\train_json'  # 包含JSON文件的文件夹
folder_images = r'D:\fei_shu\pig_datas\train_img'  # 包含对应图片的文件夜
folder_txt = r'D:\fei_shu\pig_datas\train_txt'  # 保存TXT文件的文件夹

# 确保TXT文件夹存在
if not os.path.exists(folder_txt):
    os.makedirs(folder_txt)

# 为'pig'标签分配类索引
class_index = 0

# 遍历JSON文件夹中的每个文件
for json_filename in os.listdir(folder_json):
    if json_filename.endswith('.json'):
        json_path = os.path.join(folder_json, json_filename)
        base_filename = os.path.splitext(json_filename)[0]
        image_path = os.path.join(folder_images, base_filename + '.jpg')  # 假设图片扩展名为.jpg
        txt_path = os.path.join(folder_txt, base_filename + '.txt')

        # 如果对应的图片文件不存在，则跳过
        if not os.path.exists(image_path):
            continue

        # 读取图片尺寸以进行坐标归一化
        with Image.open(image_path) as img:
            img_width, img_height = img.size

        # 读取JSON文件
        with open(json_path, 'r') as f:
            data = json.load(f)

        # 提取边界框信息并写入TXT文件
        with open(txt_path, 'w') as txt_file:
            for shape in data.get('shape', []):
                if shape['label'] == 'pig':
                    boxes = shape['boxes']
                    x_min, y_min, x_max, y_max = boxes

                    # 计算YOLO格式的中心点坐标和宽高
                    x_center = ((x_min + x_max) / 2) / img_width
                    y_center = ((y_min + y_max) / 2) / img_height
                    width = (x_max - x_min) / img_width
                    height = (y_max - y_min) / img_height

                    # 写入转换后的坐标到TXT文件
                    txt_file.write(f"{class_index} {x_center} {y_center} {width} {height}\n")

print('Finished converting JSON files to YOLOv8 format TXT files.')
