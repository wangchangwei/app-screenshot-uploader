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
        os.system(f'screencapture -R {rect} "{screenshot_path}"')
    else:
        print(f"未能找到指定应用窗口，将截取全屏保存到 {screenshot_path}...")
        os.system(f'screencapture -x "{screenshot_path}"')
        
    print(f"截图已保存: {screenshot_path}")
    return screenshot_path

def upload_to_oss(source_file_name, bucket_name, object_name):
    """
    3. 上传到兼容 S3 协议的 OSS (如 Cloudflare R2, Backblaze B2, 阿里云 OSS 等)
    需要先安装依赖: pip install boto3
    """
    try:
        import boto3
        from botocore.exceptions import NoCredentialsError

        # 请替换为你的 OSS 服务商提供的参数
        # 这里以通用的 S3 兼容 API 为例
        ENDPOINT_URL = 'https://<你的OSS服务商地址>.com'  
        ACCESS_KEY = '<你的_ACCESS_KEY>'
        SECRET_KEY = '<你的_SECRET_KEY>'

        print(f"正在上传 {source_file_name} 到 OSS...")
        
        s3_client = boto3.client(
            's3',
            endpoint_url=ENDPOINT_URL,
            aws_access_key_id=ACCESS_KEY,
            aws_secret_access_key=SECRET_KEY
        )

        s3_client.upload_file(source_file_name, bucket_name, object_name)
        print(f"上传成功！文件已保存至 bucket: {bucket_name}, 路径: {object_name}")

    except ImportError:
        print("未安装 boto3，跳过上传。请运行 pip install boto3 安装。")
    except NoCredentialsError:
        print("未找到有效的凭证，上传失败。")
    except Exception as e:
        print(f"上传失败，错误信息: {e}")

if __name__ == "__main__":
    target_app = "Calculator" 
    
    saved_image = monitor_app(target_app)
    
    # ==== OSS 上传区 ====
    # 如果您申请了免费的 OSS 并且填好了上面的密钥信息，取消下面三行的注释即可开启自动上传：
    # bucket_name = "your-bucket-name"
    # destination_name = os.path.basename(saved_image)
    # upload_to_oss(saved_image, bucket_name, destination_name)
    
    print("脚本执行完毕！")
