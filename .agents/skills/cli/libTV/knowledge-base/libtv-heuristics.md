# LibTV Heuristics

## Operational Heuristics

- Keep the local agent as a transport layer for LibTV creative tasks.
- Use local semantic names only for downloaded file prefixes.
- Prefer reporting the project canvas URL and preserved session metadata over waiting on long-running generation.
- Keep upstream scripts easy to replace; custom behavior belongs in Skill 2.0 contracts unless it is a mechanical CLI fix.
- Video requests need an explicit first operational defaults block because the provider may otherwise return silent or 10-second output.

## Failure Patterns

| pattern | prevention |
| --- | --- |
| Local prompt engineering degrades backend planning | Pass through original request |
| Missing credential discovered after partial setup | Check `LIBTV_ACCESS_KEY` first |
| User expects a local file but only checked the canvas | Explain that local download is passive and run `download_results.py` only on request |
| Existing session accidentally forked | Respect provided `sessionId` for append/query/download |
| Video output is silent or 10 seconds despite project defaults | Submit or rerun with a first hard-parameter block: `15-second video, not 10 seconds`, set canvas/video duration to 15 seconds before generation, sound/audio enabled; report provider mismatch if ignored |
