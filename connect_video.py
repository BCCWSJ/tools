import os
import subprocess

# 视频文件夹路径
video_folder = 'path/to/your/video/folder'
# 输出视频文件路径
output_video_path = 'path/to/your/output/output_video.mp4'
# 文件列表名称
file_list_name = 'file_list.txt'

# 获取视频文件夹中的所有视频文件
video_files = [f for f in os.listdir(video_folder) if f.endswith('.mp4')]  # 你可以添加其他视频格式

# 创建文件列表内容
file_list_content = "\n".join([f"file '{os.path.join(video_folder, file)}'" for file in video_files])

# 写入文件列表到文本文件
with open(file_list_name, 'w') as file_list:
    file_list.write(file_list_content)

# 构建ffmpeg命令
ffmpeg_command = ['ffmpeg', '-f', 'concat', '-safe', '0', '-i', file_list_name, '-c', 'copy', output_video_path]

# 调用ffmpeg进行视频拼接
subprocess.run(ffmpeg_command)

# 清理文件列表（可选）
os.remove(file_list_name)