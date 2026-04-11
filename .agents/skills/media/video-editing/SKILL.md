---
name: video-editing
description: Professional batch video editing skill using MoviePy
---


# Video Editing Skill

Professional batch video editing toolkit built on MoviePy, designed for intelligent editing workflows that integrate seamlessly with timestamp extraction data.

## Quick Start

### Basic Video Editing

```python
from scripts.video_editor import VideoEditor
from scripts.plan_executor import execute_plan

# Method 1: Direct API usage
editor = VideoEditor({
    'output_format': 'mp4',
    'resolution': '1080p',
    'fps': 30,
    'codec': 'libx264'
})

# Simple cut operation
result = editor.cut_video(
    input_path='input/interview.mp4',
    cuts=[
        {'start': 0, 'end': 30},      # Keep 0-30s
        {'start': 45, 'end': 120}     # Keep 45-120s
    ],
    output_path='output/interview_cut.mp4'
)

# Method 2: Using timestamp extraction results
import json
with open('output/interview-001_silence_gaps.json') as f:
    gaps = json.load(f)

# Auto-remove silence gaps with high confidence
editor.remove_silence_gaps(
    input_path='input/interview.mp4',
    gaps=gaps['gaps'],
    confidence_threshold=0.8,
    output_path='output/interview_clean.mp4'
)
```

### Template-Based Editing

```python
# Use preset template
import json
with open('templates/podcast-edit.json') as f:
    plan = json.load(f)

# Customize for your video
plan['tasks'][0]['input_video'] = 'input/my-podcast.mp4'
plan['tasks'][0]['timestamp_file'] = 'output/my-podcast_silence_gaps.json'

# Execute batch editing
results = execute_plan(plan)
```

## Core Features

### 1. Intelligent Cutting

**Remove Silence Gaps**: Automatically remove silence based on timestamp-extraction output
- Configurable confidence threshold filtering
- Smooth transitions with crossfade
- Preserve intentional pauses (low confidence gaps)

**Multi-Segment Cutting**: Extract or remove specific time ranges
- Frame-accurate cuts (±1 frame precision)
- Batch segment processing
- Gap handling (join segments or insert black frames)

**Smart Scene Assembly**: Reassemble video based on scene detection
- Use scene change timestamps from timestamp-extraction
- Automatic transition insertion
- Scene reordering support

### 2. Transitions & Effects

**Built-in Transitions**:
- Crossfade (adjustable duration)
- Fade to/from black
- Wipe (left, right, up, down)
- Slide (push, cover, uncover)

**Visual Effects**:
- Speed adjustment (slow-motion, time-lapse)
- Color grading (brightness, contrast, saturation)
- Blur (Gaussian, motion blur)
- Crop and resize
- Rotation and flip

### 3. Multi-Track Composition

**Video Layers**: Overlay multiple video tracks
- Picture-in-picture
- Split screen (2/3/4 way)
- Watermark overlay
- Custom positioning and scaling

**Audio Mixing**: Multi-track audio composition
- Background music integration
- Voiceover overlay
- Audio ducking (auto-reduce music when voice present)
- Volume normalization

### 4. Text & Graphics

**Text Overlays**:
- Titles and subtitles
- Lower thirds
- Animated text (fade in/out, slide, typewriter)
- Custom fonts and styling

**Graphics Overlay**:
- Logo watermarks
- Custom PNG/SVG overlays
- Animated graphics

### 5. Batch Processing

**Parallel Rendering**: Process multiple videos simultaneously
- CPU core utilization optimization
- Progress tracking per task
- Error recovery and retry logic

**Template Workflows**: Predefined editing pipelines
- Podcast editing (intro + content + outro)
- Interview editing (multi-cam switching)
- Montage creation (music-synced cuts)

## Configuration Reference

### VideoEditor Configuration

```python
config = {
    # Output Settings
    'output_format': 'mp4',              # mp4, avi, mov, webm
    'resolution': '1080p',                # 4k, 1080p, 720p, 480p, or custom (1920, 1080)
    'fps': 30,                            # Frame rate (23.976, 24, 25, 29.97, 30, 60)
    'codec': 'libx264',                   # Video codec (libx264, libx265, vp9)
    'audio_codec': 'aac',                 # Audio codec (aac, mp3, opus)
    'bitrate': '5M',                      # Video bitrate (e.g., '5M', '10M')
    'audio_bitrate': '192k',              # Audio bitrate (e.g., '128k', '192k', '320k')

    # Processing Settings
    'threads': 4,                         # CPU threads for encoding
    'preset': 'medium',                   # Encoding preset (ultrafast, fast, medium, slow, veryslow)
    'temp_dir': 'output/temp',           # Temporary files directory

    # Transition Settings
    'default_transition': 'crossfade',    # Default transition type
    'transition_duration': 0.5,           # Default transition duration (seconds)

    # Effect Settings
    'fade_duration': 1.0,                 # Default fade duration
    'audio_fade_duration': 0.5,           # Audio fade duration

    # Quality Settings
    'quality': 'high',                    # high, medium, low (affects bitrate/preset)
    'hardware_accel': False,              # Use hardware acceleration (if available)
}
```

