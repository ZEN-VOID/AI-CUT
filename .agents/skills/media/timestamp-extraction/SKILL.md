---
name: timestamp-extraction
description: |
  专业帧级精度时间戳提取与剪辑点检测工具，支持静音片段、语音边界、场景切换识别与批量处理。
---


# Timestamp Extraction Skill

**专业帧级精度时间戳提取与剪辑点检测工具**

本skill为C6-时间戳精准专家智能体提供执行引擎，通过ffmpeg、pydub、PySceneDetect等工具实现：
- ✅ 静音片段检测与时间戳提取
- ✅ 语音边界识别（Voice Activity Detection）
- ✅ 场景切换检测（Scene Change Detection）
- ✅ 帧级精度计算（±1帧误差）
- ✅ 置信度评分系统
- ✅ 批量处理支持
- ✅ 预设模板（播客/访谈/Vlog）

---

## Quick Start

### Basic Usage

```python
from scripts.plan_executor import execute_plan

# 1. 创建执行计划（或使用模板）
plan = {
    "plan_id": "interview-edit-001",
    "config": {
        "silence_thresh": -50,      # dB阈值
        "min_silence_len": 500,     # 最小静音时长(ms)
        "padding": 200,             # 安全填充(ms)
        "detect_scenes": True       # 是否检测场景切换
    },
    "tasks": [
        {
            "task_id": "shot-001",
            "video_path": "input/interview.mp4",
            "output_dir": "output/interview-edit/timestamps"
        }
    ]
}

# 2. 执行提取
results = execute_plan(plan)

# 3. 输出结果
# output/interview-edit/timestamps/
# ├── timestamps.json      # 所有时间戳数据
# ├── silence_gaps.json    # 静音片段详情
# ├── scene_changes.json   # 场景切换点（如启用）
# └── metadata.json        # 执行元数据
```

### Using Templates

```python
# 使用预设模板
import json
from scripts.plan_executor import execute_plan

# 加载播客剪辑模板
with open('templates/podcast.json') as f:
    plan = json.load(f)

# 修改输入路径
plan['tasks'][0]['video_path'] = 'my-podcast.mp3'

# 执行
results = execute_plan(plan)
```

### CLI Usage

```bash
# 使用模板执行
python .agents/skills/timestamp-extraction/scripts/plan_executor.py \
    .agents/skills/timestamp-extraction/templates/podcast.json

# 使用自定义计划
python .agents/skills/timestamp-extraction/scripts/plan_executor.py \
    output/plans/my-custom-plan.json
```

---

## Core Features

### 1. Silence Detection (静音检测)

**核心算法**:
- 基于pydub的`detect_silence()`函数
- 可配置dB阈值（默认-50dB）
- 可配置最小静音时长（默认500ms）
- 自动添加安全填充（避免切掉句子边缘）

**输出示例**:
```json
{
  "silence_gaps": [
    {
      "start": 12.45,
      "end": 14.32,
      "duration": 1.87,
      "confidence": 0.92,
      "type": "natural_pause",
      "recommended_fade": {
        "in": 0.2,
        "out": 0.3
      }
    }
  ]
}
```

### 2. Frame-Accurate Timestamps (帧级精度)

**支持格式**:
- 秒数（12.456）
- 帧号（374 @ 30fps）
- SMPTE时间码（00:00:12:14）
- 毫秒（12456ms）

**VFR视频处理**:
- 自动检测可变帧率（VFR）
- 使用pts_time而非简单的帧号×FPS
- 避免累积误差

**代码示例**:
```python
from scripts.frame_calculator import FrameCalculator

calc = FrameCalculator('video.mp4')

# 时间 → 帧号
frame = calc.time_to_frame(12.456)  # 374

# 帧号 → 时间码
timecode = calc.frame_to_timecode(374)  # "00:00:12:14"

# 批量转换
timestamps = [10.5, 20.3, 30.7]
frames = calc.batch_convert(timestamps, output_format='frame')
```

### 3. Scene Change Detection (场景检测)

**基于PySceneDetect**:
- ContentDetector: 基于内容相似度
- ThresholdDetector: 基于亮度阈值
- AdaptiveDetector: 自适应检测

**配置示例**:
```json
{
  "detect_scenes": true,
  "scene_detector": {
    "type": "content",
    "threshold": 27.0,
    "min_scene_len": 15
  }
}
```

### 4. Confidence Scoring (置信度评分)

**多因素评分系统**:
1. **Volume Score** (音量评分): RMS越低越好
2. **Duration Score** (时长评分): 0.5-2秒最佳
3. **Boundary Sharpness** (边界锐度): 音量下降速度
4. **Speech Completeness** (语音完整性): 是否在句子中间

**置信度等级**:
- 0.9-1.0: 高置信度（自然停顿，推荐使用）
- 0.7-0.9: 中置信度（可用，建议人工确认）
- 0.5-0.7: 低置信度（不推荐，除非必要）
- <0.5: 极低置信度（避免使用）

---

## Configuration Reference

### Plan Structure

