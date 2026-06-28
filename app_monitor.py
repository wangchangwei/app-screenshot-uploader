import os
import time
import subprocess
from datetime import datetime

def get_window_rect(app_name):
    # 使用 AppleScript 获取软件的主窗口位置和大小
    script = f'''
    tell application "System Events"
        tell process "{app_name}"
            set p to position of window 1
            set s to size of window 1
            return (item 1 of p as string) & "," & (item 2 of p as string) & "," & (item 1 of s as string) & "," & (item 2 of s as string)
        end tell
    end tell
    '''
    try:
        result = subprocess.check_output(['osascript', '-e', script], text=True).strip()
        x, y, w, h = result.split(',')
        return f"{x},{y},{w},{h}"
    except Exception as e:
        print(f"无法获取 {app_name} 的窗口位置。错误：{e}")
        return None

def monitor_app(app_name):
    # 1. 激活/打开软件
    print(f"正在打开 {app_name}...")
    os.system(f'open -a "{app_name}"')
    
    # 等待软件完全打开
    time.sleep(3)

    # 2. 获取该软件的窗口区域
    rect = get_window_rect(app_name)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    screenshot_path = f"screenshot_{app_name}_{timestamp}.png"
    
    if rect:
        print(f"检测到 {app_name} 窗口区域: {rect}，正在截图并保存到 {screenshot_path}...")
        # macOS 下使用 screencapture -R 截取特定区域 (x,y,w,h)
        os.system(f'screencapture -R {rect} "{screenshot_path}"')
    else:
        print(f"未能找到指定应用窗口，将截取全屏保存到 {screenshot_path}...")
        os.system(f'screencapture -x "{screenshot_path}"')
        
    print(f"截图已保存: {screenshot_path}")
    return screenshot_path

def upload_to_gcs(bucket_name, source_file_name, destination_blob_name):
    """
    3. 上传到 Google Cloud Storage (OSS)
    需要先安装依赖: pip install google-cloud-storage
    并且设置好环境变量: export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/key.json"
    """
    try:
        from google.cloud import storage
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(destination_blob_name)

        print(f"正在上传 {source_file_name} 到 Google Cloud Storage bucket {bucket_name}...")
        blob.upload_from_filename(source_file_name)
        print(f"上传成功！文件已保存至: gs://{bucket_name}/{destination_blob_name}")
    except ImportError:
        print("未安装 google-cloud-storage，跳过上传。请运行 pip install google-cloud-storage 安装。")
    except Exception as e:
        print(f"上传失败，请检查凭证配置。错误信息: {e}")

if __name__ == "__main__":
    target_app = "Calculator" 
    
    saved_image = monitor_app(target_app)
    
    # 如果需要上传到云端，取消下面两行的注释并填入正确的 bucket 名称
    # bucket_name = "your-bucket-name"
    # destination_name = os.path.basename(saved_image)
    # upload_to_gcs(bucket_name, saved_image, destination_name)
    
    print("脚本执行完毕！")
