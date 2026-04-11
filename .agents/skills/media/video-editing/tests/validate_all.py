#!/usr/bin/env python3
"""
完整验证脚本 - Video Editing Skills
运行所有验证检查,生成详细报告

使用方法:
    python tests/validate_all.py
    python tests/validate_all.py --quick  # 快速验证,跳过测试
    python tests/validate_all.py --report output/validation_report.md
"""

import os
import sys
import subprocess
import json
from pathlib import Path
from datetime import datetime
import argparse

class ValidationReport:
    """验证报告生成器"""

    def __init__(self):
        self.checks = []
        self.start_time = datetime.now()

    def add_check(self, name, status, message, details=None):
        """添加检查结果"""
        self.checks.append({
            'name': name,
            'status': status,  # 'pass', 'fail', 'warning'
            'message': message,
            'details': details or {}
        })

    def generate_report(self, output_path=None):
        """生成Markdown报告"""
        end_time = datetime.now()
        duration = (end_time - self.start_time).total_seconds()

        # 统计结果
        passed = sum(1 for c in self.checks if c['status'] == 'pass')
        failed = sum(1 for c in self.checks if c['status'] == 'fail')
        warnings = sum(1 for c in self.checks if c['status'] == 'warning')
        total = len(self.checks)

        # 生成报告
        report = f"""# Video Editing Skills - 验证报告

**生成时间**: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}
**验证耗时**: {duration:.2f}秒
**验证项目**: {total}项

## 📊 验证结果摘要

| 状态 | 数量 | 百分比 |
|------|------|--------|
| ✅ 通过 | {passed} | {passed/total*100:.1f}% |
| ❌ 失败 | {failed} | {failed/total*100:.1f}% |
| ⚠️  警告 | {warnings} | {warnings/total*100:.1f}% |
| **总计** | **{total}** | **100%** |

"""

        # 详细检查结果
        report += "## 📋 详细检查结果\n\n"

        for i, check in enumerate(self.checks, 1):
            status_icon = {
                'pass': '✅',
                'fail': '❌',
                'warning': '⚠️'
            }[check['status']]

            report += f"### {i}. {status_icon} {check['name']}\n\n"
            report += f"**状态**: {check['status'].upper()}\n\n"
            report += f"{check['message']}\n\n"

            if check['details']:
                report += "**详细信息**:\n"
                for key, value in check['details'].items():
                    report += f"- {key}: `{value}`\n"
                report += "\n"

        # 建议行动
        if failed > 0:
            report += "## ⚠️ 需要采取的行动\n\n"
            for check in self.checks:
                if check['status'] == 'fail':
                    report += f"- **{check['name']}**: {check['message']}\n"

        report += "\n---\n\n"
        report += f"*报告生成于: {end_time.strftime('%Y-%m-%d %H:%M:%S')}*\n"

        # 输出报告
        if output_path:
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(report)
            print(f"\n📄 验证报告已保存: {output_path}")

        return report

def check_python_version(report):
    """检查Python版本"""
    version = sys.version_info
    version_str = f"{version.major}.{version.minor}.{version.micro}"

    if version.major == 3 and 10 <= version.minor <= 13:
        report.add_check(
            'Python版本',
            'pass',
            f'Python版本正确: {version_str}',
            {'version': version_str, 'required': '3.10-3.13'}
        )
        return True
    else:
        report.add_check(
            'Python版本',
            'fail',
            f'Python版本不兼容: {version_str}。需要3.10-3.13',
            {'version': version_str, 'required': '3.10-3.13'}
        )
        return False

def check_ffmpeg(report):
    """检查FFmpeg"""
    try:
        result = subprocess.run(
            ['ffmpeg', '-version'],
            capture_output=True,
            text=True,
            timeout=5
        )
        version_line = result.stdout.split('\n')[0]
        report.add_check(
            'FFmpeg',
            'pass',
            f'FFmpeg已安装: {version_line}',
            {'version': version_line}
        )
        return True
    except FileNotFoundError:
        report.add_check(
            'FFmpeg',
            'fail',
            'FFmpeg未找到。请安装FFmpeg: brew install ffmpeg (macOS) 或 sudo apt-get install ffmpeg (Linux)',
            {}
        )
        return False
    except subprocess.TimeoutExpired:
        report.add_check(
            'FFmpeg',
            'warning',
            'FFmpeg响应超时',
            {}
        )
        return False

