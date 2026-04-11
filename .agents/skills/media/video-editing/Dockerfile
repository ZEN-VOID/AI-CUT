# Video Editing Skills - Docker环境
#
# 使用方法:
#   docker build -t video-editing:latest -f .agents/skills/video-editing/Dockerfile .
#   docker run -v $(pwd)/tests:/app/tests video-editing:latest python check_installation.py

FROM python:3.12-slim

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

# 设置工作目录
WORKDIR /app

# 复制依赖文件
COPY .agents/skills/video-editing/requirements.txt /app/requirements.txt
COPY .agents/skills/timestamp-extraction/requirements.txt /app/requirements-ts.txt

# 安装Python依赖
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir -r requirements-ts.txt

# 复制Skills代码
COPY .agents/skills/video-editing /app/video-editing
COPY .agents/skills/timestamp-extraction /app/timestamp-extraction

# 设置环境变量
ENV PYTHONPATH=/app/video-editing:/app/timestamp-extraction:$PYTHONPATH

# 默认命令
CMD ["python", "/app/video-editing/check_installation.py"]
