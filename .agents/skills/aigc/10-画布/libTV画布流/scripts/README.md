# Scripts

本目录只承载机械辅助脚本，例如：

- 解析 `8-分组` fenced YAML。
- 投影本地 YAML 的 `图片N 主体名 UUID`。
- 生成提交计划结构时，仅整理主体行重排所需的机械映射：`图片N 主体名 {{Image N}} UUID`。
- 生成 LibTV CLI 命令计划。
- 校验远端 `imageList` 与本地 YAML 顺序。

脚本不得主创或改写分镜组正文，不得生成、批量插入、正则套句、映射投影或同义改写 LibTV prompt / 视频节点正文。prompt 主体必须由 LLM 逐组读取完整分镜组正文后裁决；脚本只允许辅助 YAML、顺序、diff、manifest、CLI 参数和校验。