### Cut Configuration

```python
cut_config = {
    'segments': [
        {
            'start': 0,                   # Start time (seconds or frame number)
            'end': 30,                    # End time (seconds or frame number)
            'fade_in': 0.5,              # Optional fade in duration
            'fade_out': 0.5,             # Optional fade out duration
            'speed': 1.0,                 # Speed multiplier (1.0 = normal)
        }
    ],
    'gap_handling': 'join',               # join, black, freeze
    'transition_between_segments': True,  # Add transitions between cuts
}
```

### Audio Mixing Configuration

```python
audio_config = {
    'background_music': {
        'path': 'assets/music.mp3',
        'volume': 0.3,                    # Volume relative to original (0.0-1.0)
        'fade_in': 2.0,                   # Fade in duration
        'fade_out': 2.0,                  # Fade out duration
        'loop': True,                     # Loop music to match video duration
        'ducking': {
            'enabled': True,
            'threshold': -30,             # dB threshold to trigger ducking
            'reduction': 0.4,             # Reduce music to this volume level
            'attack': 0.1,                # Fade down time (seconds)
            'release': 0.5,               # Fade up time (seconds)
        }
    },
    'voiceover': {
        'path': 'assets/narration.mp3',
        'start_time': 5.0,                # When to start voiceover
        'volume': 1.0,
    },
    'normalize': True,                    # Normalize final audio
    'target_loudness': -14,               # LUFS target (broadcast standard: -23)
}
```

## Templates

### Template: podcast-edit.json

**Purpose**: Automated podcast editing with intro/outro and silence removal

```json
{
  "plan_id": "podcast-edit-template",
  "description": "播客自动剪辑模板 - 添加片头片尾、移除静音片段、音频规范化",
  "config": {
    "output_format": "mp4",
    "resolution": "720p",
    "fps": 30,
    "codec": "libx264",
    "quality": "high"
  },
  "tasks": [
    {
      "task_id": "podcast-001",
      "type": "podcast_edit",
      "input_video": "input/podcast.mp4",
      "timestamp_file": "output/podcast_silence_gaps.json",
      "assets": {
        "intro": "assets/podcast_intro.mp4",
        "outro": "assets/podcast_outro.mp4",
        "background_music": "assets/podcast_music.mp3"
      },
      "editing": {
        "remove_silence": {
          "enabled": true,
          "confidence_threshold": 0.8,
          "min_gap_duration": 1.0
        },
        "audio_ducking": {
          "enabled": true,
          "music_volume": 0.2,
          "reduction": 0.4
        },
        "normalize_audio": true
      },
      "output_path": "output/podcast_final.mp4"
    }
  ]
}
```

### Template: interview-edit.json

**Purpose**: Interview editing with scene detection and multi-cam switching

```json
{
  "plan_id": "interview-edit-template",
  "description": "访谈剪辑模板 - 场景切换、多机位切换、字幕叠加",
  "config": {
    "output_format": "mp4",
    "resolution": "1080p",
    "fps": 30,
    "quality": "high"
  },
  "tasks": [
    {
      "task_id": "interview-001",
      "type": "interview_edit",
      "input_video": "input/interview_cam1.mp4",
      "timestamp_file": "output/interview_scene_changes.json",
      "multi_cam": {
        "enabled": true,
        "cameras": [
          {"path": "input/interview_cam1.mp4", "position": "wide"},
          {"path": "input/interview_cam2.mp4", "position": "closeup"}
        ],
        "switch_on_scene": true
      },
      "text_overlays": [
        {
          "type": "lower_third",
          "text": "专家访谈",
          "start": 5,
          "duration": 10
        }
      ],
      "output_path": "output/interview_final.mp4"
    }
  ]
}
```

### Template: montage.json

**Purpose**: Music-synced montage creation

