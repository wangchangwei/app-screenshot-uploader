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
    screenshot_path = f"screenshot_{app_name}.png"
    
    if rect:
        print(f"检测到 {app_name} 窗口区域: {rect}，正在截图并保存到 {screenshot_path}...")
        os.system(f'screencapture -R {rect} "{screenshot_path}"')
    else:
        print(f"未能找到指定应用窗口，将截取全屏保存到 {screenshot_path}...")
        os.system(f'screencapture -x "{screenshot_path}"')
        
    print(f"截图已保存: {screenshot_path}")
    return screenshot_path

def upload_to_github(source_file_name, owner, repo, path):
    """
    3. 上传到 GitHub 仓库
    需要安装 gh CLI 并登录: https://cli.github.com/
    """
    try:
        import subprocess
        import base64

        print(f"正在上传 {source_file_name} 到 GitHub...")

        # 读取文件并 base64 编码
        with open(source_file_name, 'rb') as f:
            encoded_content = base64.b64encode(f.read()).decode('utf-8')

        # 使用 gh api 上传，会自动使用本地已登录的 GitHub 认证
        result = subprocess.run(
            ['gh', 'api', '/repos/{owner}/{repo}/contents/{path}'.format(owner=owner, repo=repo, path=path),
             '--method', 'PUT',
             '-f', 'message=Upload {source_file_name}'.format(source_file_name=source_file_name),
             '-f', 'content={encoded_content}'.format(encoded_content=encoded_content)],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            import json
            response = json.loads(result.stdout)
            # 获取 GitHub 上的完整 URL
            download_url = response.get('content', {}).get('download_url')
            if download_url:
                print(f"上传成功！")
                print(f"图片地址: {download_url}")
                return download_url
            else:
                print(f"上传成功，但无法获取 URL")
                return None
        else:
            print(f"上传失败: {result.stderr}")
            return None

    except Exception as e:
        print(f"上传失败，错误信息: {e}")
        return None

if __name__ == "__main__":
    target_app = "Calculator" 
    
    saved_image = monitor_app(target_app)
    
    # ==== GitHub 上传区 ====
    # 如果你想上传到 GitHub 仓库，取消下面四行的注释并填好信息即可开启自动上传：
    # owner = "your-github-username"
    # repo = "your-repo-name"
    # path = os.path.basename(saved_image)
    # upload_to_github(saved_image, owner, repo, path)
    
    print("脚本执行完毕！")
