#!/usr/bin/env python3
"""
测试数据准备脚本
为Video Editing Skills生成或下载测试视频

使用方法:
    python tests/prepare_test_data.py --mode generate
    python tests/prepare_test_data.py --mode download
"""

import os
import sys
from pathlib import Path
import argparse

def create_test_directories():
    """创建测试目录结构"""
    dirs = [
        'tests/data',
        'tests/output/timestamp',
        'tests/output/video',
        'tests/output/reports'
    ]

    for dir_path in dirs:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
        print(f'✅ 创建目录: {dir_path}')

def generate_synthetic_video():
    """使用MoviePy生成合成测试视频

    需要MoviePy环境可用
    """
    try:
        from moviepy.editor import (
            ColorClip, TextClip, CompositeVideoClip, AudioClip,
            concatenate_videoclips
        )
        import numpy as np
    except ImportError:
        print('❌ MoviePy未安装。请先运行: pip install moviepy')
        print('   或使用 --mode download 下载预制测试视频')
        return False

    print('\n🎬 生成合成测试视频...')

    # 1. 短视频 (30秒) - 用于快速测试
    print('  生成 short_video.mp4 (30秒)...')
    clips = []

    # 场景1: 5秒蓝色背景 + 文字
    clip1 = ColorClip(size=(1920, 1080), color=(0, 100, 200), duration=5)
    txt1 = TextClip("Scene 1", fontsize=70, color='white', font='Arial')
    txt1 = txt1.set_position('center').set_duration(5)
    scene1 = CompositeVideoClip([clip1, txt1])
    clips.append(scene1)

    # 静音片段: 2秒黑屏
    silence1 = ColorClip(size=(1920, 1080), color=(0, 0, 0), duration=2)
    clips.append(silence1)

    # 场景2: 5秒红色背景
    clip2 = ColorClip(size=(1920, 1080), color=(200, 50, 50), duration=5)
    txt2 = TextClip("Scene 2", fontsize=70, color='white', font='Arial')
    txt2 = txt2.set_position('center').set_duration(5)
    scene2 = CompositeVideoClip([clip2, txt2])
    clips.append(scene2)

    # 静音片段: 3秒黑屏
    silence2 = ColorClip(size=(1920, 1080), color=(0, 0, 0), duration=3)
    clips.append(silence2)

    # 场景3: 5秒绿色背景
    clip3 = ColorClip(size=(1920, 1080), color=(50, 200, 50), duration=5)
    txt3 = TextClip("Scene 3", fontsize=70, color='white', font='Arial')
    txt3 = txt3.set_position('center').set_duration(5)
    scene3 = CompositeVideoClip([clip3, txt3])
    clips.append(scene3)

    # 静音片段: 1.5秒黑屏
    silence3 = ColorClip(size=(1920, 1080), color=(0, 0, 0), duration=1.5)
    clips.append(silence3)

    # 场景4: 7.5秒黄色背景
    clip4 = ColorClip(size=(1920, 1080), color=(200, 200, 50), duration=7.5)
    txt4 = TextClip("Scene 4", fontsize=70, color='white', font='Arial')
    txt4 = txt4.set_position('center').set_duration(7.5)
    scene4 = CompositeVideoClip([clip4, txt4])
    clips.append(scene4)

    # 合成最终视频
    final = concatenate_videoclips(clips)

    # 添加简单音频 (正弦波音调)
    def make_audio(t):
        # 在非静音片段添加音频
        if 0 <= t < 5 or 7 <= t < 12 or 15 <= t < 20 or 21.5 <= t < 29:
            return np.sin(2 * np.pi * 440 * t) * 0.3  # 440Hz音调
        return 0  # 静音

    audio = AudioClip(make_audio, duration=final.duration)
    final = final.set_audio(audio)

    # 导出
    final.write_videofile(
        'tests/data/short_video.mp4',
        fps=24,
        codec='libx264',
        audio_codec='aac',
        verbose=False,
        logger=None
    )
    print('  ✅ short_video.mp4 生成成功')

    # 2. 播客视频 (60秒) - 用于播客剪辑测试
    print('  生成 podcast.mp4 (60秒)...')
    podcast_clips = []

    # 讲话片段: 8秒
    talk1 = ColorClip(size=(1920, 1080), color=(30, 30, 80), duration=8)
    txt_talk1 = TextClip("Podcast Intro", fontsize=60, color='white', font='Arial')
    txt_talk1 = txt_talk1.set_position('center').set_duration(8)
    podcast_clips.append(CompositeVideoClip([talk1, txt_talk1]))

    # 停顿: 3秒
    podcast_clips.append(ColorClip(size=(1920, 1080), color=(10, 10, 10), duration=3))

    # 讲话片段: 12秒
    talk2 = ColorClip(size=(1920, 1080), color=(30, 30, 80), duration=12)
    txt_talk2 = TextClip("Main Content", fontsize=60, color='white', font='Arial')
    txt_talk2 = txt_talk2.set_position('center').set_duration(12)
    podcast_clips.append(CompositeVideoClip([talk2, txt_talk2]))

    # 停顿: 4秒
    podcast_clips.append(ColorClip(size=(1920, 1080), color=(10, 10, 10), duration=4))

    # 讲话片段: 15秒
    talk3 = ColorClip(size=(1920, 1080), color=(30, 30, 80), duration=15)
    txt_talk3 = TextClip("Discussion", fontsize=60, color='white', font='Arial')
    txt_talk3 = txt_talk3.set_position('center').set_duration(15)
    podcast_clips.append(CompositeVideoClip([talk3, txt_talk3]))

    # 停顿: 2秒
    podcast_clips.append(ColorClip(size=(1920, 1080), color=(10, 10, 10), duration=2))

    # 讲话片段: 10秒
    talk4 = ColorClip(size=(1920, 1080), color=(30, 30, 80), duration=10)
    txt_talk4 = TextClip("Conclusion", fontsize=60, color='white', font='Arial')
    txt_talk4 = txt_talk4.set_position('center').set_duration(10)
    podcast_clips.append(CompositeVideoClip([talk4, txt_talk4]))

    # 停顿: 6秒 (结尾长停顿)
    podcast_clips.append(ColorClip(size=(1920, 1080), color=(10, 10, 10), duration=6))

    podcast_final = concatenate_videoclips(podcast_clips)

    # 添加音频
    def make_podcast_audio(t):
        # 讲话片段有音频,停顿无音频
        if (0 <= t < 8 or 11 <= t < 23 or 27 <= t < 42 or 44 <= t < 54):
            freq = 200 + 100 * np.sin(0.5 * t)  # 变化的语音频率
            return np.sin(2 * np.pi * freq * t) * 0.2
        return 0

    podcast_audio = AudioClip(make_podcast_audio, duration=podcast_final.duration)
    podcast_final = podcast_final.set_audio(podcast_audio)

    podcast_final.write_videofile(
        'tests/data/podcast.mp4',
        fps=24,
        codec='libx264',
        audio_codec='aac',
        verbose=False,
        logger=None
    )
    print('  ✅ podcast.mp4 生成成功')

    # 3. 访谈视频 (90秒) - 用于多机位测试
    print('  生成 interview.mp4 (90秒)...')
    interview_clips = []

    # 主持人: 10秒
    host1 = ColorClip(size=(1920, 1080), color=(80, 30, 30), duration=10)
    txt_host1 = TextClip("Host Question", fontsize=60, color='white', font='Arial')
    txt_host1 = txt_host1.set_position('center').set_duration(10)
    interview_clips.append(CompositeVideoClip([host1, txt_host1]))

    # 嘉宾: 20秒
    guest1 = ColorClip(size=(1920, 1080), color=(30, 80, 30), duration=20)
    txt_guest1 = TextClip("Guest Answer", fontsize=60, color='white', font='Arial')
    txt_guest1 = txt_guest1.set_position('center').set_duration(20)
    interview_clips.append(CompositeVideoClip([guest1, txt_guest1]))

    # 主持人: 8秒
    host2 = ColorClip(size=(1920, 1080), color=(80, 30, 30), duration=8)
    txt_host2 = TextClip("Host Follow-up", fontsize=60, color='white', font='Arial')
    txt_host2 = txt_host2.set_position('center').set_duration(8)
    interview_clips.append(CompositeVideoClip([host2, txt_host2]))

    # 嘉宾: 25秒
    guest2 = ColorClip(size=(1920, 1080), color=(30, 80, 30), duration=25)
    txt_guest2 = TextClip("Guest Explanation", fontsize=60, color='white', font='Arial')
    txt_guest2 = txt_guest2.set_position('center').set_duration(25)
    interview_clips.append(CompositeVideoClip([guest2, txt_guest2]))

    # 主持人: 12秒
    host3 = ColorClip(size=(1920, 1080), color=(80, 30, 30), duration=12)
    txt_host3 = TextClip("Host Summary", fontsize=60, color='white', font='Arial')
    txt_host3 = txt_host3.set_position('center').set_duration(12)
    interview_clips.append(CompositeVideoClip([host3, txt_host3]))

    # 嘉宾: 15秒
    guest3 = ColorClip(size=(1920, 1080), color=(30, 80, 30), duration=15)
    txt_guest3 = TextClip("Guest Final Thoughts", fontsize=60, color='white', font='Arial')
    txt_guest3 = txt_guest3.set_position('center').set_duration(15)
    interview_clips.append(CompositeVideoClip([guest3, txt_guest3]))

    interview_final = concatenate_videoclips(interview_clips)

    # 添加音频 (主持人和嘉宾不同频率)
    def make_interview_audio(t):
        # 主持人片段: 0-10, 30-38, 63-75 (低频)
        # 嘉宾片段: 10-30, 38-63, 75-90 (高频)
        if (0 <= t < 10 or 30 <= t < 38 or 63 <= t < 75):
            return np.sin(2 * np.pi * 250 * t) * 0.25  # 主持人声音
        else:
            return np.sin(2 * np.pi * 350 * t) * 0.25  # 嘉宾声音

    interview_audio = AudioClip(make_interview_audio, duration=interview_final.duration)
    interview_final = interview_final.set_audio(interview_audio)

    interview_final.write_videofile(
        'tests/data/interview.mp4',
        fps=24,
        codec='libx264',
        audio_codec='aac',
        verbose=False,
        logger=None
    )
    print('  ✅ interview.mp4 生成成功')

    print('\n✅ 所有测试视频生成完成!')
    print('\n生成的文件:')
    print('  - tests/data/short_video.mp4(30秒)')
    print('  - tests/data/podcast.mp4(60秒)')
    print('  - tests/data/interview.mp4(90秒)')

    return True