```json
{
  "plan_id": "唯一标识符",
  "config": {
    "silence_thresh": -50,           // dB阈值 (-60到-30)
    "min_silence_len": 500,          // 最小静音时长(ms)
    "padding": 200,                  // 安全填充(ms)
    "detect_scenes": false,          // 是否检测场景
    "scene_detector": {
      "type": "content",             // content|threshold|adaptive
      "threshold": 27.0,
      "min_scene_len": 15            // 最小场景长度(帧)
    },
    "output_format": {
      "include_waveform": false,     // 是否生成波形图
      "include_timecodes": true,     // 是否包含SMPTE时间码
      "include_frames": true         // 是否包含帧号
    }
  },
  "tasks": [
    {
      "task_id": "任务标识",
      "video_path": "输入视频路径",
      "output_dir": "输出目录",
      "audio_only": false            // 仅处理音频轨
    }
  ]
}
```

### Environment-Specific Thresholds

```yaml
专业录音棚:
  silence_thresh: -60dB
  min_silence_len: 300ms
  用途: 高质量音频，需要最精准的静音检测

标准采访/播客:
  silence_thresh: -50dB
  min_silence_len: 500ms
  用途: 一般录音环境

嘈杂环境（餐厅/户外）:
  silence_thresh: -40dB
  min_silence_len: 800ms
  用途: 背景噪音较大的环境
```

---

## Templates

本skill提供3个预设模板，覆盖常见剪辑场景：

### 1. Podcast Template (`templates/podcast.json`)

**特点**:
- 更严格的静音检测（-55dB）
- 较短的最小静音时长（400ms，快节奏）
- 不检测场景切换（音频为主）
- 包含波形可视化

**适用场景**: 播客、有声书、音频访谈

### 2. Interview Template (`templates/interview.json`)

**特点**:
- 标准静音检测（-50dB）
- 中等最小静音时长（500ms）
- 启用场景检测（捕捉镜头切换）
- 包含时间码和帧号

**适用场景**: 访谈视频、纪录片、教学视频

### 3. Vlog Template (`templates/vlog.json`)

**特点**:
- 宽松静音检测（-45dB，背景音乐常驻）
- 较长最小静音时长（800ms）
- 强化场景检测（频繁切换）
- 快速模式（跳过部分质量检查）

**适用场景**: Vlog、旅拍、活动记录

---

## Output Format

### timestamps.json

```json
{
  "plan_id": "interview-edit-001",
  "task_id": "shot-001",
  "video_info": {
    "path": "input/interview.mp4",
    "duration": 1845.23,
    "fps": 29.97,
    "resolution": "1920x1080",
    "audio_channels": 2,
    "audio_sample_rate": 48000
  },
  "silence_gaps": [
    {
      "start": 12.45,
      "end": 14.32,
      "duration": 1.87,
      "start_frame": 373,
      "end_frame": 429,
      "start_timecode": "00:00:12:14",
      "end_timecode": "00:00:14:12",
      "confidence": 0.92,
      "type": "natural_pause",
      "recommended_fade": {
        "in": 0.2,
        "out": 0.3
      }
    }
  ],
  "scene_changes": [
    {
      "frame": 1250,
      "time": 41.71,
      "timecode": "00:00:41:21",
      "confidence": 0.88,
      "type": "hard_cut"
    }
  ],
  "statistics": {
    "total_silence_gaps": 47,
    "total_silence_duration": 95.6,
    "high_confidence_cuts": 38,
    "scene_changes": 12,
    "processing_time": 8.3
  }
}
```

### metadata.json

```json
{
  "execution_id": "exec-20250102-143022",
  "plan_id": "interview-edit-001",
  "execution_time": "2025-01-02T14:30:22Z",
  "total_tasks": 1,
  "successful_tasks": 1,
  "failed_tasks": 0,
  "total_processing_time": 8.3,
  "skill_version": "1.0.0",
  "dependencies": {
    "ffmpeg": "6.0",
    "ffprobe": "6.0",
    "pydub": "0.25.1",
    "scenedetect": "0.6.2"
  }
}
```

---

## Error Handling

本skill实现完善的错误处理机制：

### 1. Input Validation

```python
# 视频文件检查
if not os.path.exists(video_path):
    raise FileNotFoundError(f"Video not found: {video_path}")

# 格式检查
probe = ffmpeg.probe(video_path)
if not any(s['codec_type'] == 'audio' for s in probe['streams']):
    raise ValueError("No audio track found in video")
```

### 2. Graceful Degradation

```python
# 场景检测失败时降级
try:
    scenes = detect_scenes(video_path)
except Exception as e:
    logger.warning(f"Scene detection failed: {e}")
    scenes = []  # 继续执行，仅跳过场景检测
```

### 3. Retry Logic

```python
# API调用重试
@retry(tries=3, delay=2, backoff=2)
def extract_audio_track(video_path):
    return ffmpeg.input(video_path).audio.output('temp.wav').run()
```

### 4. Detailed Logging

```python
# 分级日志
logger.info(f"Processing task {task_id}")
logger.debug(f"Using silence threshold: {silence_thresh}dB")
logger.warning(f"Low confidence gap detected at {time}s")
logger.error(f"Failed to process {video_path}: {error}")
```

