import cv2
import os

# 视频文件路径
video_path = r'Z:\TGY2023\AI_pig\videos\IPC-HFW4443T-1_2024-04-02_114300_115100.mp4'
# 存储图片的文件夹路径
frames_folder = r'D:\fei_shu_file\test\img'
# 每隔n帧抽取一帧
frame_interval = 750  # 例如，每隔5帧抽取一帧

# 如果存储图片的文件夹不存在，则创建它
if not os.path.exists(frames_folder):
    os.makedirs(frames_folder)

# 打开视频文件
cap = cv2.VideoCapture(video_path)

# 初始化帧计数器
frame_count = 849000

while True:
    # 读取下一帧
    ret, frame = cap.read()

    # 如果读取成功，则继续处理
    if ret:
        # 检查当前帧号是否为指定间隔的倍数
        if frame_count % frame_interval == 0:
            # 构造输出图片文件的名称
            frame_filename = os.path.join(frames_folder, f"frame_{frame_count}.png")
            # 保存当前帧为图片
            cv2.imwrite(frame_filename, frame)
            print(f"Saved {frame_filename}")

        # 更新帧计数器
        frame_count += 1
    else:
        # 如果没有帧了（视频结束），则退出循环
        print(f'no frame{frame_count},next is {frame_count-(frame_count%750)+750}')
        break

# 释放视频捕获对象
cap.release()
print("Finished extracting frames.")