def download_test_videos():
    """下载预制测试视频

    使用公开可用的测试视频
    """
    print('\n📥 下载测试视频...')
    print('\n选项1: 手动下载')
    print('  请访问以下网址下载测试视频:')
    print('  - https://test-videos.co.uk/vids/bigbuckbunny/mp4/h264/360/Big_Buck_Bunny_360_10s_1MB.mp4')
    print('  - https://test-videos.co.uk/vids/bigbuckbunny/mp4/h264/720/Big_Buck_Bunny_720_10s_5MB.mp4')
    print('  下载后重命名并放置到 tests/data/ 目录')

    print('\n选项2: 使用wget/curl下载')
    print('  运行以下命令:')
    print('  wget -O tests/data/short_video.mp4 https://test-videos.co.uk/vids/bigbuckbunny/mp4/h264/360/Big_Buck_Bunny_360_10s_1MB.mp4')

    print('\n选项3: 使用本地已有视频')
    print('  将任意MP4视频复制到 tests/data/ 目录并重命名为:')
    print('  - short_video.mp4 (建议30秒左右)')
    print('  - podcast.mp4 (建议60秒左右)')
    print('  - interview.mp4 (建议90秒左右)')

    return True

def verify_test_data():
    """验证测试数据是否就绪"""
    required_files = [
        'tests/data/short_video.mp4',
        'tests/data/podcast.mp4',
        'tests/data/interview.mp4'
    ]

    print('\n🔍 验证测试数据...')
    all_present = True

    for file_path in required_files:
        if Path(file_path).exists():
            size = Path(file_path).stat().st_size / (1024 * 1024)  # MB
            print(f'  ✅ {file_path} ({size:.2f} MB)')
        else:
            print(f'  ❌ {file_path} (缺失)')
            all_present = False

    if all_present:
        print('\n✅ 所有测试数据就绪!')
        return True
    else:
        print('\n⚠️  部分测试数据缺失。请运行生成或下载命令。')
        return False

def main():
    parser = argparse.ArgumentParser(
        description='准备Video Editing Skills测试数据'
    )
    parser.add_argument(
        '--mode',
        choices=['generate', 'download', 'verify'],
        default='verify',
        help='操作模式: generate(生成), download(下载), verify(验证)'
    )

    args = parser.parse_args()

    print('=' * 60)
    print('Video Editing Skills - 测试数据准备工具')
    print('=' * 60)

    # 创建目录
    create_test_directories()

    if args.mode == 'generate':
        success = generate_synthetic_video()
        if not success:
            sys.exit(1)
    elif args.mode == 'download':
        download_test_videos()
    elif args.mode == 'verify':
        if not verify_test_data():
            print('\n提示: 运行以下命令准备测试数据:')
            print('  python tests/prepare_test_data.py --mode generate')
            print('  或')
            print('  python tests/prepare_test_data.py --mode download')
            sys.exit(1)

    print('\n' + '=' * 60)

if __name__ == '__main__':
    main()
