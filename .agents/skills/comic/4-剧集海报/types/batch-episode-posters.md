# Type Package: batch-episode-posters

## Purpose

批量为多集生成海报 JSON 时使用。它只定义批量节奏，不改变单集 JSON 的 canonical status。

## Fixed Context

- 一集一个 JSON，一集一个 review verdict。
- 输出命名使用 `第N集-剧集海报.json`。
- 可额外生成索引，但索引不得替代单集 JSON。
- 每集都必须独立记录上游 artifact 和高光点筛选，不得复用上一集的主体或标题。

## Review Focus

- 是否误把多集海报揉成一个大 JSON？
- 是否有某集缺少真实上游读取？
- 是否出现标题模板批量套壳、剧情事实不变的问题？
