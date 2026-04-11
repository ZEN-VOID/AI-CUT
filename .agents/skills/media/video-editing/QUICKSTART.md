# Video Editing Skills - 快速开始指南

> **5分钟快速上手** | 从零到执行第一个视频剪辑任务

---

## 📋 前置要求检查清单

在开始之前,请确认以下环境要求:

```bash
# 1. Python版本检查 (必须3.10-3.13)
python3 --version
# ✅ 应显示: Python 3.10.x, 3.11.x, 3.12.x 或 3.13.x
# ❌ 如果是3.14.0或更高,请继续阅读"环境配置"章节

# 2. FFmpeg检查
ffmpeg -version
# ✅ 应显示: ffmpeg version 4.x或更高

# 3. 磁盘空间检查
df -h .
# ✅ 建议至少5GB可用空间
```

**如果任何检查失败,请先查看[环境配置](#环境配置)章节**

---

## 🚀 三步快速启动

### Step 1: 环境配置 (5分钟)

**场景A: Python版本正确 (3.10-3.13)**

```bash
# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate   # Windows

# 安装依赖
pip install moviepy librosa numpy scipy pillow

# 验证安装
python .agents/skills/video-editing/check_installation.py
```

**场景B: Python版本不正确 (需要3.10-3.13)**

```bash
# 使用pyenv安装Python 3.12 (推荐)
brew install pyenv  # macOS
# 或参考: https://github.com/pyenv/pyenv#installation

pyenv install 3.12.0
pyenv local 3.12.0

# 创建虚拟环境
python -m venv venv
source venv/bin/activate

# 安装依赖
pip install moviepy librosa numpy scipy pillow

# 验证安装
python .agents/skills/video-editing/check_installation.py
```

**场景C: 使用Docker (最简单)**

```bash
# 构建镜像
docker build -t video-editing:latest -f .agents/skills/video-editing/Dockerfile .

# 运行容器
docker run -v $(pwd)/tests:/app/tests video-editing:latest python check_installation.py
```

**安装FFmpeg** (如果未安装):

```bash
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt-get update
sudo apt-get install ffmpeg

# Windows
# 下载: https://www.gyan.dev/ffmpeg/builds/
# 添加到PATH环境变量
```

### Step 2: 准备测试数据 (2分钟)

**选项A: 自动生成测试视频** (推荐)

```bash
# 生成3个测试视频 (30秒, 60秒, 90秒)
python tests/prepare_test_data.py --mode generate

# 验证数据
python tests/prepare_test_data.py --mode verify
```

**选项B: 使用自己的视频**

```bash
# 复制视频到测试目录
cp /path/to/your/video.mp4 tests/data/short_video.mp4
```

### Step 3: 运行第一个任务 (3分钟)

**3.1 提取时间戳**

```bash
cd .agents/skills/timestamp-extraction

# 执行基础静音检测
python scripts/plan_executor.py templates/basic-detection.json
```

**预期输出**:
```
🎬 开始执行计划: basic-detection
📋 总任务数: 1

✅ 任务 [basic-001] 完成
📊 检测到 4 个静音片段
📁 输出: output/timestamps/basic-detection/basic_gaps.json

✅ 执行完成! 成功: 1, 失败: 0
```

**3.2 智能剪辑视频**

```bash
cd .agents/skills/video-editing

# 执行播客自动剪辑
python scripts/plan_executor.py templates/podcast-edit.json
```

**预期输出**:
```
🎬 开始执行计划: podcast-template
📋 总任务数: 1

✅ 任务 [podcast-001] 完成
📁 输出视频: output/videos/podcast-final/podcast_final.mp4
⏱️  原始时长: 60秒 → 剪辑后: 45秒 (移除了15秒停顿)

✅ 执行完成! 成功: 1, 失败: 0
```

---

## 🎯 三大核心工作流

### 工作流1: 播客自动剪辑

**场景**: 移除播客中的长时间停顿,保留自然呼吸

```python
from timestamp_extraction.scripts.timestamp_extractor import TimestampExtractor
from video_editing.scripts.video_editor import VideoEditor

# Step 1: 提取停顿时间戳
extractor = TimestampExtractor({
    'silence_threshold': -35,      # dB阈值
    'min_silence_duration': 1.0,   # 最小停顿1秒
    'min_gap_duration': 0.5        # 最小间隔0.5秒
})

result = extractor.process_task({
    'task_id': 'podcast-ts',
    'type': 'silence_detection',
    'input_video': 'tests/data/podcast.mp4',
    'output_path': 'output/timestamps/podcast_gaps.json'
})

print(f"检测到 {len(result['gaps'])} 个停顿片段")

# Step 2: 智能剪辑
editor = VideoEditor({
    'add_transitions': True,
    'default_transition': 'crossfade',
    'transition_duration': 0.3
})

edit_result = editor.process_task({
    'task_id': 'podcast-edit',
    'type': 'podcast_edit',
    'input_video': 'tests/data/podcast.mp4',
    'timestamp_file': 'output/timestamps/podcast_gaps.json',
    'preserve_natural_pauses': True,  # 保留<0.8秒的自然停顿
    'output_path': 'output/videos/podcast_final.mp4'
})

print(f"剪辑完成: {edit_result['output_path']}")
print(f"时长: {edit_result['original_duration']}s → {edit_result['final_duration']}s")
```

### 工作流2: 访谈多机位剪辑

**场景**: 访谈节目,主持人和嘉宾自动切换镜头

```python
# JSON计划模式
{
  "plan_id": "interview-auto-cut",
  "tasks": [{
    "task_id": "interview-001",
    "type": "interview_edit",
    "input_video": "tests/data/interview.mp4",
    "cameras": {
      "host": "tests/data/interview_host_cam.mp4",
      "guest": "tests/data/interview_guest_cam.mp4"
    },
    "switch_mode": "auto",  // 自动检测说话人
    "add_transitions": true,
    "transition_type": "cut",  // 访谈通常用硬切
    "output_path": "output/videos/interview_final.mp4"
  }]
}
```

```bash
python scripts/plan_executor.py plans/interview-auto-cut.json
```

### 工作流3: 音乐蒙太奇

**场景**: 快速剪辑,节拍同步,转场特效

```python
# 使用预设模板
{
  "plan_id": "music-montage",
  "tasks": [{
    "task_id": "montage-001",
    "type": "montage",
    "clips": [
      "input/clip1.mp4",
      "input/clip2.mp4",
      "input/clip3.mp4"
    ],
    "clip_durations": [3.0, 2.5, 3.5],  // 每个片段时长
    "music": {
      "path": "assets/background.mp3",
      "sync_to_beats": true,
      "beat_timestamps": [0.0, 0.5, 1.0, 1.5, 2.0]  // 节拍点
    },
    "effects": {
      "transitions": ["crossfade", "wipe_right", "slide_left"],
      "color_grading": {
        "preset": "cinematic",
        "brightness": 1.1,
        "contrast": 1.2
      }
    },
    "output_path": "output/videos/montage_final.mp4"
  }]
}
```

---

## 🎨 高级功能示例

### 功能1: 场景检测 + 自动切换

```python
# 检测场景变化并在变化处切换镜头
from timestamp_extraction.scripts.timestamp_extractor import TimestampExtractor

extractor = TimestampExtractor()
result = extractor.process_task({
    'task_id': 'scene-detect',
    'type': 'scene_detection',
    'input_video': 'input/movie.mp4',
    'threshold': 30.0,  // 帧差异阈值
    'min_scene_duration': 2.0,  // 最小场景时长
    'output_path': 'output/timestamps/scenes.json'
})

# 结果包含所有场景切换点
for scene in result['scenes']:
    print(f"场景 {scene['scene_id']}: {scene['start']:.2f}s - {scene['end']:.2f}s")
```

### 功能2: 文字叠加 + 动画

```python
# 添加标题和字幕
{
  "task_id": "add-titles",
  "type": "text_overlay",
  "input_video": "input/video.mp4",
  "text_overlays": [
    {
      "type": "title",
      "text": "Episode 1",
      "start": 0,
      "duration": 3,
      "position": "center",
      "animation": "fade_in",
      "style": {
        "fontsize": 72,
        "color": "white",
        "stroke_color": "black",
        "stroke_width": 3
      }
    },
    {
      "type": "lower_third",
      "text": "John Doe - CEO",
      "start": 5,
      "duration": 4,
      "position": "bottom_left",
      "animation": "slide_left"
    }
  ]
}
```

### 功能3: 音频混合 + Ducking

```python
# 背景音乐自动降低音量当有语音时
{
  "task_id": "audio-mix",
  "type": "audio_mixing",
  "input_video": "input/podcast.mp4",
  "background_music": {
    "path": "assets/music.mp3",
    "volume": 0.3,
    "ducking": {
      "enabled": true,
      "threshold": -40,  // 检测语音阈值
      "ratio": 0.2,      // 降低到20%音量
      "fade_duration": 0.5
    }
  },
  "output_path": "output/videos/podcast_with_music.mp4"
}
```

---

## 🔧 常见问题排查

### 问题1: "MoviePy未安装"

```bash
# 检查虚拟环境是否激活
which python
# 应显示: /path/to/venv/bin/python

# 重新安装
pip install --upgrade moviepy

# 如果失败,检查Python版本
python --version
# 必须是3.10-3.13
```

### 问题2: "FFmpeg未找到"

```bash
# 检查FFmpeg是否在PATH中
which ffmpeg

# macOS重新安装
brew reinstall ffmpeg

# Linux重新安装
sudo apt-get install --reinstall ffmpeg

# 手动指定FFmpeg路径
export FFMPEG_BINARY=/usr/local/bin/ffmpeg
```

### 问题3: "视频处理慢"

```bash
# 使用GPU加速 (NVIDIA)
pip install moviepy[optional]

# 检查GPU是否可用
nvidia-smi

# 在任务配置中启用GPU
{
  "config": {
    "gpu_acceleration": true,
    "threads": 4
  }
}
```

### 问题4: "内存不足"

```python
# 对于大文件,使用subclip分段处理
from moviepy.editor import VideoFileClip

def process_large_video(input_path, output_path):
    """分段处理大视频"""
    clip = VideoFileClip(input_path)
    duration = clip.duration

    # 每10分钟一段
    segment_duration = 600
    segments = []

    for i in range(0, int(duration), segment_duration):
        start = i
        end = min(i + segment_duration, duration)
        segment = clip.subclip(start, end)
        segments.append(segment)

    # 处理每一段...
    clip.close()
```

---

## 📚 下一步学习

### 初级 (已完成快速开始)
- ✅ 环境配置
- ✅ 第一个任务执行
- ✅ 基础工作流

### 中级 (深入学习)
- 📖 阅读 `SKILL.md` - 完整API文档
- 📖 阅读 `reference.md` - 高级配置
- 🧪 运行 `TESTING.md` 中的9个测试用例

### 高级 (自定义开发)
- 📖 阅读 `DEPLOYMENT.md` - 生产部署
- 🔧 自定义转场效果
- 🔧 开发新的剪辑模式
- 🔧 集成C5/C6智能体

---

## 🎯 性能优化建议

### 开发环境
```python
config = {
    'quality': 'medium',
    'preset': 'fast',
    'threads': 2,
    'gpu_acceleration': False
}
```

### 生产环境
```python
config = {
    'quality': 'high',
    'preset': 'slow',
    'threads': 8,
    'gpu_acceleration': True,
    'bitrate': '10M'
}
```

---

## 📞 获取帮助

- **完整文档**: `.agents/skills/video-editing/SKILL.md`
- **测试指南**: `.agents/skills/video-editing/TESTING.md`
- **部署指南**: `.agents/skills/video-editing/DEPLOYMENT.md`
- **验证报告**: `.agents/skills/video-editing/VALIDATION_REPORT.md`

---

**快速开始完成!** 🎉

现在您已经掌握了Video Editing Skills的基础使用。继续探索高级功能,或查看完整文档深入学习。