```json
{
  "plan_id": "montage-template",
  "description": "音乐蒙太奇模板 - 音乐节奏同步剪辑、转场效果",
  "config": {
    "output_format": "mp4",
    "resolution": "1080p",
    "fps": 30,
    "quality": "high"
  },
  "tasks": [
    {
      "task_id": "montage-001",
      "type": "montage",
      "clips": [
        "input/clip1.mp4",
        "input/clip2.mp4",
        "input/clip3.mp4"
      ],
      "music": {
        "path": "assets/montage_music.mp3",
        "sync_to_beats": true,
        "beat_timestamps": [0.5, 1.0, 1.5, 2.0, 2.5]
      },
      "effects": {
        "transitions": ["crossfade", "wipe", "slide"],
        "color_grading": "cinematic",
        "speed_ramps": true
      },
      "output_path": "output/montage_final.mp4"
    }
  ]
}
```

## Output Format

### Task Result Structure

```json
{
  "task_id": "podcast-001",
  "status": "success",
  "input_video": {
    "path": "input/podcast.mp4",
    "duration": 3600.5,
    "resolution": [1920, 1080],
    "fps": 30,
    "codec": "h264"
  },
  "output_video": {
    "path": "output/podcast_final.mp4",
    "duration": 3245.2,
    "size_mb": 512.3,
    "resolution": [1280, 720],
    "fps": 30,
    "codec": "h264",
    "bitrate": "5M"
  },
  "editing_operations": [
    {
      "type": "concat",
      "description": "Added intro clip",
      "duration": 5.0
    },
    {
      "type": "remove_silence",
      "segments_removed": 42,
      "total_time_saved": 355.3
    },
    {
      "type": "audio_mix",
      "description": "Added background music with ducking"
    },
    {
      "type": "concat",
      "description": "Added outro clip",
      "duration": 8.0
    }
  ],
  "statistics": {
    "original_duration": 3600.5,
    "final_duration": 3245.2,
    "time_saved": 355.3,
    "compression_ratio": 0.90,
    "processing_time": 124.5,
    "encoding_speed": "26.3x"
  },
  "metadata": {
    "timestamp_file_used": "output/podcast_silence_gaps.json",
    "gaps_analyzed": 42,
    "gaps_removed": 38,
    "gaps_preserved": 4,
    "config": { ... }
  }
}
```

### Execution Report

```json
{
  "execution_id": "exec-20250128-143022",
  "plan_id": "podcast-batch-edit",
  "execution_time": "2025-01-28T14:30:22Z",
  "total_tasks": 5,
  "successful_tasks": 5,
  "failed_tasks": 0,
  "total_execution_time": 456.7,
  "aggregated_statistics": {
    "total_input_duration": 18000.0,
    "total_output_duration": 16234.5,
    "total_time_saved": 1765.5,
    "total_output_size_mb": 2456.8,
    "average_encoding_speed": "24.1x"
  },
  "task_results": [
    { /* task 1 result */ },
    { /* task 2 result */ }
  ],
  "config": { ... }
}
```

## Integration with C5 Agent

### Workflow Integration

The video-editing skill is designed to work seamlessly with C5-视频编辑师 agent:

```
User: "帮我把这个采访视频剪辑成精华版"
  ↓
C5 Agent analyzes request
  ↓
Step 1: C5 calls timestamp-extraction skill
  - Detects silence gaps
  - Identifies scene changes
  - Generates timestamp data
  ↓
Step 2: C5 reviews timestamp data
  - Evaluates which gaps to remove
  - Determines scene structure
  - Plans editing strategy
  ↓
Step 3: C5 generates editing plan (JSON)
  - Configures cut operations
  - Sets transition preferences
  - Defines output specifications
  ↓
Step 4: C5 calls video-editing skill
  - Executes editing plan
  - Applies effects and transitions
  - Renders final video
  ↓
Step 5: C5 reviews results
  - Validates output quality
  - Generates summary report
  - Delivers to user
```

### Example: C5 Agent Usage

```python
# C5 Agent generates this plan based on user requirements
editing_plan = {
    "plan_id": "interview-精华版-20250128",
    "config": {
        "output_format": "mp4",
        "resolution": "1080p",
        "quality": "high"
    },
    "tasks": [{
        "task_id": "interview-001",
        "type": "intelligent_edit",

        # Use timestamp-extraction results
        "input_video": "input/interview.mp4",
        "timestamp_file": "output/interview_silence_gaps.json",
        "scene_file": "output/interview_scene_changes.json",

        # C5's editing decisions
        "editing": {
            "remove_silence": {
                "enabled": True,
                "confidence_threshold": 0.85,  # Only remove high-confidence gaps
                "preserve_natural_pauses": True
            },
            "keep_scenes": [0, 2, 4, 7, 9],  # Based on scene analysis
            "transitions": {
                "type": "crossfade",
                "duration": 0.3
            }
        },

        "output_path": "output/interview_精华版.mp4"
    }]
}

# C5 executes the plan
from scripts.plan_executor import execute_plan
results = execute_plan(editing_plan)
```

