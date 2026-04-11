"""
Timestamp Extraction - Core Engine
====================================

核心时间戳提取引擎，整合静音检测、场景检测、帧计算等功能。

Author: AIGC Digital Nomad Film Company
Version: 1.0.0
License: MIT
"""

import os
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime

try:
    import ffmpeg
except ImportError:
    raise ImportError(
        "ffmpeg-python is required. Install with: pip install ffmpeg-python"
    )

try:
    from pydub import AudioSegment
    from pydub.silence import detect_silence
except ImportError:
    raise ImportError(
        "pydub is required. Install with: pip install pydub"
    )

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class TimestampExtractor:
    """
    帧级精度的时间戳提取引擎

    Features:
    - Silence detection with confidence scoring
    - Frame-accurate timestamp calculation
    - Scene change detection (optional)
    - VFR video support
    - Batch processing
    """

    def __init__(self, config: Dict):
        """
        初始化提取器

        Args:
            config: 配置字典
                - silence_thresh (int): 静音阈值dB，默认-50
                - min_silence_len (int): 最小静音时长ms，默认500
                - padding (int): 安全填充ms，默认200
                - detect_scenes (bool): 是否检测场景，默认False
                - scene_detector (dict): 场景检测配置
        """
        self.silence_thresh = config.get('silence_thresh', -50)
        self.min_silence_len = config.get('min_silence_len', 500)
        self.padding = config.get('padding', 200)
        self.detect_scenes = config.get('detect_scenes', False)
        self.scene_config = config.get('scene_detector', {})
        self.output_format = config.get('output_format', {})

        logger.info(f"TimestampExtractor initialized with config: {config}")

    def extract_video_info(self, video_path: str) -> Dict:
        """
        提取视频元数据

        Args:
            video_path: 视频文件路径

        Returns:
            视频信息字典
        """
        logger.info(f"Extracting video info from: {video_path}")

        try:
            probe = ffmpeg.probe(video_path)
        except ffmpeg.Error as e:
            logger.error(f"FFprobe error: {e.stderr.decode()}")
            raise

        # 查找视频流
        video_stream = next(
            (s for s in probe['streams'] if s['codec_type'] == 'video'),
            None
        )

        # 查找音频流
        audio_stream = next(
            (s for s in probe['streams'] if s['codec_type'] == 'audio'),
            None
        )

        if not audio_stream:
            raise ValueError(f"No audio track found in {video_path}")

        # 解析FPS
        if video_stream:
            fps_parts = video_stream['r_frame_rate'].split('/')
            fps = float(fps_parts[0]) / float(fps_parts[1])
        else:
            fps = None

        info = {
            'path': video_path,
            'duration': float(probe['format']['duration']),
            'fps': fps,
            'resolution': f"{video_stream['width']}x{video_stream['height']}" if video_stream else None,
            'audio_channels': audio_stream['channels'],
            'audio_sample_rate': int(audio_stream['sample_rate']),
            'video_codec': video_stream['codec_name'] if video_stream else None,
            'audio_codec': audio_stream['codec_name']
        }

        logger.info(f"Video info extracted: {info}")
        return info

    def extract_silence_gaps(self, video_path: str) -> List[Dict]:
        """
        提取静音片段的时间戳

        Args:
            video_path: 视频文件路径

        Returns:
            静音片段列表，每项包含start/end/duration/confidence等字段
        """
        logger.info(f"Detecting silence gaps in: {video_path}")

        try:
            # 使用pydub加载音频
            audio = AudioSegment.from_file(video_path)

            # 检测静音
            silences = detect_silence(
                audio,
                min_silence_len=self.min_silence_len,
                silence_thresh=self.silence_thresh
            )

            logger.info(f"Found {len(silences)} silence gaps")

            # 转换为秒并添加安全填充
            gaps = []
            for i, (start_ms, end_ms) in enumerate(silences):
                # 应用安全填充
                padded_start = max(0, start_ms + self.padding)
                padded_end = max(padded_start, end_ms - self.padding)

                gap = {
                    'id': f"gap-{i:03d}",
                    'start': padded_start / 1000,
                    'end': padded_end / 1000,
                    'duration': (padded_end - padded_start) / 1000,
                    'original_start': start_ms / 1000,
                    'original_end': end_ms / 1000
                }

                # 计算置信度
                gap_audio = audio[start_ms:end_ms]
                gap['confidence'] = self._calculate_confidence(gap_audio, gap['duration'])

                # 分类边界类型
                gap['type'] = self._classify_boundary_type(gap['confidence'], gap['duration'])

                # 推荐淡入淡出时长
                gap['recommended_fade'] = self._recommend_fade_duration(gap['duration'])

                gaps.append(gap)

            # 按置信度排序
            gaps.sort(key=lambda x: x['confidence'], reverse=True)

            logger.info(f"Processed {len(gaps)} silence gaps with confidence scores")
            return gaps

        except Exception as e:
            logger.error(f"Error detecting silence: {e}")
            raise

    def _calculate_confidence(self, audio_segment: AudioSegment, duration: float) -> float:
        """
        计算静音片段的置信度评分（0-1）

        多因素评分：
        1. Volume Score: RMS音量越低越好
        2. Duration Score: 0.5-2秒最佳
        3. Boundary Sharpness: 未来可扩展（需要分析音量变化速率）

        Args:
            audio_segment: pydub音频片段
            duration: 持续时长（秒）

        Returns:
            置信度评分 (0.0-1.0)
        """
        # 1. Volume Score (音量评分)
        rms = audio_segment.rms
        # 将RMS映射到0-1分数（RMS越低越好）
        # 假设RMS < 100为理想静音，> 500为明显有声音
        volume_score = max(0, min(1, 1 - (rms / 500)))

        # 2. Duration Score (时长评分)
        # 0.5-2秒为最佳剪辑点时长
        if 0.5 <= duration <= 2.0:
            duration_score = 1.0
        elif duration < 0.5:
            # 过短，惩罚
            duration_score = duration / 0.5
        else:
            # 过长，适度惩罚
            duration_score = max(0.5, 2.0 / duration)

        # 综合评分（可调整权重）
        confidence = (volume_score * 0.7 + duration_score * 0.3)

        return round(confidence, 2)

    def _classify_boundary_type(self, confidence: float, duration: float) -> str:
        """
        根据置信度和时长分类边界类型

        Args:
            confidence: 置信度评分
            duration: 持续时长

        Returns:
            边界类型字符串
        """
        if confidence >= 0.9:
            if duration >= 1.5:
                return "natural_pause"  # 自然停顿
            else:
                return "breath_pause"   # 呼吸停顿
        elif confidence >= 0.7:
            return "moderate_pause"     # 中等停顿
        else:
            return "weak_pause"         # 弱停顿（不推荐）

    def _recommend_fade_duration(self, gap_duration: float) -> Dict[str, float]:
        """
        根据静音时长推荐淡入淡出时长

        Args:
            gap_duration: 静音片段时长（秒）

        Returns:
            {'in': fade_in_duration, 'out': fade_out_duration}
        """
        if gap_duration < 0.5:
            # 短停顿：快速淡入淡出
            return {'in': 0.1, 'out': 0.1}
        elif gap_duration < 1.5:
            # 中等停顿：标准淡入淡出
            return {'in': 0.2, 'out': 0.3}
        else:
            # 长停顿：较长淡入淡出
            return {'in': 0.3, 'out': 0.5}

    def convert_to_frame_accurate(
        self,
        timestamps: List[float],
        video_path: str
    ) -> List[Dict]:
        """
        将时间戳转换为帧级精度格式

        Args:
            timestamps: 时间戳列表（秒）
            video_path: 视频文件路径

        Returns:
            帧级精度数据列表
        """
        logger.info(f"Converting {len(timestamps)} timestamps to frame-accurate format")

        video_info = self.extract_video_info(video_path)
        fps = video_info['fps']

        if not fps:
            logger.warning("No video stream found, skipping frame conversion")
            return []

        frame_data = []
        for ts in timestamps:
            frame_num = int(ts * fps)

            data = {
                'time': ts,
                'frame': frame_num,
                'fps': fps,
                'timecode': self._to_smpte_timecode(ts, fps)
            }

            frame_data.append(data)

        logger.info(f"Converted {len(frame_data)} timestamps to frames")
        return frame_data

    def _to_smpte_timecode(self, seconds: float, fps: float) -> str:
        """
        转换为SMPTE时间码格式 (HH:MM:SS:FF)

        Args:
            seconds: 秒数
            fps: 帧率

        Returns:
            SMPTE时间码字符串
        """
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        frames = int((seconds % 1) * fps)

        return f"{hours:02d}:{minutes:02d}:{secs:02d}:{frames:02d}"

    def detect_scene_changes(self, video_path: str) -> List[Dict]:
        """
        检测场景切换点

        Args:
            video_path: 视频文件路径

        Returns:
            场景切换点列表
        """
        if not self.detect_scenes:
            logger.info("Scene detection disabled, skipping")
            return []

        try:
            from scenedetect import detect, ContentDetector, ThresholdDetector
        except ImportError:
            logger.error("scenedetect not installed. Install with: pip install scenedetect[opencv]")
            return []

        logger.info(f"Detecting scene changes in: {video_path}")

        try:
            # 选择检测器
            detector_type = self.scene_config.get('type', 'content')
            threshold = self.scene_config.get('threshold', 27.0)

            if detector_type == 'content':
                detector = ContentDetector(threshold=threshold)
            elif detector_type == 'threshold':
                detector = ThresholdDetector(threshold=threshold)
            else:
                detector = ContentDetector(threshold=27.0)

            # 执行检测
            scene_list = detect(video_path, detector)

            # 获取视频信息
            video_info = self.extract_video_info(video_path)
            fps = video_info['fps']

            # 转换为标准格式
            scenes = []
            for i, (start_time, end_time) in enumerate(scene_list):
                scenes.append({
                    'id': f"scene-{i:03d}",
                    'frame': int(start_time.get_frames()),
                    'time': start_time.get_seconds(),
                    'timecode': self._to_smpte_timecode(start_time.get_seconds(), fps),
                    'confidence': 0.85,  # PySceneDetect不提供置信度，使用默认值
                    'type': 'hard_cut'
                })

            logger.info(f"Detected {len(scenes)} scene changes")
            return scenes

        except Exception as e:
            logger.error(f"Scene detection failed: {e}")
            return []

    def process_task(self, task: Dict) -> Dict:
        """
        处理单个任务

        Args:
            task: 任务字典，包含video_path, output_dir等字段

        Returns:
            处理结果字典
        """
        task_id = task['task_id']
        video_path = task['video_path']
        output_dir = task.get('output_dir', 'output/timestamps')

        logger.info(f"Processing task: {task_id}")
        logger.info(f"Video: {video_path}")

        # 验证文件存在
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Video not found: {video_path}")

        # 提取视频信息
        video_info = self.extract_video_info(video_path)

        # 提取静音片段
        silence_gaps = self.extract_silence_gaps(video_path)

        # 收集所有时间戳
        timestamps = []
        for gap in silence_gaps:
            timestamps.extend([gap['start'], gap['end']])

        # 转换为帧级精度
        if video_info['fps']:
            frame_data = self.convert_to_frame_accurate(timestamps, video_path)

            # 将帧数据添加回silence_gaps
            for gap in silence_gaps:
                gap_start_data = next(
                    (f for f in frame_data if abs(f['time'] - gap['start']) < 0.001),
                    None
                )
                gap_end_data = next(
                    (f for f in frame_data if abs(f['time'] - gap['end']) < 0.001),
                    None
                )

                if gap_start_data and gap_end_data:
                    gap['start_frame'] = gap_start_data['frame']
                    gap['end_frame'] = gap_end_data['frame']
                    gap['start_timecode'] = gap_start_data['timecode']
                    gap['end_timecode'] = gap_end_data['timecode']

        # 场景检测
        scene_changes = self.detect_scene_changes(video_path)

        # 统计信息
        high_confidence_count = sum(1 for gap in silence_gaps if gap['confidence'] >= 0.9)
        total_silence_duration = sum(gap['duration'] for gap in silence_gaps)

        statistics = {
            'total_silence_gaps': len(silence_gaps),
            'total_silence_duration': round(total_silence_duration, 2),
            'high_confidence_cuts': high_confidence_count,
            'scene_changes': len(scene_changes),
            'processing_time': 0  # Will be set by executor
        }

        result = {
            'task_id': task_id,
            'video_info': video_info,
            'silence_gaps': silence_gaps,
            'scene_changes': scene_changes,
            'statistics': statistics
        }

        logger.info(f"Task {task_id} completed: {statistics}")
        return result


