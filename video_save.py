import cv2


# 视频路径
video_path = r"rtmp://119.23.107.23:1935/cam03"

# Open the video file
cap = cv2.VideoCapture(video_path)
frame_cnt=0
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))  # 获取视频的宽度
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))  # 获取视频的高度
fps = cap.get(cv2.CAP_PROP_FPS)  # 获取视频的帧率
writer = cv2.VideoWriter("video_save.mp4", 0x7634706d, fps, (width,height ))
# Loop through the video frames
while cap.isOpened():
    # Read a frame from the video
    success, frame = cap.read()
    writer.write(frame)
    frame_cnt+=1
    if not success:
        print(f'Failed to read frame {frame_cnt}.Reached end of video.')
        break
writer.release()
cap.release()
cv2.destroyAllWindows()