## Integration with timestamp-extraction

### Seamless Data Pipeline

```python
# Step 1: Extract timestamps (done by C6 or separately)
from timestamp_extraction.scripts.plan_executor import execute_plan as extract_timestamps

timestamp_plan = {
    "plan_id": "interview-timestamp",
    "config": {
        "silence_thresh": -50,
        "min_silence_len": 500,
        "detect_scenes": True
    },
    "tasks": [{
        "task_id": "interview-001",
        "video_path": "input/interview.mp4",
        "output_dir": "output/interview-timestamps"
    }]
}

timestamp_results = extract_timestamps(timestamp_plan)

# Step 2: Use timestamps for editing
from video_editing.scripts.plan_executor import execute_plan as edit_video

editing_plan = {
    "plan_id": "interview-edit",
    "config": {"resolution": "1080p"},
    "tasks": [{
        "task_id": "interview-001",
        "input_video": "input/interview.mp4",

        # Reference timestamp extraction results
        "timestamp_file": "output/interview-timestamps/interview-001_silence_gaps.json",
        "scene_file": "output/interview-timestamps/interview-001_scene_changes.json",

        "editing": {
            "remove_silence": {"enabled": True, "confidence_threshold": 0.8}
        },
        "output_path": "output/interview_edited.mp4"
    }]
}

editing_results = edit_video(editing_plan)
```

## Dependencies

### Required Libraries

```bash
# Core video processing
pip install moviepy>=1.0.3

# Audio processing (MoviePy dependency)
pip install imageio>=2.25.0
pip install imageio-ffmpeg>=0.4.8

# Image processing
pip install Pillow>=10.0.0
pip install numpy>=1.24.0

# Optional: Advanced audio
pip install pydub>=0.25.1  # For audio normalization
pip install scipy>=1.11.0  # For audio ducking algorithms

# Optional: GPU acceleration
pip install opencv-python>=4.8.0  # For faster processing
```

### System Requirements

- **FFmpeg**: Must be installed and in PATH
  - Linux: `sudo apt-get install ffmpeg`
  - macOS: `brew install ffmpeg`
  - Windows: Download from https://ffmpeg.org/

- **Python**: 3.8 or higher

- **Disk Space**:
  - Temporary space: 2-3x size of input videos
  - Output space: Varies by compression settings

- **RAM**:
  - Minimum: 4GB
  - Recommended: 8GB+ for HD videos
  - 16GB+ for 4K videos

- **CPU**:
  - Minimum: Dual-core
  - Recommended: Quad-core+ for faster encoding

## Troubleshooting

### Issue 1: Encoding Too Slow

**Symptoms**: Video rendering takes very long time

**Solutions**:
1. Use faster preset: `config['preset'] = 'fast'` or `'ultrafast'`
2. Reduce output resolution: `config['resolution'] = '720p'`
3. Enable hardware acceleration (if available):
   ```python
   config['hardware_accel'] = True
   config['codec'] = 'h264_nvenc'  # NVIDIA GPU
   # or 'h264_videotoolbox'  # macOS
   # or 'h264_qsv'  # Intel QuickSync
   ```
4. Increase thread count: `config['threads'] = 8`

### Issue 2: Output File Too Large

**Symptoms**: Edited video file size is too large

**Solutions**:
1. Reduce bitrate: `config['bitrate'] = '3M'` (lower from 5M)
2. Use more efficient codec: `config['codec'] = 'libx265'` (H.265)
3. Adjust quality preset: `config['preset'] = 'slow'` (better compression)
4. Reduce resolution if acceptable

### Issue 3: Audio Out of Sync

**Symptoms**: Audio and video are not synchronized in output

**Solutions**:
1. Ensure consistent FPS: Use original video's FPS
2. Use audio-visual sync mode:
   ```python
   editor = VideoEditor({'sync_mode': 'audio'})
   ```
3. Re-encode audio: `config['audio_codec'] = 'aac'`
4. Check for VFR (variable frame rate) input - convert to CFR first

### Issue 4: Memory Error During Rendering

**Symptoms**: Process crashes with MemoryError or out of memory

**Solutions**:
1. Process in chunks:
   ```python
   config['chunk_size'] = 300  # Process 300 seconds at a time
   ```
2. Reduce resolution during processing:
   ```python
   config['processing_resolution'] = '720p'
   config['output_resolution'] = '1080p'  # Upscale at end
   ```
