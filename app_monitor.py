import os
import time
import subprocess
from datetime import datetime

def monitor_app(app_name):
    # 1. 激活/打开软件
    print(f"正在打开 {app_name}...")
    # macOS 下使用 open 命令打开应用程序
    os.system(f'open -a "{app_name}"')
    
    # 等待软件完全打开（可根据软件启动速度调整等待时间）
    time.sleep(3)

    # 2. 截图保存到本地
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    screenshot_path = f"screenshot_{app_name}_{timestamp}.png"
    print(f"正在截图并保存到 {screenshot_path}...")
    # macOS 下使用 screencapture 命令进行全屏截图
    # 如果想只截取当前窗口，可以使用其它参数或者第三方库如 pyautogui
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
    # 替换为你想要监控的软件名称，例如 "Calculator", "Safari", "微信" 等
    target_app = "Calculator" 
    
    # 替换为你的 Google Cloud Storage Bucket 名称
    # bucket_name = "your-bucket-name"
    
    saved_image = monitor_app(target_app)
    
    # 如果需要上传到云端，取消下面两行的注释并填入正确的 bucket 名称
    # destination_name = os.path.basename(saved_image)
    # upload_to_gcs(bucket_name, saved_image, destination_name)
    
    print("脚本执行完毕！")
