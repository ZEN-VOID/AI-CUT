# LibTV Output Template

## Output Contract Alignment

| Output Contract field | Template location |
| --- | --- |
| Required output | `Result` |
| Output format | `Command Summary` and `Files` |
| Output path | `Files` |
| Naming convention | `Files` |
| Canvas notice status | `Canvas` |
| Video defaults | `Video Defaults` |
| Passive query/download status | `Command Summary` |
| Completion gate | `Review Verdict` |

## Result

- Mode:
- Session ID:
- Project UUID:
- Project URL:
- Status:

## Files

| path | type | note |
| --- | --- | --- |
|  | output_directory | preserved for optional later download |

## Canvas

- Start notice:
- Project URL:

## Video Defaults

- applies_to_video:
- audio_enabled: true
- duration_seconds: 15
- duration_override:
- provider_mismatch:

## Command Summary

- Upload:
- Session:
- Query:
  - requested_by_user:
  - status:
- Canvas notice:
- Download:
  - requested_by_user:
  - output_directory:

## Review Verdict

- Verdict:
- Residual risk:
