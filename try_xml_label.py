import os
import cv2
import yolov8
from xml.etree.ElementTree import Element, SubElement, ElementTree

def create_pascal_voc_xml(image_path, detections, output_folder):
    image_name = os.path.basename(image_path)
    image = cv2.imread(image_path)
    height, width, depth = image.shape

    # 创建XML文件的结构
    annotation = Element('annotation')
    tree = ElementTree(annotation)

    folder = SubElement(annotation, 'folder')
    folder.text = os.path.basename(os.path.dirname(image_path))

    filename = SubElement(annotation, 'filename')
    filename.text = image_name

    size = SubElement(annotation, 'size')
    width_xml = SubElement(size, 'width')
    width_xml.text = str(width)
    height_xml = SubElement(size, 'height')
    height_xml.text = str(height)
    depth_xml = SubElement(size, 'depth')
    depth_xml.text = str(depth)

    for detection in detections:
        x_min, y_min, x_max, y_max = detection[:4]
        label = str('pig')
        score = detection[4]

        if score < 0.65:  # 过滤低置信度的检测结果
            continue

        object = SubElement(annotation, 'object')
        name = SubElement(object, 'name')
        name.text = label
        pose = SubElement(object, 'pose')
        pose.text = 'Unspecified'
        truncated = SubElement(object, 'truncated')
        truncated.text = '0'
        difficult = SubElement(object, 'difficult')
        difficult.text = '0'

        bndbox = SubElement(object, 'bndbox')
        xmin = SubElement(bndbox, 'xmin')
        xmin.text = str(int(x_min))
        ymin = SubElement(bndbox, 'ymin')
        ymin.text = str(int(y_min))
        xmax = SubElement(bndbox, 'xmax')
        xmax.text = str(int(x_max))
        ymax = SubElement(bndbox, 'ymax')
        ymax.text = str(int(y_max))

    # 保存XML文件
    xml_file_path = os.path.join(output_folder, os.path.splitext(image_name)[0] + '.xml')
    tree.write(xml_file_path)

# 加载预训练的YOLOv8模型
model_ckpt = r'best.pt'
model = yolov8.YoloDetector(model_ckpt)

# 图像文件夹路径
image_folder = r'Z:\TGY2023\AI_pig\25h_datas\train\imgs'
# 保存伪标签的文件夹路径
pseudo_label_folder = r"Z:\TGY2023\AI_pig\25h_datas\train\xml"

# 创建保存伪标签的文件夹（如果不存在）
if not os.path.exists(pseudo_label_folder):
    os.makedirs(pseudo_label_folder)

# 遍历文件夹中的所有图片
for image_name in os.listdir(image_folder):
    if image_name.endswith(".png"):  # 确认文件是PNG格式
        image_path = os.path.join(image_folder, image_name)
        image = cv2.imread(image_path)
        detections = model.detect(image)

        # 转换检测结果到Pascal VOC格式并保存为XML
        create_pascal_voc_xml(image_path, detections, pseudo_label_folder)

print("处理完成!")
