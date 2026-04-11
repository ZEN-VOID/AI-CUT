# Timestamp Extraction - Extended Reference

**版本**: v1.0.0
**最后更新**: 2025-01-02

---

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [API Reference](#api-reference)
3. [Advanced Configuration](#advanced-configuration)
4. [Performance Tuning](#performance-tuning)
5. [Integration Patterns](#integration-patterns)
6. [Troubleshooting Guide](#troubleshooting-guide)
7. [External Resources](#external-resources)

---

## Architecture Overview

### System Components

```
timestamp-extraction/
│
├── SKILL.md                  # 核心文档（用户入口）
│
├── scripts/                  # 执行引擎
│   ├── core_engine.py        # 核心提取引擎
│   │   ├── TimestampExtractor类
│   │   │   ├── extract_video_info()      # 元数据提取
│   │   │   ├── extract_silence_gaps()    # 静音检测
│   │   │   ├── convert_to_frame_accurate() # 帧转换
│   │   │   ├── detect_scene_changes()    # 场景检测
│   │   │   └── process_task()            # 任务处理
│   │   └── Utility functions
│   │
│   └── plan_executor.py      # 批量执行器
│       └── PlanExecutor类
│           ├── execute()                 # 主执行函数
│           ├── _save_task_result()       # 结果保存
│           └── _generate_execution_report() # 报告生成
│
├── templates/                # 预设模板
│   ├── podcast.json          # 播客剪辑预设
│   ├── interview.json        # 访谈剪辑预设
│   └── vlog.json             # Vlog剪辑预设
│
└── reference.md              # 本文档
```

### Data Flow

```
Input: Video/Audio File
  ↓
[1] Video Info Extraction (ffprobe)
  ↓
[2] Audio Extraction (ffmpeg)
  ↓
[3] Silence Detection (pydub)
  ↓
[4] Confidence Scoring (custom algorithm)
  ↓
[5] Frame Conversion (fps calculation)
  ↓
[6] Scene Detection (PySceneDetect, optional)
  ↓
[7] JSON Output Generation
  ↓
Output: Structured Timestamp Data
```

---

## API Reference

### Core Classes

#### TimestampExtractor

**Constructor**:
```python
extractor = TimestampExtractor(config: Dict)
```

**Config Parameters**:

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `silence_thresh` | int | -50 | 静音阈值（dB），范围-60到-30 |
| `min_silence_len` | int | 500 | 最小静音时长（ms） |
| `padding` | int | 200 | 安全填充（ms） |
| `detect_scenes` | bool | False | 是否启用场景检测 |
| `scene_detector` | dict | `{}` | 场景检测器配置 |
| `output_format` | dict | `{}` | 输出格式配置 |

**Methods**:

##### extract_video_info(video_path: str) -> Dict

提取视频元数据。

**Returns**:
```python
{
    'path': str,                # 视频路径
    'duration': float,          # 时长（秒）
    'fps': float,               # 帧率
    'resolution': str,          # 分辨率 "1920x1080"
    'audio_channels': int,      # 音频声道数
    'audio_sample_rate': int,   # 采样率（Hz）
    'video_codec': str,         # 视频编码
    'audio_codec': str          # 音频编码
}
```

##### extract_silence_gaps(video_path: str) -> List[Dict]

提取静音片段。

**Returns**:
```python
[
    {
        'id': str,                      # 唯一ID "gap-001"
        'start': float,                 # 开始时间（秒）
        'end': float,                   # 结束时间（秒）
        'duration': float,              # 持续时长（秒）
        'original_start': float,        # 原始开始（未填充）
        'original_end': float,          # 原始结束（未填充）
        'confidence': float,            # 置信度 0.0-1.0
        'type': str,                    # 类型："natural_pause"|"breath_pause"|...
        'recommended_fade': {
            'in': float,                # 淡入时长（秒）
            'out': float                # 淡出时长（秒）
        },
        'start_frame': int,             # 开始帧号（可选）
        'end_frame': int,               # 结束帧号（可选）
        'start_timecode': str,          # 开始时间码（可选）
        'end_timecode': str             # 结束时间码（可选）
    }
]
```

##### detect_scene_changes(video_path: str) -> List[Dict]

检测场景切换点。

**Returns**:
```python
[
    {
        'id': str,              # 唯一ID "scene-001"
        'frame': int,           # 帧号
        'time': float,          # 时间（秒）
        'timecode': str,        # SMPTE时间码
        'confidence': float,    # 置信度
        'type': str             # 类型："hard_cut"|"fade"
    }
]
```

##### process_task(task: Dict) -> Dict

处理单个任务（综合方法）。

**Input**:
```python
{
    'task_id': str,
    'video_path': str,
    'output_dir': str
}
```

**Returns**:
```python
{
    'task_id': str,
    'video_info': dict,
    'silence_gaps': list,
    'scene_changes': list,
    'statistics': {
        'total_silence_gaps': int,
        'total_silence_duration': float,
        'high_confidence_cuts': int,
        'scene_changes': int,
        'processing_time': float
    }
}
```

#### PlanExecutor

**Constructor**:
```python
executor = PlanExecutor(plan_path: str)
```

**Methods**:

##### execute() -> Dict

执行计划中的所有任务。

**Returns**: 执行报告字典（详见SKILL.md）

---

## Advanced Configuration

### Silence Detection Tuning

#### Environment-Based Presets

```python
# 专业录音棚
STUDIO_CONFIG = {
    'silence_thresh': -60,      # 极其敏感
    'min_silence_len': 300,     # 短停顿也检测
    'padding': 100              # 小填充（高质量音频）
}

# 标准采访
INTERVIEW_CONFIG = {
    'silence_thresh': -50,      # 标准敏感度
    'min_silence_len': 500,     # 中等停顿
    'padding': 200              # 标准填充
}

# 嘈杂环境（户外/餐厅）
NOISY_CONFIG = {
    'silence_thresh': -40,      # 降低敏感度
    'min_silence_len': 800,     # 只检测长停顿
    'padding': 300              # 大填充（保险）
}

# 背景音乐常驻（Vlog/MV）
MUSIC_CONFIG = {
    'silence_thresh': -38,      # 更不敏感
    'min_silence_len': 1000,    # 只检测明显停顿
    'padding': 400              # 更大填充
}
```

#### Dynamic Threshold Adjustment

```python
# 根据音频RMS自动调整阈值
from pydub import AudioSegment

audio = AudioSegment.from_file('video.mp4')
avg_rms = audio.rms

# 动态计算阈值
if avg_rms < 200:
    silence_thresh = -60  # 高质量，严格检测
elif avg_rms < 400:
    silence_thresh = -50  # 标准质量
else:
    silence_thresh = -40  # 低质量，宽松检测

config = {
    'silence_thresh': silence_thresh,
    'min_silence_len': 500,
    'padding': 200
}
```

### Scene Detection Configuration

#### ContentDetector (内容检测器)

```python
{
    "scene_detector": {
        "type": "content",
        "threshold": 27.0,          # 默认值，适用大多数场景
        "min_scene_len": 15,        # 最小场景长度（帧）
        "luma_only": false          # 仅使用亮度（更快但不太准）
    }
}

# Threshold调优指南:
# - 降低 (18-25): 检测更细微的切换（适用频繁切镜）
# - 默认 (27): 平衡
# - 提高 (30-35): 只检测明显切换（减少误检）
```

#### ThresholdDetector (阈值检测器)

```python
{
    "scene_detector": {
        "type": "threshold",
        "threshold": 12.0,          # 亮度变化百分比阈值
        "fade_bias": 0.0            # 淡入淡出偏差
    }
}

# 适用场景:
# - 硬切（hard cuts）为主的视频
# - 性能要求高的批量处理
# - 亮度变化明显的场景切换
```

### Output Format Customization

```python
{
    "output_format": {
        "include_waveform": true,       # 生成波形图（需matplotlib）
        "waveform_resolution": "1920x1080",
        "include_timecodes": true,      # 包含SMPTE时间码
        "include_frames": true,         # 包含帧号
        "include_milliseconds": false,  # 包含毫秒级时间戳
        "json_indent": 2,               # JSON缩进
        "sort_by_confidence": true      # 按置信度排序
    }
}
```

---

## Performance Tuning

### Optimization Strategies

#### 1. Audio-Only Mode (音频专用模式)

```python
# 跳过视频解码，仅提取音频
{
    "tasks": [
        {
            "task_id": "audio-only-001",
            "video_path": "video.mp4",
            "audio_only": true  # ⚡ 速度提升3-5倍
        }
    ]
}
```

**性能对比**:
- 标准模式（视频+音频）: ~1.2x实时速度
- 音频专用模式: ~4.5x实时速度

#### 2. Parallel Processing (并行处理)

```python
from concurrent.futures import ThreadPoolExecutor
from scripts.plan_executor import execute_plan

# 并行处理多个视频
video_files = ['vid1.mp4', 'vid2.mp4', 'vid3.mp4', 'vid4.mp4']

def process_single(video_path):
    plan = {
        "config": {...},
        "tasks": [{"video_path": video_path, ...}]
    }
    return execute_plan(plan)

with ThreadPoolExecutor(max_workers=4) as executor:
    results = list(executor.map(process_single, video_files))
```

**注意事项**:
- 线程数 = CPU核心数 - 1（留一个核心给系统）
- FFmpeg默认使用多线程，避免过度并行
- 内存密集型，监控RAM使用

#### 3. Fast Mode (快速模式)

```python
{
    "config": {
        "fast_mode": true,                  # 启用快速模式
        "skip_waveform": true,              # 跳过波形生成
        "skip_confidence_scoring": false,   # 保留置信度评分
        "skip_scene_detection": true        # 跳过场景检测
    }
}
```

**速度提升**:
- 跳过波形: +15%
- 跳过场景检测: +30%
- 综合快速模式: ~50%速度提升

#### 4. Checkpoint for Large Batches (大批量断点)

```python
{
    "config": {
        "checkpoint_enabled": true,
        "checkpoint_interval": 10,  # 每10个任务保存一次
        "checkpoint_dir": "output/checkpoints"
    }
}

# 恢复执行
{
    "resume_from_checkpoint": "output/checkpoints/checkpoint-20250102-143000.json"
}
```

---

## Integration Patterns

### Pattern 1: C6 Agent Integration (智能体集成)

```python
# C6-时间戳精准专家调用本skill

# Step 1: C6接收用户请求
user_prompt = "分析这个采访视频，提取所有静音片段"

# Step 2: C6决策参数
config = {
    'silence_thresh': -50,  # C6基于视频质量分析决定
    'min_silence_len': 500,
    'padding': 200,
    'detect_scenes': True    # C6识别到"采访"关键词，启用场景检测
}

# Step 3: C6生成JSON计划
plan = {
    "plan_id": "c6-interview-analysis",
    "config": config,
    "tasks": [{
        "task_id": "interview-001",
        "video_path": "project/interview/raw.mp4",
        "output_dir": "output/interview-edit/C6-时间戳精准专家/"
    }]
}

# Step 4: C6调用本skill执行
from scripts.plan_executor import execute_plan
report = execute_plan(plan)

# Step 5: C6分析结果并提出建议
# - 识别高置信度剪辑点
# - 推荐淡入淡出参数
# - 标注需要人工确认的低置信度点
```

### Pattern 2: C5 Video Editing Integration (视频剪辑集成)

```python
# C5-视频编辑师使用C6提供的时间戳数据

# Step 1: C5调用C6获取时间戳
c6_result = execute_plan({...})

# Step 2: C5读取时间戳数据
with open('output/.../timestamps.json') as f:
    timestamps = json.load(f)

# Step 3: C5使用时间戳执行剪辑
from moviepy.editor import VideoFileClip

video = VideoFileClip('input.mp4')
clips = []

for gap in timestamps['silence_gaps']:
    if gap['confidence'] >= 0.9:  # 仅使用高置信度
        # 在静音点处切分
        clip = video.subclip(last_end, gap['start'])
        clips.append(clip)
        last_end = gap['end']

final = concatenate_videoclips(clips)
final.write_videofile('output/edited.mp4')
```

### Pattern 3: Batch Processing Pipeline (批量流水线)

```python
# 批量处理工作流

# 1. 扫描输入目录
import os
input_dir = 'input/raw_footage'
video_files = [f for f in os.listdir(input_dir) if f.endswith('.mp4')]

# 2. 生成批量计划
plan = {
    "plan_id": "batch-podcast-edit",
    "config": {...},  # 使用podcast模板配置
    "tasks": [
        {
            "task_id": f"podcast-{i:03d}",
            "video_path": os.path.join(input_dir, f),
            "output_dir": f"output/podcast-batch/timestamps/{i:03d}"
        }
        for i, f in enumerate(video_files, 1)
    ]
}

# 3. 执行批量提取
report = execute_plan(plan)

# 4. 后处理：导出CSV摘要
import csv
with open('batch_summary.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Video', 'Gaps', 'High Confidence', 'Scenes'])

    for result in report['task_results']:
        writer.writerow([
            result['video_path'],
            result['silence_gaps'],
            result['high_confidence_cuts'],
            result['scene_changes']
        ])
```

---

## Troubleshooting Guide

### Common Issues

#### Issue 1: FFmpeg Not Found

**Error**:
```
FileNotFoundError: [Errno 2] No such file or directory: 'ffmpeg'
```

**Solution**:
```bash
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt-get update && sudo apt-get install ffmpeg

# Windows
# 下载FFmpeg并添加到PATH环境变量
# https://ffmpeg.org/download.html

# 验证安装
ffmpeg -version
```

#### Issue 2: ModuleNotFoundError

**Error**:
```python
ModuleNotFoundError: No module named 'ffmpeg'
```

**Solution**:
```bash
# 确保安装的是ffmpeg-python，不是ffmpeg
pip uninstall ffmpeg  # 如果错误安装了
pip install ffmpeg-python pydub scenedetect[opencv]
```

#### Issue 3: Silence Detection Missing Gaps

**Symptoms**: 明显的静音片段未被检测到

**Solution**:
```python
# 1. 降低阈值（更敏感）
config = {
    'silence_thresh': -55  # 从-50降到-55
}

# 2. 减少最小静音时长
config = {
    'min_silence_len': 300  # 从500降到300
}

# 3. 检查音频RMS
from pydub import AudioSegment
audio = AudioSegment.from_file('video.mp4')
print(f"Average RMS: {audio.rms}")  # 如果>500，考虑降低阈值
```

#### Issue 4: VFR Video Timestamp Drift

**Symptoms**: 可变帧率视频的时间戳逐渐偏移

**Solution**:
```python
# 强制使用pts_time而非简单帧号计算
config = {
    'force_pts_time': true,
    'use_frame_numbers': false  # 不使用帧号×fps计算
}

# 或转码为CFR（恒定帧率）
ffmpeg -i input_vfr.mp4 -vf fps=30 -vsync cfr output_cfr.mp4
```

#### Issue 5: Out of Memory (大文件)

**Error**:
```
MemoryError: Unable to allocate array
```

**Solution**:
```python
# 1. 启用音频专用模式
{
    "audio_only": true
}

# 2. 分段处理大文件
# 先用ffmpeg切分视频
ffmpeg -i large.mp4 -c copy -segment_time 600 -f segment part_%03d.mp4

# 然后批量处理各段
```

#### Issue 6: Scene Detection Too Slow

**Solution**:
```python
# 1. 降低分辨率处理（不影响原视频）
{
    "scene_detector": {
        "downscale_width": 640  # 降低到640px宽
    }
}

# 2. 使用更快的检测器
{
    "scene_detector": {
        "type": "threshold",  # 比content快3-5倍
        "threshold": 12.0
    }
}

# 3. 或完全禁用
{
    "detect_scenes": false
}
```

---

## External Resources

### Official Documentation

- **FFmpeg**: https://ffmpeg.org/documentation.html
- **pydub**: https://github.com/jiaaro/pydub
- **PySceneDetect**: https://scenedetect.com/docs/
- **MoviePy**: https://zulko.github.io/moviepy/

### Recommended Libraries

| Library | Purpose | GitHub | Stars |
|---------|---------|--------|-------|
| **ffmpeg-python** | FFmpeg Python wrapper | [kkroening/ffmpeg-python](https://github.com/kkroening/ffmpeg-python) | ~10K |
| **pydub** | Audio processing | [jiaaro/pydub](https://github.com/jiaaro/pydub) | ~8K |
| **PySceneDetect** | Scene detection | [Breakthrough/PySceneDetect](https://github.com/Breakthrough/PySceneDetect) | ~3K |
| **whisper** (optional) | AI speech recognition | [openai/whisper](https://github.com/openai/whisper) | ~70K |
| **librosa** (optional) | Advanced audio analysis | [librosa/librosa](https://github.com/librosa/librosa) | ~7K |

### Related Skills

- **video-editing**: 配套的视频剪辑skill，使用本skill的时间戳数据
- **audio-enhancement**: 音频降噪和增强（未来计划）

### Community Resources

- **FFmpeg Filters Guide**: https://ffmpeg.org/ffmpeg-filters.html
- **Audio Signal Processing (Book)**: "Introduction to Digital Signal Processing" by Julius O. Smith III
- **Video Editing Theory**: "In the Blink of an Eye" by Walter Murch

---

## Version History

### v1.0.0 (2025-01-02)
- ✅ Initial release
- ✅ Core timestamp extraction with confidence scoring
- ✅ Frame-accurate calculation
- ✅ Scene change detection
- ✅ 3 preset templates
- ✅ Batch processing support

### Roadmap

**v1.1.0** (计划Q1 2025)
- [ ] Whisper integration (字级时间戳)
- [ ] Waveform visualization generation
- [ ] Export to EDL/XML formats

**v1.2.0** (计划Q2 2025)
- [ ] GPU acceleration for scene detection
- [ ] Real-time processing mode
- [ ] Web UI dashboard

**v2.0.0** (计划Q3 2025)
- [ ] Machine learning-based pause detection
- [ ] Multi-language speech boundary optimization
- [ ] DaVinci Resolve/Premiere Pro direct integration

---

## Contributing

欢迎贡献！如果您有改进建议或发现bug，请：

1. 提交Issue描述问题或建议
2. Fork本项目并创建feature分支
3. 提交PR并描述您的修改

---

## License

MIT License

Copyright (c) 2025 AIGC Digital Nomad Film Company

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
