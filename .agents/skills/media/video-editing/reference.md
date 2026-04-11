# Video Editing Skill - Extended Reference

**Version**: 1.0.0
**Last Updated**: 2025-01-28
**Author**: AIGC数字游牧派影视文化公司

---

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Complete API Reference](#complete-api-reference)
3. [Advanced Configuration](#advanced-configuration)
4. [Performance Tuning](#performance-tuning)
5. [Integration Patterns](#integration-patterns)
6. [Troubleshooting Guide](#troubleshooting-guide)
7. [MoviePy Best Practices](#moviepy-best-practices)
8. [External Resources](#external-resources)

---

## Architecture Overview

### Component Diagram

```
video-editing/
├── scripts/
│   ├── video_editor.py         # Core editing engine
│   │   ├── VideoEditor class
│   │   │   ├── remove_silence_gaps()
│   │   │   ├── cut_video()
│   │   │   ├── add_audio_mix()
│   │   │   ├── compose_multi_track()
│   │   │   └── apply_effects()
│   │   └── Helper functions
│   │
│   └── plan_executor.py        # Batch execution
│       ├── PlanExecutor class
│       │   ├── execute()
│       │   ├── _preprocess_task()
│       │   ├── _save_task_result()
│       │   └── _generate_execution_report()
│       └── execute_plan() function
│
├── templates/                  # Preset configurations
│   ├── podcast-edit.json
│   ├── interview-edit.json
│   └── montage.json
│
├── SKILL.md                    # Main documentation
└── reference.md                # This file
```

### Data Flow

```
1. Input
   ├── Video file(s)
   ├── Timestamp data (from timestamp-extraction)
   └── JSON execution plan

2. VideoEditor Processing
   ├── Load video(s) with MoviePy
   ├── Apply editing operations
   │   ├── Cutting
   │   ├── Transitions
   │   ├── Effects
   │   └── Audio mixing
   └── Render output video

3. Output
   ├── Edited video file(s)
   ├── Task result JSON
   └── Execution report JSON
```

### Execution Flow

```
User/C5 Agent
    ↓
Generate JSON Plan
    ↓
PlanExecutor.execute()
    ├── For each task:
    │   ├── _preprocess_task() (workflow-specific)
    │   ├── VideoEditor.process_task()
    │   │   ├── Load video
    │   │   ├── Load timestamp data (if needed)
    │   │   ├── Calculate segments
    │   │   ├── Apply effects
    │   │   ├── Render video
    │   │   └── Save output
    │   ├── _save_task_result()
    │   └── Update progress
    └── _generate_execution_report()
```

---

## Complete API Reference

### VideoEditor Class

#### Constructor

```python
VideoEditor(config: Dict = None)
```

**Parameters**:
- `config` (Dict, optional): Configuration dictionary

**Configuration Options**:
```python
{
    # Output Settings
    'output_format': 'mp4',              # Video format
    'resolution': '1080p',                # Resolution (4k, 1080p, 720p, 480p, or tuple)
    'fps': 30,                            # Frame rate
    'codec': 'libx264',                   # Video codec
    'audio_codec': 'aac',                 # Audio codec
    'bitrate': '5M',                      # Video bitrate
    'audio_bitrate': '192k',              # Audio bitrate

    # Processing Settings
    'threads': 4,                         # CPU threads
    'preset': 'medium',                   # Encoding preset
    'temp_dir': 'output/temp',           # Temporary files

    # Transition Settings
    'default_transition': 'crossfade',    # Default transition
    'transition_duration': 0.5,           # Transition duration (seconds)

    # Effect Settings
    'fade_duration': 1.0,                 # Fade duration
    'audio_fade_duration': 0.5,           # Audio fade duration
}
```

#### Methods

##### `remove_silence_gaps()`

Remove silence gaps from video based on timestamp data.

```python
remove_silence_gaps(
    input_path: str,
    gaps: List[Dict],
    confidence_threshold: float = 0.8,
    min_gap_duration: float = 0.5,
    preserve_natural_pauses: bool = True,
    output_path: str = None
) -> Dict
```

**Parameters**:
- `input_path` (str): Path to input video
- `gaps` (List[Dict]): Gap dictionaries from timestamp-extraction
  ```python
  {
      'id': 'gap-001',
      'start': 10.5,
      'end': 12.3,
      'duration': 1.8,
      'confidence': 0.92,
      'type': 'natural_pause'
  }
  ```
- `confidence_threshold` (float): Minimum confidence to remove (default: 0.8)
- `min_gap_duration` (float): Minimum gap duration to remove (default: 0.5s)
- `preserve_natural_pauses` (bool): Keep low-confidence gaps (default: True)
- `output_path` (str, optional): Output video path

**Returns**:
```python
{
    'input_path': 'input/video.mp4',
    'output_path': 'output/video_no_silence.mp4',
    'original_duration': 3600.5,
    'final_duration': 3245.2,
    'time_saved': 355.3,
    'compression_ratio': 0.901,
    'gaps_analyzed': 42,
    'gaps_removed': 38,
    'gaps_preserved': 4,
    'segments_kept': 39
}
```

##### `cut_video()`

Cut video into segments.

```python
cut_video(
    input_path: str,
    cuts: List[Dict],
    output_path: str = None,
    gap_handling: str = 'join',
    add_transitions: bool = True
) -> Dict
```

**Parameters**:
- `input_path` (str): Path to input video
- `cuts` (List[Dict]): Cut segments
  ```python
  [
      {
          'start': 0,
          'end': 30,
          'fade_in': 0.5,      # Optional
          'fade_out': 0.5,     # Optional
          'speed': 1.0         # Optional (1.0 = normal)
      }
  ]
  ```
- `output_path` (str, optional): Output video path
- `gap_handling` (str): How to handle gaps ('join', 'black', 'freeze')
- `add_transitions` (bool): Add transitions between segments

**Returns**:
```python
{
    'input_path': 'input/video.mp4',
    'output_path': 'output/video_cut.mp4',
    'original_duration': 3600.5,
    'final_duration': 1800.0,
    'segments': 10
}
```

##### `add_audio_mix()`

Add background music and/or voiceover to video.

```python
add_audio_mix(
    input_path: str,
    background_music: Dict = None,
    voiceover: Dict = None,
    output_path: str = None,
    normalize: bool = True
) -> Dict
```

**Parameters**:
- `input_path` (str): Path to input video
- `background_music` (Dict, optional): Background music configuration
  ```python
  {
      'path': 'assets/music.mp3',
      'volume': 0.3,
      'fade_in': 2.0,
      'fade_out': 2.0,
      'loop': True,
      'ducking': {
          'enabled': True,
          'threshold': -30,
          'reduction': 0.4,
          'attack': 0.1,
          'release': 0.5
      }
  }
  ```
- `voiceover` (Dict, optional): Voiceover configuration
  ```python
  {
      'path': 'assets/narration.mp3',
      'start_time': 5.0,
      'volume': 1.0
  }
  ```
- `output_path` (str, optional): Output video path
- `normalize` (bool): Normalize final audio (default: True)

**Returns**:
```python
{
    'input_path': 'input/video.mp4',
    'output_path': 'output/video_mixed.mp4',
    'audio_tracks_mixed': 3
}
```

##### `process_task()`

Process a single editing task from JSON plan.

```python
process_task(task: Dict) -> Dict
```

**Parameters**:
- `task` (Dict): Task configuration from execution plan

**Returns**:
```python
{
    'task_id': 'podcast-001',
    'task_type': 'remove_silence',
    'status': 'success',  # or 'failed'
    'input_path': 'input/podcast.mp4',
    'output_path': 'output/podcast_final.mp4',
    'original_duration': 3600.5,
    'final_duration': 3245.2,
    'time_saved': 355.3,
    'processing_time': 124.5,
    'error': None  # or error message if failed
}
```

### PlanExecutor Class

#### Constructor

```python
PlanExecutor(plan_path: str)
```

**Parameters**:
- `plan_path` (str): Path to JSON execution plan file

#### Methods

##### `execute()`

Execute all tasks in the plan.

```python
execute() -> Dict
```

**Returns**:
```python
{
    'execution_id': 'exec-20250128-143022',
    'plan_id': 'podcast-batch-edit',
    'execution_time': '2025-01-28T14:30:22Z',
    'total_tasks': 5,
    'successful_tasks': 5,
    'failed_tasks': 0,
    'total_execution_time': 456.7,
    'aggregated_statistics': {
        'total_input_duration': 18000.0,
        'total_output_duration': 16234.5,
        'total_time_saved': 1765.5,
        'total_output_size_mb': 2456.8,
        'average_encoding_speed': 24.1
    },
    'task_results': [...]
}
```

### Convenience Functions

#### `execute_plan()`

Execute plan from file path or dictionary.

```python
execute_plan(plan_path: Union[str, Dict]) -> Dict
```

**Parameters**:
- `plan_path` (str or Dict): JSON plan file path or plan dictionary

**Returns**: Execution report dictionary

---

## Advanced Configuration

### Environment-Based Presets

Create configuration presets for different environments:

```python
# Development: Fast encoding, lower quality
DEV_CONFIG = {
    'resolution': '720p',
    'fps': 30,
    'preset': 'ultrafast',
    'bitrate': '2M',
    'threads': 2
}

# Production: High quality, slower encoding
PROD_CONFIG = {
    'resolution': '1080p',
    'fps': 30,
    'preset': 'slow',
    'bitrate': '8M',
    'threads': 8
}

# 4K Production: Maximum quality
UHD_CONFIG = {
    'resolution': '4k',
    'fps': 60,
    'preset': 'veryslow',
    'bitrate': '30M',
    'codec': 'libx265',  # H.265 for better 4K compression
    'threads': 16
}
```

### Hardware Acceleration

Enable GPU acceleration for faster encoding (if available):

```python
# NVIDIA GPU (NVENC)
NVENC_CONFIG = {
    'codec': 'h264_nvenc',
    'preset': 'p4',  # p1-p7, p7 = slowest/best quality
    'bitrate': '10M',
    'hardware_accel': True
}

# macOS (VideoToolbox)
VT_CONFIG = {
    'codec': 'h264_videotoolbox',
    'bitrate': '10M',
    'hardware_accel': True
}

# Intel QuickSync
QSV_CONFIG = {
    'codec': 'h264_qsv',
    'preset': 'slow',
    'bitrate': '10M',
    'hardware_accel': True
}
```

### Codec Selection Guide

```python
# H.264 (libx264): Universal compatibility
H264_CONFIG = {
    'codec': 'libx264',
    'preset': 'medium',
    'bitrate': '5M'
}

# H.265 (libx265): Better compression, higher CPU usage
H265_CONFIG = {
    'codec': 'libx265',
    'preset': 'medium',
    'bitrate': '3M'  # ~40% smaller than H.264 at same quality
}

# VP9: Web-optimized, good for YouTube
VP9_CONFIG = {
    'codec': 'libvpx-vp9',
    'preset': 'good',
    'bitrate': '4M'
}

# ProRes: Professional editing codec
PRORES_CONFIG = {
    'codec': 'prores_ks',
    'profile': 2,  # 0=Proxy, 1=LT, 2=Standard, 3=HQ
    'output_format': 'mov'
}
```

---

## Performance Tuning

### Optimization Strategies

#### 1. Resolution Scaling

Process at lower resolution, upscale at end:

```python
config = {
    'processing_resolution': '720p',  # Edit at 720p
    'output_resolution': '1080p',     # Upscale to 1080p at render
    'upscale_quality': 'lanczos'      # High-quality upscaling
}
```

#### 2. Chunk Processing

Process large videos in chunks:

```python
config = {
    'chunk_size': 300,  # Process 5 minutes at a time
    'use_disk_cache': True,
    'temp_dir': '/fast-ssd/temp'  # Use SSD for temp files
}
```

#### 3. Parallel Processing

Process multiple tasks in parallel:

```python
from multiprocessing import Pool

def process_single_task(task):
    editor = VideoEditor(config)
    return editor.process_task(task)

# Process 4 tasks in parallel
with Pool(processes=4) as pool:
    results = pool.map(process_single_task, tasks)
```

#### 4. Optimize I/O

```python
# Best practices:
# - Source files on fast drive (SSD preferred)
# - Temp files on separate drive from source
# - Output to third drive if possible

config = {
    'temp_dir': '/ssd/temp',           # Fast SSD
    'input_buffer_size': '64M',        # Larger buffer
    'output_buffer_size': '64M'
}
```

### Encoding Speed vs Quality

```python
# Speed comparison (relative to 'medium'):
PRESET_SPEEDS = {
    'ultrafast': '10x faster, -40% quality',
    'superfast': '5x faster, -30% quality',
    'veryfast':  '3x faster, -20% quality',
    'faster':    '2x faster, -10% quality',
    'fast':      '1.5x faster, -5% quality',
    'medium':    'Baseline',
    'slow':      '0.5x speed, +10% quality',
    'slower':    '0.3x speed, +15% quality',
    'veryslow':  '0.1x speed, +20% quality'
}
```

**Recommendations**:
- **Development/Preview**: `ultrafast` or `veryfast`
- **Production (fast turnaround)**: `fast` or `medium`
- **Production (high quality)**: `slow` or `slower`
- **Archival/Master**: `veryslow`

---

## Integration Patterns

### Pattern 1: C5 Agent Integration

Complete workflow with C5-视频编辑师 agent:

```python
# C5 Agent workflow
class C5VideoEditor:
    def __init__(self):
        self.timestamp_extractor = TimestampExtractor()
        self.video_editor = VideoEditor()

    def intelligent_edit(self, video_path: str, user_request: str):
        # Step 1: Analyze video
        timestamp_result = self.timestamp_extractor.process_task({
            'video_path': video_path,
            'config': self._determine_timestamp_config(video_path)
        })

        # Step 2: Decide editing strategy
        editing_plan = self._generate_editing_plan(
            timestamp_result,
            user_request
        )

        # Step 3: Execute editing
        editing_result = self.video_editor.process_task(editing_plan)

        # Step 4: Quality check
        if self._validate_output(editing_result):
            return editing_result
        else:
            # Retry with adjusted parameters
            return self.intelligent_edit(video_path, user_request)

    def _determine_timestamp_config(self, video_path):
        # Analyze video type and determine optimal config
        # (Podcast vs Interview vs Vlog)
        pass

    def _generate_editing_plan(self, timestamp_result, user_request):
        # Generate JSON editing plan based on:
        # - Timestamp extraction results
        # - User request analysis
        # - Quality requirements
        pass

    def _validate_output(self, result):
        # Check output quality
        pass
```

### Pattern 2: Batch Pipeline

Processing multiple videos with consistent settings:

```python
# Generate batch plan
def create_batch_plan(video_files: List[str]) -> Dict:
    tasks = []

    for i, video_file in enumerate(video_files):
        # Find corresponding timestamp file
        timestamp_file = video_file.replace('.mp4', '_silence_gaps.json')

        task = {
            'task_id': f'batch-{i+1:03d}',
            'type': 'remove_silence',
            'input_video': video_file,
            'timestamp_file': timestamp_file,
            'editing': {
                'remove_silence': {
                    'enabled': True,
                    'confidence_threshold': 0.85
                }
            },
            'output_path': f'output/batch/video_{i+1:03d}_final.mp4'
        }
        tasks.append(task)

    return {
        'plan_id': 'batch-processing',
        'config': {'resolution': '1080p', 'quality': 'high'},
        'tasks': tasks
    }

# Execute
plan = create_batch_plan(video_files)
results = execute_plan(plan)
```

### Pattern 3: Multi-Stage Pipeline

Complex workflow with multiple editing stages:

```python
# Stage 1: Remove silence
stage1_plan = {
    'plan_id': 'stage1-silence',
    'tasks': [
        {
            'type': 'remove_silence',
            'input_video': 'input/raw.mp4',
            'timestamp_file': 'output/raw_gaps.json',
            'output_path': 'output/stage1_no_silence.mp4'
        }
    ]
}
stage1_result = execute_plan(stage1_plan)

# Stage 2: Add intro/outro
stage2_plan = {
    'plan_id': 'stage2-branding',
    'tasks': [
        {
            'type': 'concat',
            'clips': [
                'assets/intro.mp4',
                stage1_result['output_path'],
                'assets/outro.mp4'
            ],
            'output_path': 'output/stage2_with_branding.mp4'
        }
    ]
}
stage2_result = execute_plan(stage2_plan)

# Stage 3: Add background music
stage3_plan = {
    'plan_id': 'stage3-audio',
    'tasks': [
        {
            'type': 'audio_mix',
            'input_video': stage2_result['output_path'],
            'background_music': {
                'path': 'assets/music.mp3',
                'volume': 0.2,
                'loop': True
            },
            'output_path': 'output/final.mp4'
        }
    ]
}
final_result = execute_plan(stage3_plan)
```

### Pattern 4: Quality Validation

Automated quality checks:

```python
def validate_editing_result(result: Dict) -> Dict:
    """
    Validate editing result quality

    Returns:
        {
            'valid': True/False,
            'issues': [],
            'recommendations': []
        }
    """
    issues = []
    recommendations = []

    # Check 1: Output file exists
    if not os.path.exists(result['output_path']):
        issues.append('Output file not found')

    # Check 2: Duration is reasonable
    original_duration = result['original_duration']
    final_duration = result['final_duration']
    compression_ratio = final_duration / original_duration

    if compression_ratio < 0.5:
        recommendations.append(
            f'High compression ratio ({compression_ratio:.2f}). '
            f'Consider reviewing removed segments.'
        )

    # Check 3: File size
    output_size_mb = os.path.getsize(result['output_path']) / (1024 * 1024)
    expected_size = final_duration * 0.7  # ~0.7 MB/second for 1080p

    if output_size_mb < expected_size * 0.5:
        issues.append(f'Output file size too small ({output_size_mb:.1f}MB)')

    # Check 4: Processing time
    processing_time = result.get('processing_time', 0)
    encoding_speed = original_duration / processing_time if processing_time > 0 else 0

    if encoding_speed < 1.0:
        recommendations.append(
            f'Slow encoding speed ({encoding_speed:.1f}x). '
            f'Consider using faster preset.'
        )

    return {
        'valid': len(issues) == 0,
        'issues': issues,
        'recommendations': recommendations
    }
```

---

## Troubleshooting Guide

### Common Issues & Solutions

#### Issue 1: "MoviePy module not found"

**Symptoms**: ImportError when running scripts

**Solutions**:
```bash
# Install MoviePy
pip install moviepy

# Verify installation
python -c "import moviepy; print(moviepy.__version__)"

# Install with all dependencies
pip install moviepy[optional]
```

#### Issue 2: Encoding extremely slow

**Symptoms**: Processing takes hours for short videos

**Solutions**:
1. Use faster preset:
   ```python
   config['preset'] = 'fast'  # or 'veryfast'
   ```

2. Reduce resolution during editing:
   ```python
   config['processing_resolution'] = '720p'
   ```

3. Enable hardware acceleration (if available):
   ```python
   config['codec'] = 'h264_nvenc'  # NVIDIA
   config['hardware_accel'] = True
   ```

4. Increase thread count:
   ```python
   config['threads'] = 8  # Match CPU cores
   ```

#### Issue 3: Output file size too large

**Symptoms**: Edited videos are much larger than expected

**Solutions**:
1. Reduce bitrate:
   ```python
   config['bitrate'] = '3M'  # Lower from default 5M
   ```

2. Use H.265 codec:
   ```python
   config['codec'] = 'libx265'
   config['bitrate'] = '2M'  # H.265 needs less bitrate
   ```

3. Adjust quality preset:
   ```python
   config['preset'] = 'slow'  # Better compression
   ```

4. Two-pass encoding:
   ```python
   config['passes'] = 2  # Better quality per bit
   ```

#### Issue 4: Audio out of sync

**Symptoms**: Audio and video not synchronized

**Solutions**:
1. Match original FPS:
   ```python
   # Auto-detect FPS from source
   from moviepy.editor import VideoFileClip
   clip = VideoFileClip('input.mp4')
   config['fps'] = clip.fps
   ```

2. Use audio-visual sync:
   ```python
   config['sync_mode'] = 'audio'
   ```

3. Re-encode audio:
   ```python
   config['audio_codec'] = 'aac'
   config['audio_bitrate'] = '192k'
   ```

#### Issue 5: Transitions have artifacts

**Symptoms**: Visible glitches at transition points

**Solutions**:
1. Increase transition duration:
   ```python
   config['transition_duration'] = 1.0  # Longer fade
   ```

2. Use keyframe-aligned cuts:
   ```python
   config['snap_to_keyframe'] = True
   ```

3. Add black frames between segments:
   ```python
   config['gap_handling'] = 'black'
   config['black_duration'] = 0.5
   ```

#### Issue 6: Memory errors during rendering

**Symptoms**: Process crashes with MemoryError

**Solutions**:
1. Enable chunk processing:
   ```python
   config['chunk_size'] = 300  # 5 minutes
   ```

2. Use disk cache:
   ```python
   config['use_disk_cache'] = True
   config['temp_dir'] = '/large-drive/temp'
   ```

3. Close other applications to free RAM

4. Reduce processing resolution:
   ```python
   config['processing_resolution'] = '720p'
   ```

---

## MoviePy Best Practices

### Resource Management

```python
# ALWAYS close clips after use
video = VideoFileClip('input.mp4')
try:
    # Process video
    result = video.subclip(0, 10)
    result.write_videofile('output.mp4')
finally:
    # Cleanup
    video.close()
    result.close()
```

### Avoid Re-encoding When Possible

```python
# BAD: Multiple re-encodes
clip1 = VideoFileClip('video.mp4')
clip2 = clip1.subclip(0, 10).write_videofile('temp1.mp4')
clip3 = VideoFileClip('temp1.mp4').subclip(0, 5).write_videofile('temp2.mp4')

# GOOD: Single re-encode
clip = VideoFileClip('video.mp4')
final = clip.subclip(0, 5)
final.write_videofile('output.mp4')
clip.close()
final.close()
```

### Efficient Concatenation

```python
# BAD: Load each clip separately
clips = [VideoFileClip(f'clip{i}.mp4') for i in range(10)]

# GOOD: Use context manager
from moviepy.editor import concatenate_videoclips

with contextlib.ExitStack() as stack:
    clips = [stack.enter_context(VideoFileClip(f'clip{i}.mp4')) for i in range(10)]
    final = concatenate_videoclips(clips)
    final.write_videofile('output.mp4')
```

### Audio Normalization

```python
from moviepy.audio.AudioClip import CompositeAudioClip

# Normalize audio levels
def normalize_audio(clip, target_loudness=-14):
    """Normalize audio to target LUFS"""
    # Simplified normalization
    # For professional work, use external tools like ffmpeg-normalize
    return clip.volumex(1.0)
```

---

## External Resources

### Official Documentation
- **MoviePy**: https://zulko.github.io/moviepy/
- **FFmpeg**: https://ffmpeg.org/documentation.html
- **Python Imaging Library**: https://pillow.readthedocs.io/

### Useful Tools
- **FFmpeg**: Command-line video processor
- **ffprobe**: Media file analyzer
- **HandBrake**: GUI for video encoding
- **Kdenlive**: Open-source video editor (for reference)

### Learning Resources
- MoviePy Tutorial: https://zulko.github.io/moviepy/getting_started/quick_presentation.html
- FFmpeg Encoding Guide: https://trac.ffmpeg.org/wiki/Encode/H.264
- Video Codec Comparison: https://en.wikipedia.org/wiki/Comparison_of_video_codecs

### Performance Benchmarks
- H.264 vs H.265: https://www.encoding.com/blog/2015/05/05/h-264-vs-h-265/
- Preset Speed Comparison: https://trac.ffmpeg.org/wiki/Encode/H.264#Preset

---

**Document Version**: 1.0.0
**Last Updated**: 2025-01-28
**Next Review**: 2025-02-28

For questions or support, contact the C5-视频编辑师 agent or refer to the main SKILL.md documentation.
