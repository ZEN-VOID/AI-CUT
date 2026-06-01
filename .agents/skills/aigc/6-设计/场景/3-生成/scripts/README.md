# Scripts Boundary

This directory is reserved for mechanical helpers only.

Allowed script responsibilities:

- Validate that required output files exist.
- Sanitize filenames.
- Count prompt characters.
- Check that images and same-name JSON records are paired.
- Copy or move selected generated image files into the project output directory when required by `$imagegen` persistence rules.

Forbidden script responsibilities:

- Generate scene design prose.
- Rewrite upstream `2-设计` documents.
- Invent or expand scene prompts.
- Choose new architecture, lighting, culture, material or narrative details.
- Call image models without an explicit execution decision made by the skill workflow.

No executable helper is required for the initial package.