def check_python_packages(report):
    """检查Python依赖包"""
    required_packages = {
        'moviepy': 'MoviePy',
        'numpy': 'NumPy',
        'scipy': 'SciPy',
        'librosa': 'Librosa',
        'PIL': 'Pillow'
    }

    all_ok = True

    for package_name, display_name in required_packages.items():
        try:
            if package_name == 'PIL':
                import PIL
                version = PIL.__version__
            else:
                module = __import__(package_name)
                version = module.__version__

            report.add_check(
                f'{display_name}',
                'pass',
                f'{display_name} {version} 已安装',
                {'package': package_name, 'version': version}
            )
        except ImportError:
            report.add_check(
                f'{display_name}',
                'fail',
                f'{display_name} 未安装。请运行: pip install {package_name}',
                {'package': package_name}
            )
            all_ok = False

    return all_ok

def check_directory_structure(report):
    """检查目录结构"""
    required_dirs = [
        '.agents/skills/timestamp-extraction',
        '.agents/skills/timestamp-extraction/scripts',
        '.agents/skills/timestamp-extraction/templates',
        '.agents/skills/video-editing',
        '.agents/skills/video-editing/scripts',
        '.agents/skills/video-editing/templates',
        'tests/data',
        'tests/output'
    ]

    all_exist = True

    for dir_path in required_dirs:
        if Path(dir_path).is_dir():
            report.add_check(
                f'目录: {dir_path}',
                'pass',
                f'目录存在',
                {'path': dir_path}
            )
        else:
            report.add_check(
                f'目录: {dir_path}',
                'fail',
                f'目录不存在: {dir_path}',
                {'path': dir_path}
            )
            all_exist = False

    return all_exist

def check_core_files(report):
    """检查核心文件"""
    required_files = [
        '.agents/skills/timestamp-extraction/SKILL.md',
        '.agents/skills/timestamp-extraction/scripts/timestamp_extractor.py',
        '.agents/skills/timestamp-extraction/scripts/plan_executor.py',
        '.agents/skills/video-editing/SKILL.md',
        '.agents/skills/video-editing/scripts/video_editor.py',
        '.agents/skills/video-editing/scripts/plan_executor.py',
        '.agents/skills/video-editing/TESTING.md',
        '.agents/skills/video-editing/DEPLOYMENT.md',
        '.agents/skills/video-editing/QUICKSTART.md'
    ]

    all_exist = True

    for file_path in required_files:
        if Path(file_path).is_file():
            size = Path(file_path).stat().st_size
            report.add_check(
                f'文件: {Path(file_path).name}',
                'pass',
                f'文件存在 ({size} bytes)',
                {'path': file_path, 'size': size}
            )
        else:
            report.add_check(
                f'文件: {file_path}',
                'fail',
                f'文件不存在: {file_path}',
                {'path': file_path}
            )
            all_exist = False

    return all_exist

def check_test_data(report):
    """检查测试数据"""
    test_files = [
        'tests/data/short_video.mp4',
        'tests/data/podcast.mp4',
        'tests/data/interview.mp4'
    ]

    has_data = False

    for file_path in test_files:
        if Path(file_path).exists():
            size = Path(file_path).stat().st_size / (1024 * 1024)  # MB
            report.add_check(
                f'测试视频: {Path(file_path).name}',
                'pass',
                f'测试数据就绪 ({size:.2f} MB)',
                {'path': file_path, 'size_mb': f'{size:.2f}'}
            )
            has_data = True
        else:
            report.add_check(
                f'测试视频: {Path(file_path).name}',
                'warning',
                f'测试数据缺失。运行: python tests/prepare_test_data.py --mode generate',
                {'path': file_path}
            )

    return has_data

