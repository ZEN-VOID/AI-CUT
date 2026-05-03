# LibTV Heuristics

## Operational Heuristics

- Keep the local agent as a transport layer for LibTV creative tasks.
- Use local semantic names only for downloaded file prefixes.
- Prefer reporting `pass_with_todo` over hiding long-running generation when polling times out.
- Keep upstream scripts easy to replace; custom behavior belongs in Skill 2.0 contracts unless it is a mechanical CLI fix.

## Failure Patterns

| pattern | prevention |
| --- | --- |
| Local prompt engineering degrades backend planning | Pass through original request |
| Missing credential discovered after partial setup | Check `LIBTV_ACCESS_KEY` first |
| User loses remote result because no download ran | Always run or explicitly skip `download_results.py` |
| Existing session accidentally forked | Respect provided `sessionId` for append/query/download |
