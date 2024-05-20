import random
import os
import glob
import math
from PIL import Image, ImageDraw, ImageFont
import numpy as np

# 创建一张给定尺寸的空白图片
def create_blank_image(width, height):
    return Image.new('RGB', (width, height), color=(21, 21, 21))  # 十六进制151515对应的RGB值

# 固定的颜色列表
fixed_colors = [(255, 255, 255), (85, 236, 235), (246, 238, 105)]

# 随机选择颜色
def random_color():
    return random.choice(fixed_colors)

# 随机选择字体样式和大小
def random_font(font_folders, font_size):
    font_path = random.choice(font_folders)
    return ImageFont.truetype(font_path, font_size)

def is_pixel_overlapping(pixels1, pixels2):
    return not pixels1.isdisjoint(pixels2)
# # 检查新的矩形框是否与已存在的框重叠
# def is_overlapping(new_position, new_pixels, boxes):
#     x1, y1, x2, y2 = new_position
#     for pos, pixels in boxes:
#         if pos:  # 如果 pos 不是 None，即这是一个矩形框
#             left = max(x1, pos[0])
#             right = min(x2, pos[2])
#             top = max(y1, pos[1])
#             bottom = min(y2, pos[3])
#             if left < right and top < bottom:  # 如果存在重叠区域
#                 return True
#         # 检查两个像素集合是否有重叠
#         if pixels and is_pixel_overlapping(new_pixels, pixels):
#             return True
#     return False

def get_nontransparent_pixels(image):
    # 将图像转换为NumPy数组
    image_array = np.array(image)
    # 获取alpha通道（假设它是最后一个通道）
    alpha_channel = image_array[:, :, -1]
    # 找出所有非透明像素的坐标
    nontransparent_coords = np.argwhere(alpha_channel > 0)
    # 返回一个包含(x, y)坐标的集合
    return {tuple(coord) for coord in nontransparent_coords[:, [1, 0]]}  # 注意坐标的顺序

def estimate_rotated_box(x, y, width, height, angle):
    angle = -angle  # PIL旋转是逆时针的，而我们通常的角度计算是顺时针的
    radians = math.radians(angle)
    cos_theta = abs(math.cos(radians))
    sin_theta = abs(math.sin(radians))

    # 估算旋转后的宽度和高度
    new_width = int(width * cos_theta + height * sin_theta)
    new_height = int(width * sin_theta + height * cos_theta)

    # 估算旋转后的边界框
    return (x, y, x + new_width, y + new_height)

# 将单词写入图片的特定位置
def draw_word_on_image(image, word, font, color, angle, boxes, center=False):
    draw = ImageDraw.Draw(image)
    text_width, text_height = draw.textsize(word, font=font)

    # 创建文本图像
    text_image = Image.new('RGBA', (text_width, text_height), (255, 255, 255, 0))
    text_draw = ImageDraw.Draw(text_image)
    text_draw.text((0, 0), word, font=font, fill=color)

    # 如果是居中且大小为one，不旋转
    if center:
        rotated_text_image = text_image  # 不旋转图像
        rotated_width, rotated_height = text_width, text_height
    else:
        # 旋转文本图像
        rotated_text_image = text_image.rotate(angle, expand=1)
        rotated_width, rotated_height = rotated_text_image.size

    # 获取旋转后文本的非透明像素集合
    nontransparent_pixels = get_nontransparent_pixels(rotated_text_image)

    # 尝试放置文本，避免重叠
    for _ in range(100):  # 尝试100次找到不重叠的位置
        if center:
            x = (image.width - text_width) // 2
            y = (image.height - text_height) // 2
        else:
            x = random.randint(0, image.width - rotated_width)
            y = random.randint(0, image.height - rotated_height)

        # 创建一个新集合，将非透明像素移动到预期位置
        moved_pixels = {(pixel[0] + x, pixel[1] + y) for pixel in nontransparent_pixels}
        # 检查是否与已放置的文本重叠
        if not any(is_pixel_overlapping(moved_pixels, pixels) for _, pixels in boxes):
            image.paste(rotated_text_image, (x, y), rotated_text_image)
            # 保存新放置的文本的非透明像素
            boxes.append((None, moved_pixels))
            return True  # 成功放置文本
    return False  # 未能成功放置文本

# 主程序
def create_word_filled_image(image_size, word, font_folders, large_font_folder, max_attempts, outpath, four_count, three_count, two_count, one_count, one=200):
    image = create_blank_image(*image_size)
    boxes = []  # 存储已放置文本的矩形框
    font_counts = {20: four_count, 40: three_count, 100: two_count, one: one_count}
    font_usage = {20: 0, 40: 0, 100: 0, one: 0}

    attempts = 0
    used_large_font = False  # 用于跟踪是否使用了一号字体
    while attempts < max_attempts and any(usage < font_counts[size] for size, usage in font_usage.items()):
        # 随机选择字体大小
        font_size = random.choice([size for size in font_counts if font_usage[size] < font_counts[size]])
        if font_size == one:
            font_path = random.choice(large_font_folder)
        else:
            font_path = random.choice(font_folders)

        font = ImageFont.truetype(font_path, font_size)
        color = random_color()
        angle = 0 if font_size == one else random.choice([0, 90, 270, 360])

        # 对于1号字体，将其放在图片中间
        center = font_size == one
        draw_word_on_image(image, word, font, color, angle, boxes, center=center)
        if draw_word_on_image(image, word, font, color, angle, boxes, center=center):
            if center:
                used_large_font = True

        font_usage[font_size] += 1
        attempts += 1

    # 如果在所有尝试结束后一号字体的文本没有被画，则进行额外的尝试
    if not used_large_font:
        while not used_large_font:
            font_path = random.choice(large_font_folder)
            font = ImageFont.truetype(font_path, one)
            color = random_color()
            if draw_word_on_image(image, word, font, color, 0, boxes, center=True):
                used_large_font = True  # 成功放置文本
            else:
                print("Error: Unable to place the centered text after multiple attempts.")
                break

    image.save(outpath)
    return image


# 示例
all_font_folders = [
    glob.glob(os.path.join(r'D:\to HJ\font_files', 'comic_sans_ms', '*.ttf')),
    glob.glob(os.path.join(r'D:\to HJ\font_files', 'black', '*.ttf')),
    glob.glob(os.path.join(r'D:\to HJ\font_files', 'good_black', '*.ttf')),
    glob.glob(os.path.join(r'D:\to HJ\font_files', 'song', '*.ttf'))
]

# 将所有的字体文件列表合并为一个列表
all_font_paths = [font for sublist in all_font_folders for font in sublist]

large_font_folder = glob.glob(os.path.join(r'D:\to HJ\font_files', 'comic_sans_ms', '*.ttf'))

image_size = (489, 968)
word = "Alice"
max_attempts = 1000  # 尝试的次数
outpath = 'word_filled_image.png'  # 保存图像的路径

# 设置每种字体大小的单词数量
four_count = 70  # 4号字体的单词数量
three_count = 50  # 3号字体的单词数量
two_count = 30    # 2号字体的单词数量
one_count = 1    # 1号字体的单词数量

image = create_word_filled_image(image_size, word, all_font_paths, large_font_folder, max_attempts, outpath, four_count, three_count, two_count, one_count)

image.show()