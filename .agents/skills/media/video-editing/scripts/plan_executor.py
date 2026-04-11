#!/usr/bin/env python3
"""
Video Editing - Plan Executor
==============================

Batch execution engine for processing multiple video editing tasks
from JSON execution plans.

Features:
- Batch video editing from JSON plans
- Progress tracking and reporting
- Error handling and recovery
- Comprehensive execution reports
- Integration with timestamp-extraction outputs

Usage:
    python plan_executor.py <plan_json_path>

Example:
    python plan_executor.py ../templates/podcast-edit.json
    python plan_executor.py output/plans/my-editing-plan.json

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

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent))

from video_editor import VideoEditor

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('video_editing.log')
    ]
)
logger = logging.getLogger(__name__)


class PlanExecutor:
    """
    Batch video editing execution engine

    Features:
    - Read JSON execution plans
    - Batch process multiple video editing tasks
    - Progress tracking
    - Error handling and recovery
    - Result aggregation and reporting
    """

    def __init__(self, plan_path: str):
        """
        Initialize executor

        Args:
            plan_path: Path to JSON plan file
        """
        self.plan_path = plan_path
        self.plan = self._load_plan(plan_path)
        self.plan_id = self.plan.get('plan_id', self._generate_plan_id())
        self.config = self.plan.get('config', {})
        self.tasks = self.plan.get('tasks', [])

        # Create video editor
        self.editor = VideoEditor(self.config)

        # Execution state
        self.results = []
        self.failed_tasks = []
        self.start_time = None
        self.end_time = None

        logger.info(f"PlanExecutor initialized with plan: {self.plan_id}")
        logger.info(f"Total tasks: {len(self.tasks)}")

    def _load_plan(self, plan_path: str) -> Dict:
        """
        Load JSON plan file

        Args:
            plan_path: Path to JSON file

        Returns:
            Plan dictionary
        """
        logger.info(f"Loading plan from: {plan_path}")

        if not os.path.exists(plan_path):
            raise FileNotFoundError(f"Plan file not found: {plan_path}")

        with open(plan_path, 'r', encoding='utf-8') as f:
            plan = json.load(f)

        # Validate required fields
        if 'tasks' not in plan or not plan['tasks']:
            raise ValueError("Plan must contain at least one task")

        logger.info(f"Plan loaded successfully: {len(plan['tasks'])} tasks")
        return plan

    def _generate_plan_id(self) -> str:
        """
        Generate unique plan ID

        Returns:
            Plan ID string
        """
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        return f"plan-{timestamp}"

    def execute(self) -> Dict:
        """
        Execute all tasks in the plan

        Returns:
            Execution report dictionary
        """
        logger.info("=" * 60)
        logger.info(f"STARTING PLAN EXECUTION: {self.plan_id}")
        logger.info("=" * 60)

        self.start_time = time.time()

        # Execute each task
        for i, task in enumerate(self.tasks, 1):
            task_id = task.get('task_id', f"task-{i:03d}")

            logger.info(f"\n[{i}/{len(self.tasks)}] Processing: {task_id}")

            try:
                # Pre-process task (handle special types)
                processed_task = self._preprocess_task(task)

                # Execute task
                task_start = time.time()
                result = self.editor.process_task(processed_task)
                task_end = time.time()

                # Add processing time
                result['processing_time'] = round(task_end - task_start, 2)

                # Save result
                output_dir = task.get('output_dir', f"output/{self.plan_id}")
                self._save_task_result(result, output_dir)

                self.results.append(result)

                logger.info(f"✅ Task {task_id} completed in {result['processing_time']}s")

            except Exception as e:
                logger.error(f"❌ Task {task_id} failed: {e}")
                self.failed_tasks.append({
                    'task_id': task_id,
                    'error': str(e)
                })

                # Check if we should continue on error
                if not self.config.get('continue_on_error', False):
                    logger.error("Stopping execution due to error (continue_on_error=False)")
                    break

        self.end_time = time.time()

        # Generate execution report
        report = self._generate_execution_report()

        # Save execution report
        self._save_execution_report(report)

        logger.info("\n" + "=" * 60)
        logger.info("PLAN EXECUTION COMPLETED")
        logger.info("=" * 60)
        logger.info(f"Total tasks: {len(self.tasks)}")
        logger.info(f"Successful: {len(self.results)}")
        logger.info(f"Failed: {len(self.failed_tasks)}")
        logger.info(f"Total time: {report['total_execution_time']:.2f}s")
        logger.info("=" * 60 + "\n")

        return report

    def _preprocess_task(self, task: Dict) -> Dict:
        """
        Preprocess task based on task type

        Some task types require special handling:
        - podcast_edit: Add intro/outro, remove silence
        - interview_edit: Multi-cam switching
        - montage: Music-synced editing

        Args:
            task: Original task dictionary

        Returns:
            Processed task dictionary
        """
        task_type = task.get('type', 'cut')

        if task_type == 'podcast_edit':
            # Handle podcast editing workflow
            return self._preprocess_podcast_edit(task)

        elif task_type == 'interview_edit':
            # Handle interview editing workflow
            return self._preprocess_interview_edit(task)

        elif task_type == 'montage':
            # Handle montage editing workflow
            return self._preprocess_montage(task)

        else:
            # Return task as-is
            return task

    def _preprocess_podcast_edit(self, task: Dict) -> Dict:
        """
        Preprocess podcast editing task

        Workflow:
        1. Add intro (if provided)
        2. Remove silence from main content
        3. Add outro (if provided)
        4. Mix background music with ducking

        Args:
            task: Podcast edit task

        Returns:
            Processed task for remove_silence operation
        """
        logger.info("Preprocessing podcast_edit task...")

        # For now, just convert to remove_silence task
        # TODO: Implement full podcast workflow (intro/outro/music)

        processed_task = {
            'task_id': task['task_id'],
            'type': 'remove_silence',
            'input_video': task['input_video'],
            'timestamp_file': task.get('timestamp_file'),
            'output_path': task.get('output_path'),
            'editing': task.get('editing', {})
        }

        return processed_task

    def _preprocess_interview_edit(self, task: Dict) -> Dict:
        """
        Preprocess interview editing task

        Workflow:
        1. Scene detection-based cutting
        2. Multi-cam switching (if enabled)
        3. Text overlays (lower thirds)

        Args:
            task: Interview edit task

        Returns:
            Processed task
        """
        logger.info("Preprocessing interview_edit task...")

        # For now, convert to basic cut task
        # TODO: Implement multi-cam and text overlay support

        processed_task = {
            'task_id': task['task_id'],
            'type': 'remove_silence',
            'input_video': task['input_video'],
            'timestamp_file': task.get('timestamp_file'),
            'output_path': task.get('output_path'),
            'editing': task.get('editing', {})
        }

        return processed_task

    def _preprocess_montage(self, task: Dict) -> Dict:
        """
        Preprocess montage editing task

        Workflow:
        1. Sync clips to music beats
        2. Add transitions
        3. Apply color grading

        Args:
            task: Montage task

        Returns:
            Processed task
        """
        logger.info("Preprocessing montage task...")

        # For now, convert to basic cut task
        # TODO: Implement music sync and effects

        processed_task = {
            'task_id': task['task_id'],
            'type': 'cut',
            'input_video': task['clips'][0],  # Use first clip for now
            'output_path': task.get('output_path'),
            'cuts': []  # TODO: Generate cuts based on music beats
        }

        return processed_task

    def _save_task_result(self, result: Dict, output_dir: str):
        """
        Save task result to JSON file

        Args:
            result: Task result dictionary
            output_dir: Output directory
        """
        # Create output directory
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        task_id = result['task_id']

        # Save complete result
        result_file = output_path / f"{task_id}_result.json"
        with open(result_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)

        logger.info(f"  → Saved result: {result_file}")

    def _generate_execution_report(self) -> Dict:
        """
        Generate execution report

        Returns:
            Report dictionary
        """
        total_execution_time = self.end_time - self.start_time if self.end_time else 0

        # Aggregate statistics
        total_input_duration = sum(
            r.get('original_duration', 0) for r in self.results
        )
        total_output_duration = sum(
            r.get('final_duration', 0) for r in self.results
        )
        total_time_saved = sum(
            r.get('time_saved', 0) for r in self.results
        )
        total_processing_time = sum(
            r.get('processing_time', 0) for r in self.results
        )

        # Calculate output file sizes
        total_output_size = 0
        for r in self.results:
            output_path = r.get('output_path')
            if output_path and os.path.exists(output_path):
                total_output_size += os.path.getsize(output_path) / (1024 * 1024)  # MB

        report = {
            'execution_id': f"exec-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
            'plan_id': self.plan_id,
            'execution_time': datetime.now().isoformat(),
            'total_tasks': len(self.tasks),
            'successful_tasks': len(self.results),
            'failed_tasks': len(self.failed_tasks),
            'total_execution_time': round(total_execution_time, 2),
            'aggregated_statistics': {
                'total_input_duration': round(total_input_duration, 2),
                'total_output_duration': round(total_output_duration, 2),
                'total_time_saved': round(total_time_saved, 2),
                'compression_ratio': round(total_output_duration / total_input_duration, 3) if total_input_duration > 0 else 0,
                'total_output_size_mb': round(total_output_size, 2),
                'total_processing_time': round(total_processing_time, 2),
                'average_encoding_speed': round(total_input_duration / total_processing_time, 1) if total_processing_time > 0 else 0
            },
            'task_results': [
                {
                    'task_id': r['task_id'],
                    'task_type': r.get('task_type', 'unknown'),
                    'status': r.get('status', 'unknown'),
                    'input_path': r.get('input_path', ''),
                    'output_path': r.get('output_path', ''),
                    'original_duration': r.get('original_duration', 0),
                    'final_duration': r.get('final_duration', 0),
                    'time_saved': r.get('time_saved', 0),
                    'processing_time': r.get('processing_time', 0)
                }
                for r in self.results
            ],
            'failed_tasks': self.failed_tasks,
            'config': self.config
        }

        return report

    def _save_execution_report(self, report: Dict):
        """
        Save execution report

        Args:
            report: Report dictionary
        """
        # Save to first task's output directory
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
    Convenience function: Execute plan

    Args:
        plan_path: JSON plan file path or plan dictionary

    Returns:
        Execution report dictionary
    """
    if isinstance(plan_path, dict):
        # If passed a dictionary, save to temp file
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

        # Cleanup temp file
        os.unlink(temp_path)

        return report
    else:
        executor = PlanExecutor(plan_path)
        return executor.execute()