3. Close other applications to free RAM
4. Use disk-based temp files: `config['use_disk_cache'] = True`

### Issue 5: Transitions Not Smooth

**Symptoms**: Visible jumps or artifacts at transition points

**Solutions**:
1. Increase transition duration: `config['transition_duration'] = 1.0`
2. Use different transition type:
   ```python
   config['transition_type'] = 'crossfade'  # Usually smoothest
   ```
3. Ensure cuts are at keyframes:
   ```python
   config['snap_to_keyframe'] = True
   ```
4. Add fade to black between segments:
   ```python
   config['gap_handling'] = 'black'
   config['fade_duration'] = 0.5
   ```

### Issue 6: Text Overlay Not Visible

**Symptoms**: Text overlays don't appear or are cut off

**Solutions**:
1. Check text positioning:
   ```python
   text_config = {
       'position': ('center', 'bottom'),
       'margin': 50  # Pixels from edge
   }
   ```
2. Increase text size: `'fontsize': 48`
3. Add text background/stroke:
   ```python
   text_config = {
       'stroke_color': 'black',
       'stroke_width': 2,
       'bg_color': 'rgba(0,0,0,0.5)'
   }
   ```
4. Verify font is installed: Use built-in fonts or provide font path

## Advanced Usage

### Custom Effect Pipeline

```python
from scripts.video_editor import VideoEditor

editor = VideoEditor()

# Chain multiple effects
result = editor.process_video(
    input_path='input/video.mp4',
    effects=[
        {'type': 'color_grade', 'preset': 'cinematic'},
        {'type': 'speed', 'factor': 1.2},  # Speed up 20%
        {'type': 'blur', 'amount': 0.5, 'start': 0, 'end': 5},  # Blur intro
        {'type': 'crop', 'x': 100, 'y': 0, 'w': 1720, 'h': 1080}
    ],
    output_path='output/processed.mp4'
)
```

### Multi-Track Composition

```python
# Picture-in-picture effect
editor.compose_multi_track(
    main_video='input/main.mp4',
    overlays=[
        {
            'video': 'input/webcam.mp4',
            'position': ('right', 'bottom'),
            'size': (480, 270),  # 25% of 1080p
            'start': 10,
            'end': 60
        }
    ],
    output_path='output/pip.mp4'
)

# Split screen (2-way)
editor.split_screen(
    videos=[
        'input/speaker1.mp4',
        'input/speaker2.mp4'
    ],
    layout='horizontal',  # or 'vertical', 'grid'
    output_path='output/split.mp4'
)
```

### Automated Color Grading

```python
# Apply LUT (Look-Up Table)
editor.apply_lut(
    input_path='input/video.mp4',
    lut_file='assets/luts/cinematic.cube',
    strength=0.8,  # 80% of LUT effect
    output_path='output/graded.mp4'
)

# Preset color grades
editor.color_grade(
    input_path='input/video.mp4',
    preset='cinematic',  # or 'warm', 'cool', 'vibrant', 'desaturated'
    output_path='output/graded.mp4'
)
```

### Subtitle Generation & Overlay

```python
# From SRT file
editor.add_subtitles(
    input_path='input/video.mp4',
    srt_file='assets/subtitles.srt',
    style={
        'fontsize': 48,
        'color': 'white',
        'stroke_color': 'black',
        'stroke_width': 2,
        'position': ('center', 'bottom'),
        'margin': 50
    },
    output_path='output/subtitled.mp4'
)
```

## Performance Tips

1. **Use Proxy Files for Preview**: Edit with lower-resolution proxies, render with originals
2. **Batch Similar Operations**: Group cuts, transitions, effects to minimize re-encoding
3. **Optimize I/O**: Use SSD for temp files, keep source and output on different drives
4. **Monitor Resources**: Use `config['verbose'] = True` to see encoding stats
5. **Pre-Process Audio**: Normalize and mix audio separately for faster video rendering

## Version History

### v1.0.0 (2025-01-28)

**Initial Release**

Features:
- Core editing operations (cut, concat, fade)
- Transition effects (crossfade, wipe, slide)
- Multi-track composition (PIP, split-screen)
- Audio mixing and ducking
- Text overlays and graphics
- Batch processing system
- Integration with timestamp-extraction skill
- 3 preset templates (podcast, interview, montage)

Compatibility:
- MoviePy 1.0.3+
- Python 3.8+
- FFmpeg 4.0+

---

**Author**: AIGC数字游牧派影视文化公司
**License**: MIT
**Support**: 通过C5-视频编辑师 agent获取帮助
