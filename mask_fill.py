import os
import cv2
import numpy as np

# 设置源文件夹和目标文件夹
input_folder_path = r'Z:\TGY2023\AI_pig\Lee_dataset\images'
output_folder_path = r'Z:\TGY2023\AI_pig\Lee_dataset\mask_img'
mask_image_path = 'file/black.png'  # 掩码图片的路径

# 确保输出文件夹存在
if not os.path.exists(output_folder_path):
    os.makedirs(output_folder_path)

# 读取掩码图像
mask_image = cv2.imread(mask_image_path, cv2.IMREAD_GRAYSCALE)
if mask_image is None:
    print(f"Mask image at {mask_image_path} could not be read.")
    exit()

# 遍历输入文件夹中的所有图像
for filename in os.listdir(input_folder_path):
    # 构建完整的文件路径
    file_path = os.path.join(input_folder_path, filename)

    # 确保是文件而不是文件夹
    if os.path.isfile(file_path):
        # 读取图像
        image = cv2.imread(file_path)
        if image is None:
            print(f"Image {filename} could not be read.")
            continue

        # 调整掩码大小以匹配图像大小
        resized_mask = cv2.resize(mask_image, (image.shape[1], image.shape[0]), interpolation=cv2.INTER_AREA)

        # 应用掩码（确保掩码是二值化的，即只有0和255）
        result = cv2.bitwise_and(image, image, mask=resized_mask)

        # 构建输出文件路径
        output_file_path = os.path.join(output_folder_path, filename)

        # 保存结果图像
        cv2.imwrite(output_file_path, result)
        print(f"Processed image saved as {output_file_path}")

print("Processing completed.")