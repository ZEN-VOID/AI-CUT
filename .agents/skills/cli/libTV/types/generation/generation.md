# Generation Type Package

Use for new LibTV image/video creation from user text.

## Fixed Context

- Preserve the user's original creative request.
- Do not locally expand, translate, embellish, or split the prompt.
- Use `create_session.py` for a new request or `create_session.py --session-id` only when the user explicitly wants to append to an existing session.
- Download generated images/videos after result URLs appear.

## Required Evidence

- `sessionId`
- `projectUuid` when returned
- final `projectUrl`
- downloaded file paths or timeout status
