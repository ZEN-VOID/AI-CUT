#!/usr/bin/env python3
"""
Timestamp Extraction - Plan Executor
=====================================

批量执行引擎，读取JSON计划并执行时间戳提取任务。

Usage:
    python plan_executor.py <plan_json_path>

Example:
    python plan_executor.py ../templates/podcast.json
    python plan_executor.py output/plans/my-plan.json

Author: AIGC Digital Nomad Film Company
Version: 1.0.0
"""

import os
import sys
import json
import time
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

# 添加scripts目录到Python路径
sys.path.insert(0, str(Path(__file__).parent))

from core_engine import TimestampExtractor

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('timestamp_extraction.log')
    ]
)
logger = logging.getLogger(__name__)


class PlanExecutor:
    """
    批量执行引擎

    Features:
    - 读取JSON计划文件
    - 批量处理多个视频
    - 进度追踪
    - 错误处理与重试
    - 结果保存（JSON + 可选可视化）
    - 执行报告生成
    """

    def __init__(self, plan_path: str):
        """
        初始化执行器

        Args:
            plan_path: JSON计划文件路径
        """
        self.plan_path = plan_path
        self.plan = self._load_plan(plan_path)
        self.plan_id = self.plan.get('plan_id', self._generate_plan_id())
        self.config = self.plan.get('config', {})
        self.tasks = self.plan.get('tasks', [])

        # 创建提取器
        self.extractor = TimestampExtractor(self.config)

        # 执行状态
        self.results = []
        self.failed_tasks = []
        self.start_time = None
        self.end_time = None

        logger.info(f"PlanExecutor initialized with plan: {self.plan_id}")
        logger.info(f"Total tasks: {len(self.tasks)}")

    def _load_plan(self, plan_path: str) -> Dict:
        """
        加载JSON计划文件

        Args:
            plan_path: JSON文件路径

        Returns:
            计划字典
        """
        logger.info(f"Loading plan from: {plan_path}")

        if not os.path.exists(plan_path):
            raise FileNotFoundError(f"Plan file not found: {plan_path}")

        with open(plan_path, 'r', encoding='utf-8') as f:
            plan = json.load(f)

        # 验证必需字段
        if 'tasks' not in plan or not plan['tasks']:
            raise ValueError("Plan must contain at least one task")

        logger.info(f"Plan loaded successfully: {len(plan['tasks'])} tasks")
        return plan

    def _generate_plan_id(self) -> str:
        """
        生成唯一的计划ID

        Returns:
            计划ID字符串
        """
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        return f"plan-{timestamp}"

    def execute(self) -> Dict:
        """
        执行计划中的所有任务

        Returns:
            执行报告字典
        """
        logger.info("="*60)
        logger.info(f"STARTING PLAN EXECUTION: {self.plan_id}")
        logger.info("="*60)

        self.start_time = time.time()

        # 执行每个任务
        for i, task in enumerate(self.tasks, 1):
            task_id = task.get('task_id', f"task-{i:03d}")

            logger.info(f"\n[{i}/{len(self.tasks)}] Processing: {task_id}")

            try:
                # 处理任务
                task_start = time.time()
                result = self.extractor.process_task(task)
                task_end = time.time()

                # 添加处理时间
                result['statistics']['processing_time'] = round(task_end - task_start, 2)

                # 保存结果
                output_dir = task.get('output_dir', f"output/{self.plan_id}")
                self._save_task_result(result, output_dir)

                self.results.append(result)

                logger.info(f"✅ Task {task_id} completed in {result['statistics']['processing_time']}s")

            except Exception as e:
                logger.error(f"❌ Task {task_id} failed: {e}")
                self.failed_tasks.append({
                    'task_id': task_id,
                    'error': str(e)
                })

                # 根据配置决定是否继续
                if not self.config.get('continue_on_error', False):
                    logger.error("Stopping execution due to error (continue_on_error=False)")
                    break

        self.end_time = time.time()

        # 生成执行报告
        report = self._generate_execution_report()

        # 保存执行报告
        self._save_execution_report(report)

        logger.info("\n" + "="*60)
        logger.info("PLAN EXECUTION COMPLETED")
        logger.info("="*60)
        logger.info(f"Total tasks: {len(self.tasks)}")
        logger.info(f"Successful: {len(self.results)}")
        logger.info(f"Failed: {len(self.failed_tasks)}")
        logger.info(f"Total time: {report['total_execution_time']:.2f}s")
        logger.info("="*60 + "\n")

        return report

    def _save_task_result(self, result: Dict, output_dir: str):
        """
        保存单个任务的结果

        Args:
            result: 任务结果字典
            output_dir: 输出目录
        """
        # 创建输出目录
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        task_id = result['task_id']

        # 保存完整结果
        result_file = output_path / f"{task_id}_timestamps.json"
        with open(result_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)

        logger.info(f"  → Saved: {result_file}")

        # 保存静音片段（单独文件，便于快速访问）
        silence_file = output_path / f"{task_id}_silence_gaps.json"
        silence_data = {
            'task_id': task_id,
            'video_path': result['video_info']['path'],
            'total_gaps': len(result['silence_gaps']),
            'high_confidence_gaps': sum(
                1 for gap in result['silence_gaps'] if gap['confidence'] >= 0.9
            ),
            'gaps': result['silence_gaps']
        }
        with open(silence_file, 'w', encoding='utf-8') as f:
            json.dump(silence_data, f, indent=2, ensure_ascii=False)

        logger.info(f"  → Saved: {silence_file}")

        # 保存场景切换（如果有）
        if result['scene_changes']:
            scene_file = output_path / f"{task_id}_scene_changes.json"
            scene_data = {
                'task_id': task_id,
                'video_path': result['video_info']['path'],
                'total_scenes': len(result['scene_changes']),
                'scenes': result['scene_changes']
            }
            with open(scene_file, 'w', encoding='utf-8') as f:
                json.dump(scene_data, f, indent=2, ensure_ascii=False)

            logger.info(f"  → Saved: {scene_file}")

    def _generate_execution_report(self) -> Dict:
        """
        生成执行报告

        Returns:
            报告字典
        """
        total_execution_time = self.end_time - self.start_time if self.end_time else 0

        # 聚合统计
        total_silence_gaps = sum(r['statistics']['total_silence_gaps'] for r in self.results)
        total_high_confidence = sum(r['statistics']['high_confidence_cuts'] for r in self.results)
        total_scene_changes = sum(r['statistics']['scene_changes'] for r in self.results)

        report = {
            'execution_id': f"exec-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
            'plan_id': self.plan_id,
            'execution_time': datetime.now().isoformat(),
            'total_tasks': len(self.tasks),
            'successful_tasks': len(self.results),
            'failed_tasks': len(self.failed_tasks),
            'total_execution_time': round(total_execution_time, 2),
            'aggregated_statistics': {
                'total_silence_gaps': total_silence_gaps,
                'total_high_confidence_cuts': total_high_confidence,
                'total_scene_changes': total_scene_changes
            },
            'task_results': [
                {
                    'task_id': r['task_id'],
                    'video_path': r['video_info']['path'],
                    'duration': r['video_info']['duration'],
                    'silence_gaps': r['statistics']['total_silence_gaps'],
                    'high_confidence_cuts': r['statistics']['high_confidence_cuts'],
                    'scene_changes': r['statistics']['scene_changes'],
                    'processing_time': r['statistics']['processing_time']
                }
                for r in self.results
            ],
            'failed_tasks': self.failed_tasks,
            'config': self.config
        }

        return report

    def _save_execution_report(self, report: Dict):
        """
        保存执行报告

        Args:
            report: 报告字典
        """
        # 保存到第一个任务的输出目录
        if self.tasks:
            output_dir = self.tasks[0].get('output_dir', f"output/{self.plan_id}")
        else:
            output_dir = f"output/{self.plan_id}"

        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        report_file = output_path / "execution_report.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)

        logger.info(f"\n📊 Execution report saved: {report_file}")


