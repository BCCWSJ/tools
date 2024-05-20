import os
import xml.etree.ElementTree as ET

def convert(size, box):
    dw = 1. / size[0]
    dh = 1. / size[1]
    x = (box[0] + box[1]) / 2.0 - 1
    y = (box[2] + box[3]) / 2.0 - 1
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    return (x, y, w, h)

def convert_annotation(xml_file, txt_file, classes):
    in_file = open(xml_file)
    out_file = open(txt_file, 'w')
    tree = ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)

    for obj in root.iter('object'):
        cls = obj.find('name').text
        if cls not in classes :
            continue
        # if obj.find('difficult').text == '1':
        #     continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text),
             float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
        bb = convert((w, h), b)
        out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')

    in_file.close()
    out_file.close()

# Classes
classes = ["pig"]  # Example class names

# Paths
xml_dir = r'Z:\TGY2023\AI_pig\25h_datas\train\xml'
txt_dir = r'Z:\TGY2023\AI_pig\25h_datas\train\txt'
if not os.path.exists(txt_dir):
    os.makedirs(txt_dir)

# Conversion
for xml_file in os.listdir(xml_dir):
    if xml_file.endswith('.xml'):
        xml_path = os.path.join(xml_dir, xml_file)
        txt_path = os.path.join(txt_dir, os.path.splitext(xml_file)[0] + '.txt')
        convert_annotation(xml_path, txt_path, classes)