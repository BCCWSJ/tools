import cv2
import os

# 设置文件夹路径
folder_txt = r'Z:\TGY2023\AI_pig\ourpig\spu_label'  # 包含txt文件的文件夹
folder_images = r'Z:\TGY2023\AI_pig\ourpig\mask_img'  # 包含对应图片的文件夹
folder_output = r'Z:\TGY2023\AI_pig\ourpig\11'  # 保存带边界框的图片的文件夹

# 确保输出文件夹存在
if not os.path.exists(folder_output):
    os.makedirs(folder_output)

# 遍历TXT文件夹中的每个文件
for txt_filename in os.listdir(folder_txt):
    if txt_filename.endswith('.txt'):
        txt_path = os.path.join(folder_txt, txt_filename)
        base_filename = os.path.splitext(txt_filename)[0]
        image_path = os.path.join(folder_images, base_filename + '.png')  # 假设图片扩展名
        output_path = os.path.join(folder_output, base_filename + '_bbox.png')  # 输出图片的路径

        # 如果对应的图片文件不存在，则跳过
        if not os.path.exists(image_path):
            continue

        # 读取图片
        image = cv2.imread(image_path)
        img_height, img_width = image.shape[:2]

        # 读取TXT文件
        with open(txt_path, 'r') as f:
            lines = f.readlines()

        # 遍历TXT文件中的每一行
        for line in lines:
            class_id, x_center, y_center, width, height = map(float, line.split())

            # 将YOLO格式的坐标转换为像素坐标
            x_center_pixel = int(x_center * img_width)
            y_center_pixel = int(y_center * img_height)
            width_pixel = int(width * img_width)
            height_pixel = int(height * img_height)

            # 计算边界框的左上角和右下角坐标
            x_min = int(x_center_pixel - width_pixel / 2)
            y_min = int(y_center_pixel - height_pixel / 2)
            x_max = int(x_center_pixel + width_pixel / 2)
            y_max = int(y_center_pixel + height_pixel / 2)

            # 在图片上绘制边界框
            cv2.rectangle(image, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)  # 绿色边界框

        # 保存绘制了边界框的图片
        cv2.imwrite(output_path, image)

print('Finished drawing bounding boxes on images.')