def execute_plan(plan_path: str) -> Dict:
    """
    便捷函数：执行计划

    Args:
        plan_path: JSON计划文件路径或计划字典

    Returns:
        执行报告字典
    """
    if isinstance(plan_path, dict):
        # 如果传入的是字典，先保存为临时文件
        import tempfile
        with tempfile.NamedTemporaryFile(
            mode='w',
            suffix='.json',
            delete=False,
            encoding='utf-8'
        ) as f:
            json.dump(plan_path, f, indent=2)
            temp_path = f.name

        executor = PlanExecutor(temp_path)
        report = executor.execute()

        # 清理临时文件
        os.unlink(temp_path)

        return report
    else:
        executor = PlanExecutor(plan_path)
        return executor.execute()


def main():
    """
    CLI入口函数
    """
    if len(sys.argv) < 2:
        print("Usage: python plan_executor.py <plan_json_path>")
        print("\nExamples:")
        print("  python plan_executor.py ../templates/podcast.json")
        print("  python plan_executor.py output/plans/my-plan.json")
        sys.exit(1)

    plan_path = sys.argv[1]

    try:
        report = execute_plan(plan_path)

        # 打印摘要
        print("\n" + "="*60)
        print("EXECUTION SUMMARY")
        print("="*60)
        print(f"Plan ID: {report['plan_id']}")
        print(f"Total Tasks: {report['total_tasks']}")
        print(f"Successful: {report['successful_tasks']}")
        print(f"Failed: {report['failed_tasks']}")
        print(f"Execution Time: {report['total_execution_time']:.2f}s")
        print(f"\nAggregated Statistics:")
        print(f"  Total Silence Gaps: {report['aggregated_statistics']['total_silence_gaps']}")
        print(f"  High Confidence Cuts: {report['aggregated_statistics']['total_high_confidence_cuts']}")
        print(f"  Scene Changes: {report['aggregated_statistics']['total_scene_changes']}")
        print("="*60 + "\n")

        sys.exit(0 if report['failed_tasks'] == 0 else 1)

    except Exception as e:
        logger.error(f"Execution failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
