import os
from xml.etree.ElementTree import Element, SubElement, ElementTree
import cv2

def create_xml_file(img_path, boxes, labels, output_dir):
    img_filename = os.path.basename(img_path)
    img_name, img_ext = os.path.splitext(img_filename)
    img = cv2.imread(img_path)
    h, w, _ = img.shape

    # 创建XML结构
    annotation = Element('annotation')
    filename = SubElement(annotation, 'filename')
    filename.text = img_filename
    size = SubElement(annotation, 'size')
    width = SubElement(size, 'width')
    width.text = str(w)
    height = SubElement(size, 'height')
    height.text = str(h)
    depth = SubElement(size, 'depth')
    depth.text = '3'

    for box, label in zip(boxes, labels):
        # YOLO格式转换为像素坐标
        x_center, y_center, box_width, box_height = box
        x_min = (x_center - box_width / 2) * w
        y_min = (y_center - box_height / 2) * h
        x_max = (x_center + box_width / 2) * w
        y_max = (y_center + box_height / 2) * h

        # 创建object节点
        object = SubElement(annotation, 'object')
        name = SubElement(object, 'name')
        name.text = str(label)
        bndbox = SubElement(object, 'bndbox')
        xmin = SubElement(bndbox, 'xmin')
        xmin.text = str(int(x_min))
        ymin = SubElement(bndbox, 'ymin')
        ymin.text = str(int(y_min))
        xmax = SubElement(bndbox, 'xmax')
        xmax.text = str(int(x_max))
        ymax = SubElement(bndbox, 'ymax')
        ymax.text = str(int(y_max))

    # 生成XML文件
    tree = ElementTree(annotation)
    xml_filename = os.path.join(output_dir, img_name + '.xml')
    tree.write(xml_filename)

# 假设label文件和图片在同一个文件夹内
input_dir = r'Z:\TGY2023\AI_pig\ourpig\spu_label'
output_dir = r'Z:\TGY2023\AI_pig\ourpig\xml'
image_dir = r'Z:\TGY2023\AI_pig\ourpig\mask_img'
class_labels = ['pig']  # 假设你有三个类别

for label_file in os.listdir(input_dir):
    label_file_path = os.path.join(input_dir, label_file)
    img_path = os.path.join(image_dir, os.path.splitext(label_file)[0] + '.png')  # 假设图片格式为jpg

    with open(label_file_path, 'r') as file:
        lines = file.readlines()

    boxes = []
    labels = []
    for line in lines:
        class_id, x_center, y_center, width, height = map(float, line.split())
        boxes.append((x_center, y_center, width, height))
        labels.append(class_labels[int(class_id)])

    create_xml_file(img_path, boxes, labels, output_dir)