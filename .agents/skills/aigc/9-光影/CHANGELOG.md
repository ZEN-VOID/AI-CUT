# Changelog: aigc 9-光影

## 2026-06-10

- 接入 `../_shared/upstream-context-application-contract.md`，要求光影注入证明 `8-摄影` 分镜/运镜与三类 `3-美学` 协议如何投影为光源、受光、阴影、色温、材质、空气介质和动态光。
- 新增 `FAIL-LIGHT-UPSTREAM-CONTEXT`、`GATE-LIGHT-09-UPSTREAM-CONTEXT` 和报告 `Upstream Context Application Map`。
- 验证通过：`python3 scripts/skill_context_audit.py --root .agents/skills/aigc --strict`；`python3 scripts/aigc_skill_audit.py --strict`。

## 2026-06-04

- 新建 `9-光影` Skill 2.0 runtime-spine 包。
- 明确默认消费 `8-摄影` 输出物，用户指定 source 优先。
- 明确必须结合 `3-美学` 的画面基调、场景风格和摄影风格，提取参照大师及作品的光影原则。
- 建立逐分镜内联光影美学注入格式、节点、gate、references、入口元数据和测试 prompts。
- 新增 `knowledge-base/cinematic-lighting-top10.md`，基于网络资料整理电影光影表现技巧 TOP10，并在主入口 Module Loading / Trigger Matrix 中声明引用与触发。
- 新增 `knowledge-base/aigc-video-lighting-vocabulary.md`，基于 Runway、Luma、Sora、Kling 等视频生成提示指南整理 AIGC 可实现的高质量光影表现词库，并绑定 `aigc_video_lighting_vocab` 触发。
- 将 `Seedance 2.0` 设为未指定其他下游工具时的默认最优工具标准；主入口新增 `seedance_2_0_tool_standard` 触发、`GATE-LIGHT-09-SEEDANCE2` gate、`FAIL-LIGHT-SEEDANCE2-MISMATCH` 返工码，并同步词库、经验层、README 和测试 prompt。
