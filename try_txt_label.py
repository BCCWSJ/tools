import cv2
import yolov8
import os

model_ckpt = r'best.pt'
# 加载预训练的YOLOv8模型
model = yolov8.YoloDetector(model_ckpt)

# 图像文件夹路径
image_folder = r'Z:\TGY2023\AI_pig\ourpig\mask_img'
# 保存伪标签的文件夹路径
pseudo_label_folder = r"Z:\TGY2023\AI_pig\ourpig\spu_label"

# 创建保存伪标签的文件夹（如果不存在）
if not os.path.exists(pseudo_label_folder):
    os.makedirs(pseudo_label_folder)

# 遍历文件夹中的所有图片
for image_name in os.listdir(image_folder):
    if image_name.endswith(".png"):  # 确认文件是PNG格式
        image_path = os.path.join(image_folder, image_name)
        image = cv2.imread(image_path)
        detections = model.detect(image)
        height = image.shape[0]
        width = image.shape[1]

        # 将检测结果转换为某种标注格式
        pseudo_labels = []
        for detection in detections:
            x, y, w, h = ((detection[0]+detection[2])/2)/width, ((detection[1]+detection[3])/2)/height, ((detection[2]-detection[0]))/width, ((detection[3]-detection[1]))/height  # 获取边界框坐标
            label = detection[5]  # 获取检测到的类别
            score = detection[4]  # 获取置信度

            # 过滤低置信度的检测结果
            if score < 0.5:
                continue

            # 转换为你需要的标注格式
            pseudo_label = {
                "class": label,
                "bbox": [x, y, w, h],
                "confidence": score
            }
            pseudo_labels.append(pseudo_label)

        # 为每个图像创建单独的伪标签文件
        pseudo_label_path = os.path.join(pseudo_label_folder, f"{os.path.splitext(image_name)[0]}.txt")
        with open(pseudo_label_path, "w") as file:
            for label in pseudo_labels:
                file.write(f"{label['class']} {label['bbox'][0]} {label['bbox'][1]} {label['bbox'][2]} {label['bbox'][3]}\n")

print("处理完成!")