# Utility functions

def format_timecode(seconds: float, fps: float = 30.0) -> str:
    """
    便捷函数：将秒数转换为时间码

    Args:
        seconds: 秒数
        fps: 帧率（默认30）

    Returns:
        SMPTE时间码字符串
    """
    extractor = TimestampExtractor({})
    return extractor._to_smpte_timecode(seconds, fps)


def calculate_frame_number(seconds: float, fps: float) -> int:
    """
    便捷函数：计算帧号

    Args:
        seconds: 秒数
        fps: 帧率

    Returns:
        帧号
    """
    return int(seconds * fps)


if __name__ == "__main__":
    # 测试代码
    import sys

    if len(sys.argv) < 2:
        print("Usage: python core_engine.py <video_path>")
        sys.exit(1)

    video_path = sys.argv[1]

    # 创建提取器
    config = {
        'silence_thresh': -50,
        'min_silence_len': 500,
        'padding': 200,
        'detect_scenes': True
    }

    extractor = TimestampExtractor(config)

    # 处理任务
    task = {
        'task_id': 'test-001',
        'video_path': video_path,
        'output_dir': 'output/test'
    }

    result = extractor.process_task(task)

    # 打印结果
    print("\n" + "="*60)
    print("TIMESTAMP EXTRACTION RESULTS")
    print("="*60)
    print(f"\nVideo: {result['video_info']['path']}")
    print(f"Duration: {result['video_info']['duration']:.2f}s")
    print(f"FPS: {result['video_info']['fps']}")
    print(f"\nSilence Gaps: {result['statistics']['total_silence_gaps']}")
    print(f"High Confidence Cuts: {result['statistics']['high_confidence_cuts']}")
    print(f"Scene Changes: {result['statistics']['scene_changes']}")
    print(f"\nTop 5 High-Confidence Cut Points:")
    for gap in result['silence_gaps'][:5]:
        print(f"  {gap['start']:.2f}s - {gap['end']:.2f}s "
              f"(confidence: {gap['confidence']}, type: {gap['type']})")
    print("="*60 + "\n")
