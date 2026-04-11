# Video Editing Skills - 部署指南

> **版本**: v1.0.0 | **更新时间**: 2025-10-26
> **适用系统**: macOS, Linux, Windows
> **Python版本**: 3.8+

---

## 📋 目录

- [1. 系统要求](#1-系统要求)
- [2. 快速安装](#2-快速安装)
- [3. 详细安装步骤](#3-详细安装步骤)
- [4. 环境配置](#4-环境配置)
- [5. 验证安装](#5-验证安装)
- [6. 性能优化](#6-性能优化)
- [7. 故障排除](#7-故障排除)
- [8. 生产环境部署](#8-生产环境部署)

---

## 1. 系统要求

### 1.1 硬件要求

**最低配置**:
```yaml
CPU: 双核 2.0GHz+
内存: 8GB RAM
存储: 10GB 可用空间
显卡: 集成显卡（软件编码）
```

**推荐配置**:
```yaml
CPU: 四核 3.0GHz+ (支持AVX2指令集)
内存: 16GB+ RAM
存储: 50GB+ SSD
显卡: NVIDIA GPU (支持CUDA) / Apple Silicon GPU
```

**高性能配置**:
```yaml
CPU: 8核+ 3.5GHz+ (Intel i7/i9, AMD Ryzen 7/9)
内存: 32GB+ RAM
存储: 100GB+ NVMe SSD
显卡: NVIDIA RTX系列 (8GB+ VRAM) / Apple M1/M2/M3
```

### 1.2 软件要求

**必需软件**:
- Python 3.8 或更高版本
- FFmpeg 4.0 或更高版本
- pip (Python包管理器)

**可选软件**:
- CUDA Toolkit 11.0+ (NVIDIA GPU加速)
- Git (版本控制)
- Virtual Environment (Python虚拟环境)

### 1.3 操作系统支持

| 操作系统 | 版本要求 | 状态 | 说明 |
|---------|---------|------|------|
| macOS | 11.0+ (Big Sur+) | ✅ 完全支持 | 推荐M1/M2/M3芯片 |
| Linux | Ubuntu 20.04+, Debian 10+ | ✅ 完全支持 | 推荐Ubuntu 22.04 |
| Windows | Windows 10/11 | ✅ 完全支持 | 需要安装FFmpeg |
| Docker | - | ✅ 支持 | 见Docker部署章节 |

---

## 2. 快速安装

### 2.1 一键安装脚本

**macOS / Linux**:
```bash
#!/bin/bash
# 快速安装脚本

# 1. 检查Python版本
python3 --version

# 2. 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 3. 安装Python依赖
pip install --upgrade pip
pip install moviepy numpy scipy librosa pillow

# 4. 安装FFmpeg
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    brew install ffmpeg
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux
    sudo apt-get update
    sudo apt-get install -y ffmpeg
fi

# 5. 验证安装
ffmpeg -version
python -c "import moviepy; print('MoviePy version:', moviepy.__version__)"

echo "✅ 安装完成!"
```

保存为 `install.sh`，然后执行：
```bash
chmod +x install.sh
./install.sh
```

**Windows**:
```powershell
# PowerShell快速安装脚本

# 1. 检查Python版本
python --version

# 2. 创建虚拟环境
python -m venv venv
.\venv\Scripts\Activate.ps1

# 3. 安装Python依赖
pip install --upgrade pip
pip install moviepy numpy scipy librosa pillow

# 4. 下载FFmpeg
Write-Host "请手动下载并安装FFmpeg:"
Write-Host "https://ffmpeg.org/download.html#build-windows"
Write-Host "并将ffmpeg.exe添加到系统PATH"

# 5. 验证安装
ffmpeg -version
python -c "import moviepy; print('MoviePy version:', moviepy.__version__)"

Write-Host "✅ 安装完成!"
```

---

## 3. 详细安装步骤

### 3.1 安装Python

#### macOS

**方法1: 使用Homebrew（推荐）**
```bash
# 安装Homebrew（如果未安装）
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 安装Python
brew install python@3.11

# 验证安装
python3 --version
```

**方法2: 从官网下载**
- 访问 https://www.python.org/downloads/
- 下载 macOS 安装包
- 运行安装程序

#### Linux (Ubuntu/Debian)

```bash
# 更新包列表
sudo apt-get update

# 安装Python 3.11
sudo apt-get install -y python3.11 python3.11-venv python3.11-dev

# 安装pip
sudo apt-get install -y python3-pip

# 验证安装
python3.11 --version
pip3 --version
```

#### Windows

1. 访问 https://www.python.org/downloads/windows/
2. 下载 Python 3.11 安装程序
3. 运行安装程序
4. **重要**: 勾选 "Add Python to PATH"
5. 验证安装：
   ```powershell
   python --version
   pip --version
   ```

### 3.2 安装FFmpeg

#### macOS

**方法1: 使用Homebrew（推荐）**
```bash
brew install ffmpeg
```

**方法2: 下载预编译二进制**
```bash
# 下载
curl -O https://evermeet.cx/ffmpeg/ffmpeg-6.0.zip

# 解压
unzip ffmpeg-6.0.zip

# 移动到系统路径
sudo mv ffmpeg /usr/local/bin/

# 验证
ffmpeg -version
```

#### Linux (Ubuntu/Debian)

**方法1: 使用apt（推荐）**
```bash
sudo apt-get update
sudo apt-get install -y ffmpeg
```

**方法2: 从PPA安装最新版本**
```bash
sudo add-apt-repository ppa:jonathonf/ffmpeg-4
sudo apt-get update
sudo apt-get install -y ffmpeg
```

**方法3: 从源码编译**
```bash
# 安装依赖
sudo apt-get install -y \
    build-essential \
    yasm \
    libx264-dev \
    libx265-dev \
    libvpx-dev \
    libfdk-aac-dev \
    libmp3lame-dev \
    libopus-dev

# 下载源码
wget https://ffmpeg.org/releases/ffmpeg-6.0.tar.bz2
tar -xf ffmpeg-6.0.tar.bz2
cd ffmpeg-6.0

# 配置和编译
./configure --enable-gpl --enable-libx264 --enable-libx265 --enable-libvpx
make -j$(nproc)
sudo make install

# 验证
ffmpeg -version
```

#### Windows

**方法1: 下载预编译二进制（推荐）**

1. 访问 https://www.gyan.dev/ffmpeg/builds/
2. 下载 `ffmpeg-release-full.7z`
3. 解压到 `C:\ffmpeg`
4. 添加到系统PATH：
   - 右键 "此电脑" → "属性"
   - "高级系统设置" → "环境变量"
   - 编辑 "Path"，添加 `C:\ffmpeg\bin`
5. 验证：
   ```powershell
   ffmpeg -version
   ```

**方法2: 使用Chocolatey**
```powershell
# 安装Chocolatey（如果未安装）
Set-ExecutionPolicy Bypass -Scope Process -Force
iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))

# 安装FFmpeg
choco install ffmpeg

# 验证
ffmpeg -version
```

### 3.3 安装Python依赖

#### 创建虚拟环境（推荐）

**macOS / Linux**:
```bash
# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境
source venv/bin/activate

# 升级pip
pip install --upgrade pip
```

**Windows**:
```powershell
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
.\venv\Scripts\Activate.ps1

# 升级pip
pip install --upgrade pip
```

#### 安装核心依赖

```bash
# 核心依赖包
pip install moviepy==1.0.3
pip install numpy==1.24.3
pip install scipy==1.10.1
pip install librosa==0.10.0
pip install pillow==10.0.0

# 可选依赖（性能优化）
pip install numba==0.57.0        # 加速librosa
pip install soundfile==0.12.1    # 音频I/O
pip install imageio-ffmpeg==0.4.9 # FFmpeg绑定
```

#### 使用requirements.txt

创建 `requirements.txt`:
```text
# 核心依赖
moviepy==1.0.3
numpy==1.24.3
scipy==1.10.1
librosa==0.10.0
pillow==10.0.0

# 性能优化
numba==0.57.0
soundfile==0.12.1
imageio-ffmpeg==0.4.9

# 开发依赖
pytest==7.4.0
pytest-cov==4.1.0
black==23.7.0
flake8==6.0.0
```

安装：
```bash
pip install -r requirements.txt
```

### 3.4 GPU加速支持（可选）

#### NVIDIA CUDA（Linux/Windows）

**1. 安装CUDA Toolkit**
```bash
# Ubuntu 22.04
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-ubuntu2204.pin
sudo mv cuda-ubuntu2204.pin /etc/apt/preferences.d/cuda-repository-pin-600
wget https://developer.download.nvidia.com/compute/cuda/12.0.0/local_installers/cuda-repo-ubuntu2204-12-0-local_12.0.0-525.60.13-1_amd64.deb
sudo dpkg -i cuda-repo-ubuntu2204-12-0-local_12.0.0-525.60.13-1_amd64.deb
sudo cp /var/cuda-repo-ubuntu2204-12-0-local/cuda-*-keyring.gpg /usr/share/keyrings/
sudo apt-get update
sudo apt-get -y install cuda
```

**2. 配置FFmpeg CUDA支持**
```bash
# 编译FFmpeg with CUDA
./configure --enable-cuda-nvcc --enable-cuvid --enable-nvenc --enable-nonfree
make -j$(nproc)
sudo make install
```

**3. 验证CUDA**
```bash
nvidia-smi
nvcc --version
```

#### Apple Silicon GPU（macOS M1/M2/M3）

```bash
# 确保使用Apple Silicon原生Python
arch -arm64 python3 --version

# 安装优化的依赖
pip install --no-binary :all: numpy
pip install --no-binary :all: scipy

# FFmpeg自动使用VideoToolbox硬件加速
```

---

## 4. 环境配置

### 4.1 创建配置文件

创建 `.env` 文件（可选）:
```bash
# FFmpeg路径（如果不在PATH中）
FFMPEG_BINARY=/usr/local/bin/ffmpeg
FFPROBE_BINARY=/usr/local/bin/ffprobe

# 临时文件目录
TEMP_DIR=/tmp/video_editing

# 日志级别
LOG_LEVEL=INFO

# 硬件加速
USE_GPU=true
GPU_TYPE=cuda  # 或 videotoolbox (macOS)

# 性能设置
MAX_THREADS=8
CHUNK_SIZE=1000
```

### 4.2 配置MoviePy

创建 `~/.moviepy_config`:
```python
# MoviePy配置文件
{
    "FFMPEG_BINARY": "/usr/local/bin/ffmpeg",
    "IMAGEMAGICK_BINARY": "/usr/local/bin/convert"
}
```

### 4.3 设置Python路径

**macOS / Linux**:
```bash
# 添加到 ~/.bashrc 或 ~/.zshrc
export PYTHONPATH="${PYTHONPATH}:/path/to/AIGC数字游牧派影视文化公司/.agents/skills"
export PATH="${PATH}:/path/to/AIGC数字游牧派影视文化公司/.agents/skills/video-editing/scripts"
```

**Windows**:
```powershell
# 添加到系统环境变量
$env:PYTHONPATH = "C:\path\to\AIGC数字游牧派影视文化公司\.gemini\skills"
```

---

## 5. 验证安装

### 5.1 系统检查脚本

创建 `check_installation.py`:
```python
#!/usr/bin/env python3
"""
安装验证脚本
检查所有依赖是否正确安装
"""

import sys
import subprocess

def check_python_version():
    """检查Python版本"""
    version = sys.version_info
    if version.major == 3 and version.minor >= 8:
        print(f"✅ Python版本: {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"❌ Python版本过低: {version.major}.{version.minor}.{version.micro}")
        print("   需要Python 3.8+")
        return False

def check_ffmpeg():
    """检查FFmpeg"""
    try:
        result = subprocess.run(['ffmpeg', '-version'],
                              capture_output=True, text=True)
        version_line = result.stdout.split('\n')[0]
        print(f"✅ FFmpeg: {version_line}")
        return True
    except FileNotFoundError:
        print("❌ FFmpeg未找到")
        print("   请安装FFmpeg: https://ffmpeg.org/download.html")
        return False

def check_python_packages():
    """检查Python包"""
    packages = {
        'moviepy': '1.0.3',
        'numpy': '1.24.3',
        'scipy': '1.10.1',
        'librosa': '0.10.0',
        'PIL': '10.0.0'  # Pillow
    }

    all_ok = True

    for package, expected_version in packages.items():
        try:
            if package == 'PIL':
                import PIL
                version = PIL.__version__
                package_name = 'Pillow'
            else:
                module = __import__(package)
                version = module.__version__
                package_name = package

            print(f"✅ {package_name}: {version}")

        except ImportError:
            print(f"❌ {package} 未安装")
            all_ok = False

    return all_ok

def check_gpu_support():
    """检查GPU支持"""
    try:
        # 检查NVIDIA GPU
        result = subprocess.run(['nvidia-smi'],
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ NVIDIA GPU检测成功")
            gpu_lines = [l for l in result.stdout.split('\n') if 'CUDA' in l]
            if gpu_lines:
                print(f"   {gpu_lines[0].strip()}")
            return True
    except FileNotFoundError:
        pass

    # 检查Apple Silicon
    try:
        result = subprocess.run(['sysctl', '-n', 'machdep.cpu.brand_string'],
                              capture_output=True, text=True)
        if 'Apple' in result.stdout:
            print(f"✅ Apple Silicon: {result.stdout.strip()}")
            return True
    except:
        pass

    print("⚠️  未检测到GPU（将使用CPU编码）")
    return False

def main():
    """主函数"""
    print("=" * 60)
    print("Video Editing Skills - 安装验证")
    print("=" * 60 + "\n")

    results = []

    print("检查Python版本...")
    results.append(check_python_version())

    print("\n检查FFmpeg...")
    results.append(check_ffmpeg())

    print("\n检查Python包...")
    results.append(check_python_packages())

    print("\n检查GPU支持...")
    check_gpu_support()  # 不计入结果

    print("\n" + "=" * 60)
    if all(results):
        print("✅ 所有依赖检查通过!")
        print("=" * 60)
        return 0
    else:
        print("❌ 部分依赖检查失败，请查看上方错误信息")
        print("=" * 60)
        return 1

if __name__ == '__main__':
    sys.exit(main())
```

运行验证：
```bash
python check_installation.py
```

### 5.2 功能测试

**测试时间戳提取**:
```bash
# 创建测试视频（如果没有）
ffmpeg -f lavfi -i testsrc=duration=30:size=1280x720:rate=30 \
       -f lavfi -i sine=frequency=1000:duration=30 \
       test_video.mp4

# 运行时间戳提取
python .agents/skills/timestamp-extraction/scripts/timestamp_extractor.py \
    test_video.mp4
```

**测试视频剪辑**:
```bash
# 运行视频剪辑
python .agents/skills/video-editing/scripts/video_editor.py \
    test_video.mp4 \
    output/timestamp-extraction/test_video_gaps.json
```

---

## 6. 性能优化

### 6.1 硬件加速配置

#### NVIDIA GPU (NVENC)

```python
# 在video_editor.py中配置
NVENC_CONFIG = {
    'codec': 'h264_nvenc',
    'preset': 'p4',  # p1-p7, p4平衡质量和速度
    'threads': 0,    # 自动
    'hardware_accel': True
}

editor = VideoEditor(NVENC_CONFIG)
```

#### Apple Silicon (VideoToolbox)

```python
# 自动使用VideoToolbox
VIDEOTOOLBOX_CONFIG = {
    'codec': 'h264_videotoolbox',
    'preset': 'medium',
    'hardware_accel': True
}

editor = VideoEditor(VIDEOTOOLBOX_CONFIG)
```

#### Intel Quick Sync

```python
QSV_CONFIG = {
    'codec': 'h264_qsv',
    'preset': 'medium',
    'hardware_accel': True
}

editor = VideoEditor(QSV_CONFIG)
```

### 6.2 并行处理优化

```python
# 配置多线程
config = {
    'threads': 8,  # CPU核心数
    'chunk_processing': True,
    'chunk_size': 1000  # 帧数
}
```

### 6.3 内存优化

```python
# 配置内存限制
config = {
    'processing_resolution': '720p',  # 处理时降低分辨率
    'output_resolution': '1080p',     # 输出时升级
    'max_memory_mb': 4096             # 最大内存使用
}
```

---

## 7. 故障排除

### 7.1 常见问题

#### 问题1: "FFmpeg not found"

**症状**:
```
FileNotFoundError: [Errno 2] No such file or directory: 'ffmpeg'
```

**解决方案**:
```bash
# 检查FFmpeg是否在PATH中
which ffmpeg  # macOS/Linux
where ffmpeg  # Windows

# 如果未找到，重新安装
brew install ffmpeg  # macOS
sudo apt-get install ffmpeg  # Linux

# 或手动指定路径
export FFMPEG_BINARY=/path/to/ffmpeg
```

#### 问题2: "MoviePy ImportError"

**症状**:
```
ImportError: No module named 'moviepy'
```

**解决方案**:
```bash
# 确保虚拟环境已激活
source venv/bin/activate  # macOS/Linux
.\venv\Scripts\Activate.ps1  # Windows

# 重新安装MoviePy
pip install --upgrade moviepy
```

#### 问题3: 内存不足

**症状**:
```
MemoryError: Unable to allocate array
```

**解决方案**:
```python
# 降低处理分辨率
config = {
    'processing_resolution': '480p',  # 从1080p降到480p
    'chunk_processing': True,
    'chunk_size': 500
}
```

#### 问题4: GPU编码失败

**症状**:
```
Error: Encoder 'h264_nvenc' not found
```

**解决方案**:
```bash
# 检查GPU驱动
nvidia-smi  # NVIDIA

# 重新编译FFmpeg with CUDA
./configure --enable-cuda-nvcc --enable-nvenc
make && sudo make install

# 或降级到CPU编码
config = {'codec': 'libx264', 'hardware_accel': False}
```

#### 问题5: 音频同步问题

**症状**: 输出视频音画不同步

**解决方案**:
```python
# 强制音频同步
config = {
    'audio_sync': True,
    'fps': 30  # 确保帧率一致
}

# 或重新编码音频
result = editor.add_audio_mix(
    ...,
    audio_codec='aac',
    audio_bitrate='192k'
)
```

### 7.2 日志调试

#### 启用详细日志

```python
import logging

# 配置日志
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('video_editing_debug.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger('video_editing')
```

#### 查看FFmpeg输出

```python
# VideoEditor配置
config = {
    'verbose': True,  # 显示FFmpeg输出
    'logger': logger
}
```

---

## 8. 生产环境部署

### 8.1 Docker部署

#### Dockerfile

```dockerfile
FROM python:3.11-slim

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

# 设置工作目录
WORKDIR /app

# 复制依赖文件
COPY requirements.txt .

# 安装Python依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制Skills目录
COPY .agents/skills/timestamp-extraction /app/timestamp-extraction
COPY .agents/skills/video-editing /app/video-editing

# 设置环境变量
ENV PYTHONPATH=/app
ENV TEMP_DIR=/tmp/video_editing

# 创建临时目录
RUN mkdir -p /tmp/video_editing

# 默认命令
CMD ["python", "-m", "video_editing.scripts.plan_executor"]
```

#### docker-compose.yml

```yaml
version: '3.8'

services:
  video-editing:
    build: .
    container_name: video-editing
    volumes:
      - ./input:/app/input:ro
      - ./output:/app/output:rw
      - ./plans:/app/plans:ro
    environment:
      - LOG_LEVEL=INFO
      - MAX_THREADS=4
    restart: unless-stopped

  # GPU版本
  video-editing-gpu:
    build:
      context: .
      dockerfile: Dockerfile.gpu
    container_name: video-editing-gpu
    runtime: nvidia
    environment:
      - NVIDIA_VISIBLE_DEVICES=all
      - USE_GPU=true
    volumes:
      - ./input:/app/input:ro
      - ./output:/app/output:rw
```

#### 构建和运行

```bash
# 构建镜像
docker build -t video-editing:latest .

# 运行容器
docker run -v $(pwd)/input:/app/input \
           -v $(pwd)/output:/app/output \
           video-editing:latest

# 使用docker-compose
docker-compose up -d
```

### 8.2 云服务器部署

#### AWS EC2

```bash
# 1. 启动实例 (推荐p3.2xlarge for GPU)
aws ec2 run-instances \
    --image-id ami-0c55b159cbfafe1f0 \
    --instance-type p3.2xlarge \
    --key-name my-key

# 2. SSH登录
ssh -i my-key.pem ubuntu@<instance-ip>

# 3. 安装CUDA
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/cuda-ubuntu2004.pin
sudo mv cuda-ubuntu2004.pin /etc/apt/preferences.d/cuda-repository-pin-600
sudo apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/3bf863cc.pub
sudo add-apt-repository "deb https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/ /"
sudo apt-get update
sudo apt-get -y install cuda

# 4. 安装依赖
sudo apt-get install -y python3-pip ffmpeg
pip3 install -r requirements.txt

# 5. 运行服务
python3 -m video_editing.scripts.plan_executor
```

#### Google Cloud Platform

```bash
# 使用gcloud CLI
gcloud compute instances create video-editing \
    --machine-type=n1-standard-8 \
    --accelerator=type=nvidia-tesla-t4,count=1 \
    --image-family=ubuntu-2004-lts \
    --image-project=ubuntu-os-cloud \
    --boot-disk-size=50GB

# SSH登录
gcloud compute ssh video-editing

# 安装依赖（同AWS）
```

### 8.3 自动化部署

#### Ansible Playbook

```yaml
# deploy.yml
---
- name: Deploy Video Editing Skills
  hosts: video_servers
  become: yes

  tasks:
    - name: Update apt cache
      apt:
        update_cache: yes

    - name: Install system packages
      apt:
        name:
          - python3
          - python3-pip
          - ffmpeg
          - nvidia-cuda-toolkit
        state: present

    - name: Create app directory
      file:
        path: /opt/video-editing
        state: directory
        mode: '0755'

    - name: Copy application files
      copy:
        src: .agents/skills/
        dest: /opt/video-editing/
        mode: '0755'

    - name: Install Python requirements
      pip:
        requirements: /opt/video-editing/requirements.txt
        executable: pip3

    - name: Configure systemd service
      template:
        src: video-editing.service.j2
        dest: /etc/systemd/system/video-editing.service

    - name: Start service
      systemd:
        name: video-editing
        state: started
        enabled: yes
```

运行部署：
```bash
ansible-playbook -i inventory.ini deploy.yml
```

### 8.4 监控和日志

#### Prometheus监控

```python
# 添加到video_editor.py
from prometheus_client import Counter, Histogram, Gauge

# 指标
videos_processed = Counter('videos_processed_total', 'Total videos processed')
processing_time = Histogram('video_processing_seconds', 'Video processing time')
active_tasks = Gauge('active_editing_tasks', 'Number of active editing tasks')

# 在process_task中使用
@processing_time.time()
def process_task(self, task):
    active_tasks.inc()
    try:
        # 处理逻辑
        result = ...
        videos_processed.inc()
        return result
    finally:
        active_tasks.dec()
```

#### ELK日志聚合

```python
# 配置日志发送到Elasticsearch
import logging
from elasticapm.handlers.logging import LoggingHandler

handler = LoggingHandler()
handler.setLevel(logging.INFO)
logger.addHandler(handler)
```

---

## 总结

本部署指南涵盖了：

- ✅ 完整的系统要求和硬件推荐
- ✅ macOS/Linux/Windows详细安装步骤
- ✅ GPU加速配置（NVIDIA/Apple Silicon/Intel）
- ✅ 环境配置和验证
- ✅ 性能优化建议
- ✅ 故障排除方案
- ✅ Docker和云服务器部署
- ✅ 生产环境监控

建议部署流程：

1. **本地开发**: 按照快速安装完成基础环境
2. **功能验证**: 运行验证脚本确保所有依赖正常
3. **性能调优**: 根据硬件配置GPU加速
4. **测试环境**: 使用Docker部署测试环境
5. **生产部署**: 云服务器部署 + 监控告警
6. **持续优化**: 根据监控数据调整配置

---

**文档版本**: v1.0.0
**最后更新**: 2025-10-26
**维护者**: 制作组
