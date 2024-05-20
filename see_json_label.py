import cv2
import json
import os

# 设置文件夹路径
folder_json = r'D:\fei_shu\pig_datas\train_json'  # 包含JSON文件的文件夹
folder_images = r'D:\fei_shu\pig_datas\train_img'  # 包含对应图片的文件夹
folder_output = r'D:\fei_shu\pig_datas\see_label'  # 保存带边界框的图片的文件夹

# 确保输出文件夹存在
if not os.path.exists(folder_output):
    os.makedirs(folder_output)

# 遍历JSON文件夹中的每个文件
for json_filename in os.listdir(folder_json):
    if json_filename.endswith('.json'):
        json_path = os.path.join(folder_json, json_filename)
        base_filename = os.path.splitext(json_filename)[0]
        image_path = os.path.join(folder_images, base_filename + '.jpg')  # 假设图片扩展名为.jpg
        output_path = os.path.join(folder_output, base_filename + '_bbox.jpg')  # 输出图片的路径

        # 如果对应的图片文件不存在，则跳过
        if not os.path.exists(image_path):
            continue

        # 读取图片
        image = cv2.imread(image_path)

        # 读取JSON文件
        with open(json_path, 'r') as f:
            data = json.load(f)

        # 遍历所有的边界框并在图片上绘制
        for shape in data.get('shape', []):
            if shape['label'] == 'pig':
                boxes = shape['boxes']
                x_min, y_min, x_max, y_max = boxes

                # 在图片上绘制边界框
                cv2.rectangle(image, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)  # 绿色边界框

        # 保存绘制了边界框的图片
        cv2.imwrite(output_path, image)

print('Finished drawing bounding boxes on images.')
