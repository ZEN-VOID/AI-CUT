# Subject Registry Contract

本文件定义 `3-主体` 前置后使用的主体注册表合同。它不是第二创作稿，而是角色、场景、道具在后续 `4-编剧` 到 `10-画布` 中保持命名一致的身份真源。

## Ownership

- owner stage: `3-主体`
- canonical human-readable file: `projects/aigc/<项目名>/3-主体/主体注册表.md`
- canonical machine-readable file: `projects/aigc/<项目名>/3-主体/subject-registry.yaml`
- downstream read mode: read-only

`8-分组` 理论上不新增主体信息。分组稿的 YAML 只能引用本注册表中已登记的 `id` 与 `canonical_name`，不得临时创造新角色、新场景或新道具名称。

## Inputs

建立注册表时默认读取：

- `projects/aigc/<项目名>/1-分集/` 中涉及本项目或目标分集的全部故事源内容。
- `projects/aigc/<项目名>/2-美学/类型风格.md`。
- `projects/aigc/<项目名>/2-美学/画面基调/全局风格协议.md`。
- `projects/aigc/<项目名>/2-美学/{角色风格,场景风格,道具风格}/` 中与本轮项目或分集相关的风格协议。
- 项目根 `MEMORY.md` 与相关 `CONTEXT/`。

后置已有 `8-分组` 稿时，可作为 reconciliation 证据读取，但不得替代上述初始来源。

## YAML Shape

```yaml
registry_version: subject-registry/v1
project: "<项目名>"
source_scope:
  episodes: ["第1集"]
  source_refs:
    - "1-分集/第1集.md"
  aesthetic_refs:
    - "2-美学/类型风格.md"
subjects:
  characters:
    - id: CHR-001
      canonical_name: "角色标准名"
      aliases: []
      first_appearance: "第1集"
      source_anchors:
        - "1-分集/第1集.md#..."
      style_refs:
        - "2-美学/角色风格/角色风格协议.md"
      status: canonical
  scenes:
    - id: SCN-001
      canonical_name: "场景标准名"
      aliases: []
      first_appearance: "第1集"
      source_anchors:
        - "1-分集/第1集.md#..."
      style_refs:
        - "2-美学/场景风格/场景风格协议.md"
      status: canonical
  props:
    - id: PRP-001
      canonical_name: "道具标准名"
      aliases: []
      first_appearance: "第1集"
      source_anchors:
        - "1-分集/第1集.md#..."
      style_refs:
        - "2-美学/道具风格/道具风格协议.md"
      status: canonical
```

## ID Rules

- 角色使用 `CHR-###`。
- 场景使用 `SCN-###`。
- 道具使用 `PRP-###`。
- `canonical_name` 必须短、稳定、可用于后续 YAML、图片参照和视频节点。
- `aliases` 只记录故事源中的称呼差异或后续历史产物中的旧称，不作为 downstream 首选输出名。

## Alignment Rules

| condition | verdict | action |
| --- | --- | --- |
| downstream entry uses exact `id` and matching `canonical_name` | pass | 保持 |
| downstream entry uses `canonical_name` only | pass with normalization | 可补 `id` |
| downstream entry uses alias listed in registry | candidate | 归一为 canonical name 并记录 normalization |
| downstream entry not found in registry | fail | `FAIL-SUBJECT-REGISTRY-UNREGISTERED`，回到 `3-主体` 补证或确认不是主体 |
| downstream entry invents a new subject from wording drift | fail | 删除或回写 `3-主体` reconciliation，不得在 `8-分组` 内定稿 |

## Downstream Contract

- `4-编剧` 到 `7-摄影` 可以使用注册表作为命名对齐上下文，但不得因为剧作措辞变化改写注册表。
- `8-分组` 组底 YAML 的 `角色`、`场景`、`道具` 必须引用已登记主体；空列表允许，未登记主体不允许。
- `9-图像` 与 `10-画布` 绑定主体参照时，以 `subject-registry.yaml` 的 `id` 和各域生成 manifest 为联合索引。
- 若后续阶段发现确有故事源主体遗漏，返工目标是 `3-主体` 的注册表和对应域清单，不是分组 YAML 临时补名。
