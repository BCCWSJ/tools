import os
from PIL import Image, ImageDraw

# 设置源文件夹和目标文件夹
source_folder = 'path_to_source_folder'
target_folder = 'path_to_target_folder'

# 如果目标文件夹不存在，则创建它
if not os.path.exists(target_folder):
    os.makedirs(target_folder)

# 定义多个自定义形状的坐标点列表，每个列表代表一个区域
shapes = [
    [(0, 0), (0, 0), (0, 0)],  # 第一个形状的坐标点
    [(0, 0), (0, 0), (0, 0)],  # 第二个形状的坐标点
    # ...可以继续添加更多的形状
]

# 遍历源文件夹中的所有图片
for filename in os.listdir(source_folder):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
        # 构造完整的文件路径
        source_path = os.path.join(source_folder, filename)
        target_path = os.path.join(target_folder, filename)

        # 打开图片
        image = Image.open(source_path)

        # 创建一个可用于绘图的对象
        draw = ImageDraw.Draw(image)

        # 遍历所有的形状并填充它们
        for points in shapes:
            draw.polygon(points, fill="black")

        # 保存到目标文件夹
        image.save(target_path)

print("所有图片处理完成。")