def check_code_syntax(report):
    """检查Python代码语法"""
    python_files = [
        '.agents/skills/timestamp-extraction/scripts/timestamp_extractor.py',
        '.agents/skills/timestamp-extraction/scripts/plan_executor.py',
        '.agents/skills/video-editing/scripts/video_editor.py',
        '.agents/skills/video-editing/scripts/plan_executor.py'
    ]

    all_valid = True

    for file_path in python_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                code = f.read()
            compile(code, file_path, 'exec')
            report.add_check(
                f'语法检查: {Path(file_path).name}',
                'pass',
                f'Python语法正确',
                {'path': file_path}
            )
        except SyntaxError as e:
            report.add_check(
                f'语法检查: {Path(file_path).name}',
                'fail',
                f'语法错误: {str(e)}',
                {'path': file_path, 'error': str(e)}
            )
            all_valid = False
        except Exception as e:
            report.add_check(
                f'语法检查: {Path(file_path).name}',
                'warning',
                f'检查异常: {str(e)}',
                {'path': file_path, 'error': str(e)}
            )

    return all_valid

def check_json_templates(report):
    """检查JSON模板"""
    json_files = list(Path('.agents/skills/timestamp-extraction/templates').glob('*.json')) + \
                 list(Path('.agents/skills/video-editing/templates').glob('*.json'))

    all_valid = True

    for file_path in json_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                json.load(f)
            report.add_check(
                f'JSON模板: {file_path.name}',
                'pass',
                f'JSON格式正确',
                {'path': str(file_path)}
            )
        except json.JSONDecodeError as e:
            report.add_check(
                f'JSON模板: {file_path.name}',
                'fail',
                f'JSON格式错误: {str(e)}',
                {'path': str(file_path), 'error': str(e)}
            )
            all_valid = False

    return all_valid

def run_quick_tests(report):
    """运行快速功能测试"""
    # 这里可以添加简单的功能测试
    # 由于需要MoviePy环境,暂时跳过
    report.add_check(
        '快速功能测试',
        'warning',
        '功能测试需要MoviePy环境,请运行完整测试套件',
        {}
    )
    return True

def main():
    parser = argparse.ArgumentParser(
        description='Video Editing Skills 完整验证'
    )
    parser.add_argument(
        '--quick',
        action='store_true',
        help='快速验证,跳过测试执行'
    )
    parser.add_argument(
        '--report',
        type=str,
        default='tests/output/validation_report.md',
        help='验证报告输出路径'
    )

    args = parser.parse_args()

    print('=' * 70)
    print('Video Editing Skills - 完整验证')
    print('=' * 70)
    print()

    report = ValidationReport()

    # 1. 环境检查
    print('📋 环境检查...')
    check_python_version(report)
    check_ffmpeg(report)
    check_python_packages(report)
    print('  完成\n')

    # 2. 结构检查
    print('📂 目录结构检查...')
    check_directory_structure(report)
    print('  完成\n')

    # 3. 文件检查
    print('📄 核心文件检查...')
    check_core_files(report)
    print('  完成\n')

    # 4. 测试数据检查
    print('🎬 测试数据检查...')
    check_test_data(report)
    print('  完成\n')

    # 5. 代码质量检查
    print('🔍 代码质量检查...')
    check_code_syntax(report)
    check_json_templates(report)
    print('  完成\n')

    # 6. 功能测试 (可选)
    if not args.quick:
        print('🧪 快速功能测试...')
        run_quick_tests(report)
        print('  完成\n')

    # 生成报告
    print('📊 生成验证报告...')
    report_content = report.generate_report(args.report)
    print('  完成\n')

    # 打印控制台摘要
    print('=' * 70)
    print('验证完成!')
    print('=' * 70)
    print()

    # 统计结果
    passed = sum(1 for c in report.checks if c['status'] == 'pass')
    failed = sum(1 for c in report.checks if c['status'] == 'fail')
    warnings = sum(1 for c in report.checks if c['status'] == 'warning')
    total = len(report.checks)

    print(f'✅ 通过: {passed}/{total}')
    print(f'❌ 失败: {failed}/{total}')
    print(f'⚠️  警告: {warnings}/{total}')
    print()

    if failed > 0:
        print('⚠️  发现问题,请查看验证报告获取详细信息')
        print(f'📄 报告位置: {args.report}')
        sys.exit(1)
    elif warnings > 0:
        print('✅ 验证通过,但有警告')
        print(f'📄 报告位置: {args.report}')
        sys.exit(0)
    else:
        print('✅ 所有检查通过!')
        print(f'📄 报告位置: {args.report}')
        sys.exit(0)

if __name__ == '__main__':
    main()
