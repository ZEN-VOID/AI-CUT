#!/usr/bin/env python3
"""
Video Editing Skills - 安装验证脚本
快速检查环境是否正确配置

使用方法:
    python check_installation.py
"""

import sys
import subprocess
from pathlib import Path


def check_python_version():
    """检查Python版本"""
    version = sys.version_info
    version_str = f"{version.major}.{version.minor}.{version.micro}"

    print("=" * 60)
    print("Python版本检查")
    print("=" * 60)
    print(f"当前版本: {version_str}")

    if version.major == 3 and 10 <= version.minor <= 13:
        print("✅ Python版本正确 (需要3.10-3.13)")
        return True
    else:
        print(f"❌ Python版本不兼容!")
        print(f"   当前: {version_str}")
        print(f"   需要: 3.10-3.13")
        print("\n建议:")
        print("  1. 使用pyenv安装Python 3.12:")
        print("     brew install pyenv")
        print("     pyenv install 3.12.0")
        print("     pyenv local 3.12.0")
        print("\n  2. 或使用conda:")
        print("     conda create -n video-editing python=3.12")
        print("     conda activate video-editing")
        return False


def check_ffmpeg():
    """检查FFmpeg"""
    print("\n" + "=" * 60)
    print("FFmpeg检查")
    print("=" * 60)

    try:
        result = subprocess.run(
            ['ffmpeg', '-version'],
            capture_output=True,
            text=True,
            timeout=5
        )
        version_line = result.stdout.split('\n')[0]
        print(f"✅ FFmpeg已安装: {version_line}")
        return True
    except FileNotFoundError:
        print("❌ FFmpeg未找到!")
        print("\n建议:")
        print("  macOS:  brew install ffmpeg")
        print("  Ubuntu: sudo apt-get install ffmpeg")
        print("  CentOS: sudo yum install ffmpeg")
        return False
    except subprocess.TimeoutExpired:
        print("⚠️  FFmpeg响应超时")
        return False


def check_python_packages():
    """检查Python依赖包"""
    print("\n" + "=" * 60)
    print("Python依赖包检查")
    print("=" * 60)

    packages = {
        'moviepy': 'MoviePy',
        'numpy': 'NumPy',
        'scipy': 'SciPy',
        'librosa': 'Librosa',
        'PIL': 'Pillow'
    }

    all_installed = True

    for package_name, display_name in packages.items():
        try:
            if package_name == 'PIL':
                import PIL
                version = PIL.__version__
            else:
                module = __import__(package_name)
                version = module.__version__

            print(f"✅ {display_name} {version}")
        except ImportError:
            print(f"❌ {display_name} 未安装")
            all_installed = False

    if not all_installed:
        print("\n建议:")
        print("  pip install moviepy librosa numpy scipy pillow")

    return all_installed


def check_directory_structure():
    """检查目录结构"""
    print("\n" + "=" * 60)
    print("目录结构检查")
    print("=" * 60)

    skill_root = Path(__file__).parent

    required_dirs = [
        'scripts',
        'templates',
        'tests',
        'tests/data',
        'tests/output',
        'examples'
    ]

    all_exist = True

    for dir_name in required_dirs:
        dir_path = skill_root / dir_name
        if dir_path.is_dir():
            print(f"✅ {dir_name}/")
        else:
            print(f"❌ {dir_name}/ (缺失)")
            all_exist = False

    return all_exist


def check_core_files():
    """检查核心文件"""
    print("\n" + "=" * 60)
    print("核心文件检查")
    print("=" * 60)

    skill_root = Path(__file__).parent

    required_files = [
        'SKILL.md',
        'scripts/video_editor.py',
        'scripts/plan_executor.py',
        'TESTING.md',
        'DEPLOYMENT.md',
        'QUICKSTART.md'
    ]

    all_exist = True

    for file_name in required_files:
        file_path = skill_root / file_name
        if file_path.is_file():
            size = file_path.stat().st_size
            print(f"✅ {file_name} ({size} bytes)")
        else:
            print(f"❌ {file_name} (缺失)")
            all_exist = False

    return all_exist


def main():
    """主函数"""
    print("\n")
    print("*" * 60)
    print("Video Editing Skills - 安装验证")
    print("*" * 60)
    print("\n")

    checks = [
        ("Python版本", check_python_version),
        ("FFmpeg", check_ffmpeg),
        ("Python依赖包", check_python_packages),
        ("目录结构", check_directory_structure),
        ("核心文件", check_core_files)
    ]

    results = []
    for name, check_func in checks:
        result = check_func()
        results.append((name, result))

    # 总结
    print("\n" + "=" * 60)
    print("验证总结")
    print("=" * 60)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = "✅" if result else "❌"
        print(f"{status} {name}")

    print("\n" + "-" * 60)
    print(f"通过: {passed}/{total}")

    if passed == total:
        print("\n🎉 所有检查通过! 环境配置正确.")
        print("\n下一步:")
        print("  1. 准备测试数据:")
        print("     python tests/prepare_test_data.py --mode generate")
        print("\n  2. 运行第一个任务:")
        print("     python scripts/plan_executor.py templates/podcast-edit.json")
        sys.exit(0)
    else:
        print("\n⚠️  部分检查失败,请根据上述建议修复问题.")
        print("\n完整验证报告:")
        print("  python tests/validate_all.py")
        sys.exit(1)


if __name__ == '__main__':
    main()
