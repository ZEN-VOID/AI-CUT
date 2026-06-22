# `libtv download` — 下载节点资源

下载具体画布中的节点资源到本地。`-n` 接受节点 id 或展示名，解析规则与 [`libtv node`](./node.md) 一致；图片、视频、音频单节点通常直存为文件，普通分组或多文件场景输出 ZIP，对齐画布批量下载命名。

## 子命令

无子命令，仅 flags。

用法骨架：`libtv download [flags]`

### 选项

| 选项 | 必填 | 说明 |
| --- | --- | --- |
| `-n, --node <node>` | 是 | 目标节点 id 或显示名。节点显示名不唯一时优先使用节点 id，避免下载覆盖或解析歧义。 |
| `-p, --project <uuid>` | 否 | 目标画布 **UUID**；省略时读当前目录 `.libtv/project.json` 的 `projectUuid`。这里必须是具体画布 UUID，不是 `projectSpaceId` / `folderId`。 |
| `-g, --group <node>` | 否 | 限定在普通分组子节点范围内解析 `-n`；批量下载该组时 `-n` 传分组节点 id。 |
| `-o, --out <dir>` | 否 | 输出目录，默认当前工作目录。目录不存在时先创建。 |
| `--without-ai-watermark` | 否 | 偏好不添加 AI 水印；会员且账号有效时图片 / 视频可走原链。 |
| `--vip` | 否 | 声明当前账号为会员，等价 `LIBTV_DOWNLOAD_IS_VIP=1`；影响社区水印策略。 |
| `--help` | 否 | 打印帮助。 |

### 输出

| 流 | 内容 |
| --- | --- |
| stdout | 成功时通常输出已保存文件的绝对路径；普通分组或多文件场景可能输出 ZIP 路径。 |
| stderr | 下载进度、权限、节点无资源或解析失败等诊断信息。 |

## 示例

```bash
# case 1: 下载当前目录绑定画布中的单个视频节点
libtv download -n "vid__6-2-1__b001__r00__v001" -o ./downloads

# case 2: 显式指定画布 UUID，并用节点 id 避免重名歧义
libtv download -p 11111111-2222-3333-4444-555555555555 \
  -n v-abc123 \
  -o ./downloads

# case 3: 会员账号偏好下载无 AI 水印版本
libtv download -p 11111111-2222-3333-4444-555555555555 \
  -n v-abc123 \
  -o ./downloads \
  --without-ai-watermark \
  --vip
```

## 批量下载提示

- 批量下载画布全部视频时，先用 `libtv node list -p <projectUuid>` 枚举 `type=video` 节点，再逐个传节点 id 给 `libtv download`。
- 若不同节点展示名相同，CLI 会按资源名落盘，可能覆盖同名文件；批量任务应记录 `node_id -> output_path`，并给重名产物追加节点 id 后缀。
- 下载受账号可见性限制；若画布报 `此项目仅团队版可见`，先切换有权限的账号或使用当前账号可访问的画布 UUID。