def main():
    """
    CLI entry function
    """
    if len(sys.argv) < 2:
        print("Usage: python plan_executor.py <plan_json_path>")
        print("\nExamples:")
        print("  python plan_executor.py ../templates/podcast-edit.json")
        print("  python plan_executor.py output/plans/my-editing-plan.json")
        sys.exit(1)

    plan_path = sys.argv[1]

    try:
        report = execute_plan(plan_path)

        # Print summary
        print("\n" + "=" * 60)
        print("EXECUTION SUMMARY")
        print("=" * 60)
        print(f"Plan ID: {report['plan_id']}")
        print(f"Total Tasks: {report['total_tasks']}")
        print(f"Successful: {report['successful_tasks']}")
        print(f"Failed: {report['failed_tasks']}")
        print(f"Execution Time: {report['total_execution_time']:.2f}s")
        print(f"\nAggregated Statistics:")
        print(f"  Total Input Duration: {report['aggregated_statistics']['total_input_duration']:.1f}s")
        print(f"  Total Output Duration: {report['aggregated_statistics']['total_output_duration']:.1f}s")
        print(f"  Time Saved: {report['aggregated_statistics']['total_time_saved']:.1f}s")
        print(f"  Output Size: {report['aggregated_statistics']['total_output_size_mb']:.1f}MB")
        print(f"  Average Encoding Speed: {report['aggregated_statistics']['average_encoding_speed']:.1f}x")
        print("=" * 60 + "\n")

        sys.exit(0 if report['failed_tasks'] == 0 else 1)

    except Exception as e:
        logger.error(f"Execution failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
