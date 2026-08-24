# 语雀开放 API 对接文档（yuque-push）

> 适用范围：向语雀知识库自动创建/更新文档并挂载到指定目录（如周报自动发布）。
> 本文档基于 2026-08 实测编写，记录全部接口明细、踩坑点与复用方式。
> 配套实现：同目录 `../scripts/push.py`（可直接复用）。

---

## 1. 基础信息

| 项目 | 值 |
|---|---|
| API 基址 | `https://www.yuque.com/api/v2` |
| 认证 | 请求头 `X-Auth-Token: <个人Token>` |
| 必带请求头 | `User-Agent`（不带会被拒绝） |
| Token 获取 | 语雀 → 个人设置 → Token 生成 |
| 限流 | 官方口径：5000 次/小时、100 次/秒；实测高频写操作会触发更严的风控（见 §6.5） |

个人 Token 的权限范围 = 该账号名下的所有可见知识库（含个人与团队）。

## 2. 核心流程（5 步）

```
① 定位用户 → ② 定位知识库 → ③ 定位目标目录 → ④ 创建/更新文档 → ⑤ 挂载到目录
GET /user      GET /users/{login}/repos   GET /repos/{ns}/toc    POST|PUT /repos/{ns}/docs   PUT /repos/{ns}/toc
```

**关键结论：创建文档接口不支持指定目录，必须先创建、再通过 TOC 接口挂载。**

## 3. 接口明细

### 3.1 定位用户

```
GET /user
```
响应 `data.login`（个人登录名）、`data.name`。

### 3.2 定位知识库

```
GET /users/{login}/repos
```
按 `name` 字段（如「工作相关」）筛选，取 `namespace`（格式 `{login}/{repo-slug}`）和 `id`（数字，后续前缀用）。

### 3.3 获取目录树（TOC）

```
GET /repos/{namespace}/toc
```
响应 `data` 为目录树节点数组，关键字段：

| 字段 | 说明 |
|---|---|
| `uuid` | 节点唯一 ID，**格式 `{repoId}:{节点id}`（带前缀）** |
| `type` | `TITLE` = 目录节点；`DOC` = 文档节点；`LINK` = 链接 |
| `title` | 节点标题 |
| `parent_uuid` | 父节点 uuid（根层级的节点该字段为空） |
| `child_uuid` / `sibling_uuid` | 树的链结构（child 指向第一个子节点，sibling 指向同级下一个节点） |
| `doc_id` | DOC 节点对应的文档 id |

> 注意：`GET /repos/{namespace}/docs`（文档列表接口）**不返回** `parent_uuid`，无法用于判断文档归属；验证挂载位置必须用 `/toc`。

### 3.4 创建 / 更新文档（upsert）

```
POST /repos/{namespace}/docs                      # 创建
PUT  /repos/{namespace}/docs/{slug}               # 更新
```

请求体：

```json
{
  "title": "工作周报（2026-08-10 ~ 2026-08-14）",
  "slug": "weekly-report-2026-08-14",
  "format": "markdown",
  "body": "# 文档内容（markdown 原文）"
}
```

| 参数 | 说明 |
|---|---|
| `title` | 文档标题（必填） |
| `slug` | 文档路径标识。**仅允许 `[\w\-\.]{2,190}`（字母数字下划线连字符点），中文报 422** |
| `format` | `markdown` / `lake` / `html` |
| `body` | 文档正文 |

**Upsert 标准做法**：先 `PUT /docs/{slug}`，404 则 `POST` 创建（创建时**必须带 slug**，否则语雀生成随机 slug，下次无法命中更新，会造成重复文档）。

### 3.5 挂载文档到目录

```
PUT /repos/{namespace}/toc
```

```json
{
  "action": "appendNode",
  "action_mode": "child",
  "target_uuid": "29025828:1BWbIuNuYWbxn9bQ",
  "type": "DOC",
  "doc_ids": [281607142]
}
```

| 参数 | 说明 |
|---|---|
| `action` | `appendNode`（追加）等 |
| `action_mode` | `child`（作为子节点） |
| `target_uuid` | 目标目录节点 uuid，**必须带 repoId 前缀**（见 §6.3） |
| `type` + `doc_ids` | 挂载文档时固定为 `"DOC"` + 文档 id 数组 |