---

## Performance Optimization

### 1. Batch Processing

```python
# 并行处理多个任务
from concurrent.futures import ThreadPoolExecutor

with ThreadPoolExecutor(max_workers=4) as executor:
    futures = [executor.submit(process_task, task) for task in tasks]
    results = [f.result() for f in futures]
```

### 2. Audio-Only Mode

```python
# 仅提取音频轨（跳过视频解码）
{
  "audio_only": true  // 速度提升3-5倍
}
```

### 3. Fast Mode

```python
# 快速模式（降低精度换取速度）
{
  "fast_mode": true,
  "skip_waveform": true,
  "skip_confidence_scoring": true
}
```

### 4. Checkpoint Support

```python
# 断点续传（大批量任务）
{
  "checkpoint_enabled": true,
  "checkpoint_interval": 10  // 每10个任务保存一次
}
```

---

## Integration with C6 Agent

### 工作流程

```
用户请求
  ↓
C6-时间戳精准专家（智能体）
  ↓
决策：选择检测策略和参数
  ↓
调用 timestamp-extraction skill
  ↓
执行：ffmpeg + pydub + PySceneDetect
  ↓
返回：结构化JSON数据
  ↓
C6分析并提出建议
```

### Python调用示例

```python
# C6智能体调用本skill的方式
from gemini_code import Task

# 方式1: 通过Bash工具
Task(
    subagent_type="C6-时间戳精准专家",
    prompt="""
    分析这个访谈视频，提取所有静音片段和场景切换点。
    视频路径: project/interview/raw-footage.mp4
    输出目录: output/interview-edit/C6-时间戳精准专家/
    """
)

# C6内部会调用：
# python .agents/skills/timestamp-extraction/scripts/plan_executor.py \
#     .agents/skills/timestamp-extraction/templates/interview.json
```

---

## Dependencies

### Required

```bash
pip install ffmpeg-python pydub scenedetect[opencv]
```

```requirements.txt
ffmpeg-python>=0.2.0
pydub>=0.25.1
scenedetect[opencv]>=0.6.2
numpy>=1.24.0
```

### Optional (for enhanced features)

```bash
# Whisper（AI语音识别，字级时间戳）
pip install openai-whisper

# Librosa（高级音频分析）
pip install librosa
```

### System Dependencies

```bash
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt-get install ffmpeg

# Windows
# 下载FFmpeg二进制文件并添加到PATH
```

---

## Troubleshooting

### 常见问题

**Q: "ModuleNotFoundError: No module named 'ffmpeg'"**
```bash
# 确保安装的是ffmpeg-python，不是ffmpeg
pip uninstall ffmpeg  # 卸载错误的包
pip install ffmpeg-python
```

**Q: 静音检测漏检太多**
```json
// 降低阈值（更敏感）
{
  "silence_thresh": -55  // 从-50调整到-55
}
```

**Q: VFR视频时间戳不准确**
```python
# 强制使用pts_time而非简单计算
{
  "force_pts_time": true
}
```

**Q: 处理速度太慢**
```json
{
  "fast_mode": true,
  "audio_only": true,
  "skip_scene_detection": true
}
```

---

## Advanced Usage

### Custom Confidence Scoring

```python
# 自定义置信度评分算法
from scripts.silence_detector import SilenceDetector

class CustomDetector(SilenceDetector):
    def calculate_confidence(self, gap):
        # 添加自定义评分逻辑
        base_score = super().calculate_confidence(gap)

        # 惩罚过短的静音
        if gap['duration'] < 0.3:
            base_score *= 0.5

        # 奖励自然句子边界
        if self.is_sentence_boundary(gap):
            base_score *= 1.2

        return min(1.0, base_score)
```

### Whisper Integration (字级时间戳)

```python
# 启用Whisper增强
{
  "enable_whisper": true,
  "whisper_model": "base",
  "language": "zh"  // 中文
}

# 输出包含字级时间戳
{
  "word_timestamps": [
    {"word": "你好", "start": 1.23, "end": 1.56, "confidence": 0.98},
    {"word": "世界", "start": 1.60, "end": 1.92, "confidence": 0.95}
  ]
}
```

---

## Version History

**v1.0.0** (2025-01-02)
- ✅ Initial release
- ✅ Silence detection with confidence scoring
- ✅ Frame-accurate timestamp calculation
- ✅ Scene change detection (PySceneDetect)
- ✅ 3 preset templates (podcast/interview/vlog)
- ✅ Batch processing support
- ✅ VFR video handling

**Roadmap**:
- v1.1.0: Whisper integration (字级时间戳)
- v1.2.0: Waveform visualization
- v1.3.0: GPU acceleration for scene detection
- v2.0.0: Real-time processing support

---

## License

MIT License - 可自由用于商业和个人项目

---

## Support

- **Documentation**: See `reference.md` for detailed API documentation
- **Examples**: Check `templates/` for preset configurations
- **Issues**: Report bugs in project's GitHub repository
- **Related**: Pairs with `video-editing` skill for complete editing pipeline
