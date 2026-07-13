# Scripts

This directory is reserved for `workflow` mechanical helpers. No helper script is currently required for the runtime spine to execute.

Allowed future script roles:

- scan default input paths and write a source manifest
- validate source preprocessing manifests, original/1.1x timestamp maps, and source-unit round maps
- validate slice quantity evidence such as candidate/output/excluded counts and manifest references
- validate combination-slice manifests for A/B1-B5/C coverage, random seed recording, and file references
- validate output directory shape
- check manifest references and file existence
- summarize render or QA logs
- perform dry-run route checks

Forbidden script roles:

- selecting the teaching arc
- deciding whether a slice opportunity is pedagogically worth outputting
- deciding which guide steps matter
- generating captions, titles, or explanations as creative truth
- rewriting source content without LLM review
- overriding `SKILL.md`, peer skill routing, or the output contract
