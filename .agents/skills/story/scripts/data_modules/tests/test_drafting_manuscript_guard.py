#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from pathlib import Path


def _load_module():
    scripts_dir = Path(__file__).resolve().parents[2]
    if str(scripts_dir) not in sys.path:
        sys.path.insert(0, str(scripts_dir))
    import drafting_manuscript_guard

    return drafting_manuscript_guard


def test_guard_blocks_short_summary_manuscript(tmp_path):
    module = _load_module()
    manuscript = tmp_path / "第1集.md"
    planning = tmp_path / "第1章.md"

    manuscript.write_text(
        "---\n"
        "episode_title: 港雨暂安\n"
        "rhythm_type: 势能式\n"
        "---\n\n"
        "# 第1集\n\n"
        "令狐冲和任盈盈在港口过日子，遇到恶霸收账，随后准备夜探王府。\n",
        encoding="utf-8",
    )
    planning.write_text("对下章的直接推动：闻得真鹤邀二人夜入首里王府回廊试听密语\n", encoding="utf-8")

    result = module.validate_manuscript(manuscript, planning_path=planning)

    assert result["status"] == "block"
    issue_codes = {item["code"] for item in result["issues"]}
    assert "body_too_short" in issue_codes


def test_guard_passes_chapter_complete_manuscript(tmp_path):
    module = _load_module()
    manuscript = tmp_path / "第1集.md"
    planning = tmp_path / "第1章.md"

    base_paragraphs = [
        "那霸港起了潮雾，令狐冲和任盈盈在海边木屋里醒来，各自忙着把日子过成真的样子，连窗边酒壶和晾衣绳都像在替他们守住这份偷来的安稳。",
        "两人去夜市前还在斗嘴，语气很轻，却都知道这份小日子得来不易，因此谁都不愿先把刀意带进清晨的海风里。",
        "夜市摊贩、海盐、鱼腥和孩子哭声一起把港口早晨推到眼前，也把琉球民间还没被彻底压垮的那点活气先立住了。",
        "久武平四郎的人带着黑印收账牌闯进来，把渔户按在地上逼债，推翻了鱼桶，又把整条石街的平和一下压成了屈辱。",
        "令狐冲先扶人不先杀人，任盈盈则先辨账牌与税线的关系，两人的动作一轻一稳，先把‘真像夫妻过日子’的假安稳扯进危局。",
        "真壁十兵卫压上来时，二人分别站住了护人与辨局的位置，前者挡住明刀，后者拎住暗线，使场面不是单纯械斗，而是制度恶压正面落地。",
        "黑印牌上的印记让任盈盈意识到恶压不是散的，而是一条直通税关的线；她因此不再只想护住眼前一家，而开始意识到整座港口都被写进了账页里。",
        "一场不长的交手过后，港口平静已经失守，夜市里的人都知道有人出了剑，可真正可怕的是那把剑已经被税线和官差一起记住了。",
        "闻得真鹤带着王府灯影来到街口，先看盐与血，再开口递话，她不是来讲公道，而是来告诉两人，真正的账不在夜市，而在回廊深处。",
        "闻得真鹤邀二人夜入首里王府回廊试听密语。",
    ]
    extension = (
        "这一段继续把人物动作、空间压力、情绪反应和下一拍危机往前推，让正文保持章节级而不是摘要级密度。"
        "同时补一层更细的身体感、环境细节与关系反应，确保这一段不是只交代梗概，而是真的在展开场面。"
        "再补一笔人物之间的相互牵制与场面后果，使文本长度和章节承重都达到 guard 的默认门槛。"
    )
    body = "\n\n".join([f"{p}{extension}" for p in base_paragraphs])
    manuscript.write_text(
        "---\n"
        "episode_title: 港雨暂安\n"
        "rhythm_type: 势能式\n"
        "---\n\n"
        "# 第1集\n\n"
        + body
        + "\n",
        encoding="utf-8",
    )
    planning.write_text("对下章的直接推动：闻得真鹤邀二人夜入首里王府回廊试听密语\n", encoding="utf-8")

    result = module.validate_manuscript(manuscript, planning_path=planning)

    assert result["status"] == "pass"
    assert result["metrics"]["body_chars"] >= module.DEFAULT_MIN_BODY_CHARS
