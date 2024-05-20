import cv2
import os

# 视频文件路径
video_path = r'Z:\TGY2023\AI_pig\videos\20240407\IPC-HFW4443T-1\train.mp4'
# 存储图片的文件夹路径
frames_folder = r'Z:\TGY2023\AI_pig\25h_datas\images'
# 每隔n帧抽取一帧
frame_interval = 375  # 例如，每隔5帧抽取一帧
mask_image_path = 'file/black.png'  # 掩码图片的路径
mask_image = cv2.imread(mask_image_path, cv2.IMREAD_GRAYSCALE)
if mask_image is None:
    print(f"Mask image at {mask_image_path} could not be read.")
    exit()

# 如果存储图片的文件夹不存在，则创建它
if not os.path.exists(frames_folder):
    os.makedirs(frames_folder)

# 打开视频文件
cap = cv2.VideoCapture(video_path)

# 初始化帧计数器
frame_count = 0

while True:
    # 读取下一帧
    ret, frame = cap.read()

    # 如果读取成功，则继续处理
    if ret:
        # 检查当前帧号是否为指定间隔的倍数
        if frame_count % frame_interval == 0:
            # 调整掩码大小以匹配图像大小
            resized_mask = cv2.resize(mask_image, (frame.shape[1], frame.shape[0]), interpolation=cv2.INTER_AREA)

            # 应用掩码（确保掩码是二值化的，即只有0和255）
            result = cv2.bitwise_and(frame, frame, mask=resized_mask)
            # 构造输出图片文件的名称
            frame_filename = os.path.join(frames_folder, f"frame_{frame_count}.png")
            # 保存当前帧为图片
            cv2.imwrite(frame_filename, result)
            print(f"Saved {frame_filename}")

        # 更新帧计数器
        frame_count += 1
    else:
        # 如果没有帧了（视频结束），则退出循环
        print(f'no frame{frame_count}')
        break

# 释放视频捕获对象
cap.release()
print("Finished extracting frames.")