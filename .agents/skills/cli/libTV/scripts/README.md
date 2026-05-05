# LibTV Scripts

These scripts are imported from `libtv-labs/libtv-skills` and kept as the mechanical CLI bridge for LibTV Agent-IM.

## Commands

```bash
python3 scripts/create_session.py "【给龙虾的工作流管理要求】把全部工作流和结果都放在画布上。\n\n【创作请求原文】用户原始请求"
python3 scripts/create_session.py "追加消息" --session-id SESSION_ID
python3 scripts/create_session.py "把全部工作流和结果都放在画布上。" --session-id SESSION_ID
python3 scripts/query_session.py SESSION_ID --after-seq 0
python3 scripts/upload_file.py /path/to/reference.png
python3 scripts/download_results.py SESSION_ID --output-dir ./output --prefix libtv
python3 scripts/change_project.py
```

For reference handoff, run `upload_file.py` first and copy only the returned OSS URL into the session message. Do not submit local filesystem paths to `create_session.py` as reference material.

For video handoff, include a separate default spec unless the user overrides it: sound/audio enabled, 15 seconds, 16:9, 720P, and do not shorten to 10 seconds.

Generation/editing routes should not call `query_session.py` or `download_results.py` automatically after `create_session.py`. Keep those commands for explicit user-requested status checks and downloads.

`LIBTV_ACCESS_KEY` is required for live calls.