响应 `data` 为更新后的**完整目录树**（可直接用于验证挂载结果）。

### 3.6 删除文档（清理用）

```
DELETE /repos/{namespace}/docs/{slug}
```

## 4. 本环境已确认的对接值

| 项目 | 值 |
|---|---|
| 用户 login / name | `yuqiusuo` / 余求索 |
| 知识库 | 「工作相关」 `namespace=yuqiusuo/wvcp3q`，`id=29025828` |
| 目标目录 | 「1.交控信息 → 3.工作记录 → 1.周报」 |
| 目录节点 uuid | `29025828:1BWbIuNuYWbxn9bQ`（**带前缀**） |
| 周报 slug 规则 | 文件名日期 → `weekly-report-YYYY-MM-DD`（如 `weekly-report-2026-08-14`） |
| 已发布示例 | https://www.yuque.com/yuqiusuo/wvcp3q/weekly-report-2026-08-14 |

## 5. 复用方式

直接使用配套脚本 `scripts/push.py`（零 API 开发）：

```bash
# 凭证在 skill 目录 .env：YUQUE_TOKEN / YUQUE_NAMESPACE / YUQUE_PARENT_UUID
python scripts/push.py                      # 自动找 workspace 下最新 周报-*.md
python scripts/push.py --file <文档路径>     # 指定文件
```

脚本行为：PUT 命中则更新、404 则创建（固定 slug）→ 创建后自动挂载到目标目录 → 输出发布 URL。幂等，可重复执行。

更换目标目录：改 `.env` 的 `YUQUE_PARENT_UUID`（用 §3.3 的 TOC 接口查 uuid）。

## 6. 踩坑记录（对接必读）

### 6.1 中文 slug 被拒
`PUT/POST /docs` 的 slug 只接受 `[\w\-\.]{2,190}`，中文/日期中文名会 422。→ 用英文 slug，标题保持中文。

### 6.2 创建接口不认 parentUuid
`POST /docs` 请求体里传 `parentUuid`（无论带不带前缀）**都会被静默忽略**，文档落在根层级。→ 必须先创建，再 `PUT /toc` 挂载。

### 6.3 target_uuid 必须带 repoId 前缀
`PUT /toc` 的 `target_uuid` 传无前缀 uuid（如 `1BWbIuNuYWbxn9bQ`）时接口返回 200 但**静默挂到根层级**，不报错。→ 必须传完整 `29025828:1BWbIuNuYWbxn9bQ`。

### 6.4 删除 slug 导致无法幂等
创建时若删除 `slug` 字段，语雀生成随机 slug，后续 `PUT /docs/{固定slug}` 永远 404 → 每周重复创建。→ 创建时保留固定 slug。

### 6.5 429 风控（本次踩过的大坑）
- 短时间高频创建/删除文档（约十几分钟内 15+ 次写操作）触发 Token 级风控：**所有请求（含 GET）返回 429**，持续数小时。
- 表现与普通限流不同：`GET /user` 也 429。
- 规避：生产脚本每次运行 ≤5 次调用；不在脚本里做循环创建/删除；调试用一次性测试文档并及时删除。
- 恢复：停止调用数小时后自动解除，无需联系客服。

### 6.6 挂载验证要看 TOC，别看文档详情
文档详情接口（`GET /docs/{slug}`）**不返回** `parent_uuid`；`GET /docs` 列表的 `parent_uuid` 恒为空。→ 用 `GET /toc` 或 `PUT /toc` 的响应树验证归属。

### 6.7 PUT /toc 响应序列化差异
`PUT /toc` 响应树中新挂载节点的 `uuid` 不带 repoId 前缀（与 `GET /toc` 不同），且 `parent_uuid` 为 null；判断挂载结果应沿 `TITLE.child_uuid → sibling_uuid` 链遍历（见 push.py 验证逻辑），不要依赖节点自身的 parent_uuid 字段。

## 7. 自动化接入（周报场景）

每周五 16:00 定时任务「发布简报」已配置：
1. 按 `周报模板.md` 生成周报 → 保存 `周报-YYYY-MM-DD.md`
2. 调用 `push.py --file <周报路径>` 发布到语雀「1.周报」目录
3. 汇报本地文件路径 + 语雀发布 URL

每周仅 1 次调用（创建或更新 + 挂载），不会触发风控。
