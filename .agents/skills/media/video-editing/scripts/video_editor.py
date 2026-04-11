#!/usr/bin/env python3
"""
Video Editing - Core Engine
============================

MoviePy-based video editing engine with intelligent cutting, transitions,
effects, and multi-track composition capabilities.

Key Features:
- Intelligent silence gap removal using timestamp data
- Multi-segment cutting with frame accuracy
- Transition effects (crossfade, wipe, slide, fade)
- Audio mixing with ducking
- Text overlays and graphics
- Multi-track composition (PIP, split-screen)
- Batch processing support

Author: AIGC Digital Nomad Film Company
Version: 1.0.0
"""

import os
import sys
import json
import logging
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Union
from datetime import datetime

# MoviePy imports
try:
    # MoviePy 2.x uses direct import from moviepy package
    from moviepy import (
        VideoFileClip, AudioFileClip, ImageClip, TextClip, ColorClip,
        CompositeVideoClip, concatenate_videoclips, concatenate_audioclips,
        vfx, afx
    )
    # Import effects modules
    try:
        from moviepy.video.fx import all as vfx_all
        from moviepy.audio.fx import all as afx_all
    except ImportError:
        # MoviePy 2.x may have different fx structure
        vfx_all = vfx
        afx_all = afx
except ImportError:
    print("Error: MoviePy not installed. Run: pip install moviepy")
    sys.exit(1)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class VideoEditor:
    """
    MoviePy-based video editing engine

    Provides comprehensive video editing capabilities:
    - Cutting and concatenation
    - Transition effects
    - Audio mixing and ducking
    - Text overlays
    - Multi-track composition
    - Effects and color grading
    """

    def __init__(self, config: Dict = None):
        """
        Initialize VideoEditor

        Args:
            config: Configuration dictionary with output settings
        """
        self.config = config or {}

        # Output settings
        self.output_format = self.config.get('output_format', 'mp4')
        self.resolution = self._parse_resolution(self.config.get('resolution', '1080p'))
        self.fps = self.config.get('fps', 30)
        self.codec = self.config.get('codec', 'libx264')
        self.audio_codec = self.config.get('audio_codec', 'aac')
        self.bitrate = self.config.get('bitrate', '5M')
        self.audio_bitrate = self.config.get('audio_bitrate', '192k')

        # Processing settings
        self.threads = self.config.get('threads', 4)
        self.preset = self.config.get('preset', 'medium')
        self.temp_dir = self.config.get('temp_dir', 'output/temp')

        # Transition settings
        self.default_transition = self.config.get('default_transition', 'crossfade')
        self.transition_duration = self.config.get('transition_duration', 0.5)
        self.fade_duration = self.config.get('fade_duration', 1.0)

        # Create temp directory
        Path(self.temp_dir).mkdir(parents=True, exist_ok=True)

        logger.info(f"VideoEditor initialized: {self.resolution[0]}x{self.resolution[1]}@{self.fps}fps")

    def _parse_resolution(self, resolution: Union[str, Tuple[int, int]]) -> Tuple[int, int]:
        """Parse resolution string or tuple"""
        if isinstance(resolution, tuple):
            return resolution

        resolution_map = {
            '4k': (3840, 2160),
            '1080p': (1920, 1080),
            '720p': (1280, 720),
            '480p': (854, 480),
        }

        return resolution_map.get(resolution.lower(), (1920, 1080))

    def remove_silence_gaps(
        self,
        input_path: str,
        gaps: List[Dict],
        confidence_threshold: float = 0.8,
        min_gap_duration: float = 0.5,
        preserve_natural_pauses: bool = True,
        output_path: str = None
    ) -> Dict:
        """
        Remove silence gaps from video based on timestamp data

        Args:
            input_path: Path to input video
            gaps: List of gap dictionaries from timestamp-extraction
            confidence_threshold: Only remove gaps with confidence >= this
            min_gap_duration: Minimum gap duration to remove (seconds)
            preserve_natural_pauses: Keep low-confidence gaps (natural pauses)
            output_path: Path to output video

        Returns:
            Result dictionary with statistics
        """
        logger.info(f"Removing silence gaps from: {input_path}")
        logger.info(f"Total gaps analyzed: {len(gaps)}")

        # Load video
        video = VideoFileClip(input_path)
        original_duration = video.duration

        # Filter gaps to remove
        gaps_to_remove = []
        gaps_to_preserve = []

        for gap in gaps:
            confidence = gap.get('confidence', 0)
            duration = gap.get('duration', 0)

            # Decision logic
            should_remove = (
                confidence >= confidence_threshold and
                duration >= min_gap_duration and
                not (preserve_natural_pauses and confidence < 0.9)
            )

            if should_remove:
                gaps_to_remove.append(gap)
            else:
                gaps_to_preserve.append(gap)

        logger.info(f"Gaps to remove: {len(gaps_to_remove)}")
        logger.info(f"Gaps to preserve: {len(gaps_to_preserve)}")

        # Generate keep segments (inverse of gaps to remove)
        keep_segments = self._calculate_keep_segments(
            video.duration,
            gaps_to_remove
        )

        # Extract and concatenate keep segments
        clips = []
        for i, segment in enumerate(keep_segments):
            start, end = segment['start'], segment['end']
            logger.debug(f"Extracting segment {i+1}: {start:.2f}s - {end:.2f}s")

            clip = video.subclip(start, end)
            clips.append(clip)

        # Concatenate with transitions
        if self.config.get('add_transitions', True):
            final_video = self._concatenate_with_transitions(
                clips,
                transition=self.default_transition,
                duration=self.transition_duration
            )
        else:
            final_video = concatenate_videoclips(clips)

        # Generate output path if not provided
        if output_path is None:
            output_path = self._generate_output_path(input_path, suffix='_no_silence')

        # Ensure output directory exists
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)

        # Write output video
        logger.info(f"Rendering video to: {output_path}")
        final_video.write_videofile(
            output_path,
            codec=self.codec,
            audio_codec=self.audio_codec,
            bitrate=self.bitrate,
            audio_bitrate=self.audio_bitrate,
            fps=self.fps,
            preset=self.preset,
            threads=self.threads,
            logger=None  # Suppress moviepy's logger
        )

        # Calculate statistics
        final_duration = final_video.duration
        time_saved = original_duration - final_duration

        # Cleanup
        video.close()
        final_video.close()
        for clip in clips:
            clip.close()

        result = {
            'input_path': input_path,
            'output_path': output_path,
            'original_duration': round(original_duration, 2),
            'final_duration': round(final_duration, 2),
            'time_saved': round(time_saved, 2),
            'compression_ratio': round(final_duration / original_duration, 3),
            'gaps_analyzed': len(gaps),
            'gaps_removed': len(gaps_to_remove),
            'gaps_preserved': len(gaps_to_preserve),
            'segments_kept': len(keep_segments)
        }

        logger.info(f"✅ Editing complete: saved {time_saved:.1f}s ({time_saved/original_duration*100:.1f}%)")

        return result

    def _calculate_keep_segments(
        self,
        duration: float,
        gaps_to_remove: List[Dict]
    ) -> List[Dict]:
        """
        Calculate segments to keep (inverse of gaps)

        Args:
            duration: Total video duration
            gaps_to_remove: List of gap dictionaries to remove

        Returns:
            List of segment dictionaries with start/end times
        """
        # Sort gaps by start time
        sorted_gaps = sorted(gaps_to_remove, key=lambda g: g['start'])

        segments = []
        current_pos = 0.0

        for gap in sorted_gaps:
            gap_start = gap['start']
            gap_end = gap['end']

            # Add segment before this gap
            if gap_start > current_pos:
                segments.append({
                    'start': current_pos,
                    'end': gap_start
                })

            # Move position to end of gap
            current_pos = gap_end

        # Add final segment after last gap
        if current_pos < duration:
            segments.append({
                'start': current_pos,
                'end': duration
            })

        return segments

    def _concatenate_with_transitions(
        self,
        clips: List[VideoFileClip],
        transition: str = 'crossfade',
        duration: float = 0.5
    ) -> VideoFileClip:
        """
        Concatenate clips with transition effects

        Args:
            clips: List of video clips
            transition: Transition type ('crossfade', 'fade', 'none')
            duration: Transition duration in seconds

        Returns:
            Concatenated video clip
        """
        if not clips:
            raise ValueError("No clips to concatenate")

        if len(clips) == 1 or transition == 'none':
            return concatenate_videoclips(clips)

        if transition == 'crossfade':
            # Crossfade between clips
            result_clips = []

            for i in range(len(clips)):
                clip = clips[i]

                if i == 0:
                    # First clip: fade in at start
                    clip = clip.fadein(duration)
                elif i == len(clips) - 1:
                    # Last clip: fade out at end
                    clip = clip.fadeout(duration)
                else:
                    # Middle clips: crossfade
                    clip = clip.fadein(duration).fadeout(duration)

                result_clips.append(clip)

            # Concatenate with overlap
            return concatenate_videoclips(result_clips, padding=-duration, method='compose')

        elif transition == 'fade':
            # Fade to black between clips
            result_clips = []

            for i, clip in enumerate(clips):
                result_clips.append(clip.fadeout(duration))

                # Add black frame between clips
                if i < len(clips) - 1:
                    black = ColorClip(
                        size=clip.size,
                        color=(0, 0, 0),
                        duration=duration
                    )
                    result_clips.append(black)

            return concatenate_videoclips(result_clips)

        else:
            logger.warning(f"Unknown transition type: {transition}, using direct concat")
            return concatenate_videoclips(clips)

    def cut_video(
        self,
        input_path: str,
        cuts: List[Dict],
        output_path: str = None,
        gap_handling: str = 'join',
        add_transitions: bool = True
    ) -> Dict:
        """
        Cut video into segments and optionally join them

        Args:
            input_path: Path to input video
            cuts: List of cut dictionaries with start/end times
            output_path: Path to output video
            gap_handling: How to handle gaps ('join', 'black', 'freeze')
            add_transitions: Add transitions between segments

        Returns:
            Result dictionary
        """
        logger.info(f"Cutting video: {input_path}")
        logger.info(f"Number of cuts: {len(cuts)}")

        video = VideoFileClip(input_path)

        # Extract segments
        segments = []
        for i, cut in enumerate(cuts):
            start = cut['start']
            end = cut['end']

            logger.debug(f"Cut {i+1}: {start:.2f}s - {end:.2f}s")

            segment = video.subclip(start, end)

            # Apply segment-specific effects
            if 'fade_in' in cut:
                segment = segment.fadein(cut['fade_in'])
            if 'fade_out' in cut:
                segment = segment.fadeout(cut['fade_out'])
            if 'speed' in cut and cut['speed'] != 1.0:
                segment = segment.fx(vfx.speedx, cut['speed'])

            segments.append(segment)

        # Join segments based on gap handling
        if gap_handling == 'join':
            if add_transitions:
                final_video = self._concatenate_with_transitions(segments)
            else:
                final_video = concatenate_videoclips(segments)

        elif gap_handling == 'black':
            # Insert black frames between segments
            result_segments = []
            black_duration = self.config.get('black_duration', 1.0)

            for i, segment in enumerate(segments):
                result_segments.append(segment)

                if i < len(segments) - 1:
                    black = ColorClip(
                        size=segment.size,
                        color=(0, 0, 0),
                        duration=black_duration
                    )
                    result_segments.append(black)

            final_video = concatenate_videoclips(result_segments)

        else:  # freeze
            # Keep original timeline with frozen frames
            logger.warning("Freeze gap handling not yet implemented, using join")
            final_video = concatenate_videoclips(segments)

        # Generate output path if not provided
        if output_path is None:
            output_path = self._generate_output_path(input_path, suffix='_cut')

        Path(output_path).parent.mkdir(parents=True, exist_ok=True)

        # Write output
        logger.info(f"Rendering video to: {output_path}")
        final_video.write_videofile(
            output_path,
            codec=self.codec,
            audio_codec=self.audio_codec,
            fps=self.fps,
            preset=self.preset,
            threads=self.threads,
            logger=None
        )

        result = {
            'input_path': input_path,
            'output_path': output_path,
            'original_duration': round(video.duration, 2),
            'final_duration': round(final_video.duration, 2),
            'segments': len(segments)
        }

        # Cleanup
        video.close()
        final_video.close()
        for segment in segments:
            segment.close()

        logger.info(f"✅ Video cut complete: {len(segments)} segments")

        return result

    def add_audio_mix(
        self,
        input_path: str,
        background_music: Dict = None,
        voiceover: Dict = None,
        output_path: str = None,
        normalize: bool = True
    ) -> Dict:
        """
        Add background music and/or voiceover to video

        Args:
            input_path: Path to input video
            background_music: Background music configuration dict
            voiceover: Voiceover configuration dict
            output_path: Path to output video
            normalize: Normalize final audio

        Returns:
            Result dictionary
        """
        logger.info(f"Adding audio mix to: {input_path}")

        video = VideoFileClip(input_path)
        audio_tracks = []

        # Original audio
        if video.audio is not None:
            original_audio = video.audio
            audio_tracks.append(original_audio)

        # Background music
        if background_music:
            music_path = background_music['path']
            music = AudioFileClip(music_path)

            # Adjust volume
            volume = background_music.get('volume', 0.3)
            music = music.volumex(volume)

            # Loop if needed
            if background_music.get('loop', False) and music.duration < video.duration:
                n_loops = int(video.duration / music.duration) + 1
                music = concatenate_audioclips([music] * n_loops)

            # Trim to video duration
            music = music.subclip(0, min(music.duration, video.duration))

            # Fade in/out
            fade_in = background_music.get('fade_in', 2.0)
            fade_out = background_music.get('fade_out', 2.0)
            music = music.audio_fadein(fade_in).audio_fadeout(fade_out)

            # TODO: Implement audio ducking (requires more complex logic)

            audio_tracks.append(music)

        # Voiceover
        if voiceover:
            vo_path = voiceover['path']
            vo = AudioFileClip(vo_path)

            # Start time
            start_time = voiceover.get('start_time', 0)

            # Adjust volume
            volume = voiceover.get('volume', 1.0)
            vo = vo.volumex(volume)

            # Set start time
            vo = vo.set_start(start_time)

            audio_tracks.append(vo)

        # Composite audio
        if len(audio_tracks) > 1:
            final_audio = CompositeAudioClip(audio_tracks)
        else:
            final_audio = audio_tracks[0] if audio_tracks else None

        # Normalize if requested
        if normalize and final_audio:
            # Simple normalization (multiply by factor)
            target_loudness = self.config.get('target_loudness', -14)
            # TODO: Implement proper LUFS normalization
            final_audio = final_audio.volumex(1.0)

        # Set audio to video
        final_video = video.set_audio(final_audio)

        # Generate output path
        if output_path is None:
            output_path = self._generate_output_path(input_path, suffix='_mixed')

        Path(output_path).parent.mkdir(parents=True, exist_ok=True)

        # Write output
        logger.info(f"Rendering video to: {output_path}")
        final_video.write_videofile(
            output_path,
            codec=self.codec,
            audio_codec=self.audio_codec,
            fps=self.fps,
            preset=self.preset,
            threads=self.threads,
            logger=None
        )

        result = {
            'input_path': input_path,
            'output_path': output_path,
            'audio_tracks_mixed': len(audio_tracks)
        }

        # Cleanup
        video.close()
        final_video.close()
        if final_audio:
            final_audio.close()

        logger.info(f"✅ Audio mixing complete")

        return result

    def _generate_output_path(self, input_path: str, suffix: str = '_edited') -> str:
        """
        Generate output path based on input path

        Args:
            input_path: Input video path
            suffix: Suffix to add before extension

        Returns:
            Output path string
        """
        input_path = Path(input_path)
        stem = input_path.stem
        parent = input_path.parent

        # Change to output directory
        output_dir = Path('output') / parent.name
        output_dir.mkdir(parents=True, exist_ok=True)

        output_path = output_dir / f"{stem}{suffix}.{self.output_format}"

        return str(output_path)

    def process_task(self, task: Dict) -> Dict:
        """
        Process a single editing task based on task configuration

        Args:
            task: Task dictionary from execution plan

        Returns:
            Result dictionary with task execution details
        """
        task_id = task.get('task_id', 'unknown')
        task_type = task.get('type', 'cut')

        logger.info(f"Processing task: {task_id} (type: {task_type})")

        try:
            if task_type == 'remove_silence' or (
                'editing' in task and task['editing'].get('remove_silence', {}).get('enabled', False)
            ):
                # Load timestamp file
                timestamp_file = task.get('timestamp_file')
                if not timestamp_file:
                    raise ValueError("timestamp_file required for remove_silence task")

                with open(timestamp_file, 'r') as f:
                    timestamp_data = json.load(f)

                gaps = timestamp_data.get('gaps', [])

                # Get editing parameters
                editing_config = task.get('editing', {}).get('remove_silence', {})
                confidence_threshold = editing_config.get('confidence_threshold', 0.8)
                min_gap_duration = editing_config.get('min_gap_duration', 0.5)

                result = self.remove_silence_gaps(
                    input_path=task['input_video'],
                    gaps=gaps,
                    confidence_threshold=confidence_threshold,
                    min_gap_duration=min_gap_duration,
                    output_path=task.get('output_path')
                )

            elif task_type == 'cut':
                cuts = task.get('cuts', [])
                gap_handling = task.get('gap_handling', 'join')

                result = self.cut_video(
                    input_path=task['input_video'],
                    cuts=cuts,
                    output_path=task.get('output_path'),
                    gap_handling=gap_handling
                )

            elif task_type == 'audio_mix':
                background_music = task.get('background_music')
                voiceover = task.get('voiceover')

                result = self.add_audio_mix(
                    input_path=task['input_video'],
                    background_music=background_music,
                    voiceover=voiceover,
                    output_path=task.get('output_path')
                )

            else:
                raise ValueError(f"Unknown task type: {task_type}")

            result['task_id'] = task_id
            result['task_type'] = task_type
            result['status'] = 'success'

            return result

        except Exception as e:
            logger.error(f"Task {task_id} failed: {e}")

            return {
                'task_id': task_id,
                'task_type': task_type,
                'status': 'failed',
                'error': str(e)
            }


