# LibTV Scripts

These scripts are imported from `libtv-labs/libtv-skills` and kept as the mechanical CLI bridge for LibTV Agent-IM.

## Commands

```bash
python3 scripts/create_session.py "用户原始请求"
python3 scripts/create_session.py "追加消息" --session-id SESSION_ID
python3 scripts/query_session.py SESSION_ID --after-seq 0
python3 scripts/upload_file.py /path/to/reference.png
python3 scripts/download_results.py SESSION_ID --output-dir ./output --prefix libtv
python3 scripts/change_project.py
```

`LIBTV_ACCESS_KEY` is required for live calls.