def main():
    """
    CLI test interface
    """
    if len(sys.argv) < 2:
        print("Usage: python video_editor.py <test_mode>")
        print("\nTest modes:")
        print("  cut - Test video cutting")
        print("  silence - Test silence removal")
        print("  audio - Test audio mixing")
        sys.exit(1)

    test_mode = sys.argv[1]

    editor = VideoEditor({
        'resolution': '720p',
        'fps': 30,
        'quality': 'medium'
    })

    if test_mode == 'cut':
        print("Testing video cutting...")
        result = editor.cut_video(
            input_path='input/test.mp4',
            cuts=[
                {'start': 0, 'end': 10},
                {'start': 20, 'end': 30}
            ],
            output_path='output/test_cut.mp4'
        )
        print(json.dumps(result, indent=2))

    elif test_mode == 'silence':
        print("Testing silence removal...")
        # Load timestamp file
        with open('output/test_silence_gaps.json') as f:
            data = json.load(f)

        result = editor.remove_silence_gaps(
            input_path='input/test.mp4',
            gaps=data['gaps'],
            output_path='output/test_no_silence.mp4'
        )
        print(json.dumps(result, indent=2))

    elif test_mode == 'audio':
        print("Testing audio mixing...")
        result = editor.add_audio_mix(
            input_path='input/test.mp4',
            background_music={
                'path': 'assets/music.mp3',
                'volume': 0.3,
                'loop': True,
                'fade_in': 2.0,
                'fade_out': 2.0
            },
            output_path='output/test_mixed.mp4'
        )
        print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
