---
name: yuque-push
description: "将本地 markdown 文档发布到语雀（Yuque）知识库指定目录。当用户要求把周报、总结、文档上传/同步到语雀，或要求定时发布到语雀时使用。支持同名文档覆盖更新（upsert），自动保留历史版本。默认目标：知识库「工作相关」→ 1.交控信息 → 3.工作记录 → 1.周报。"
---

# Yuque Push — 发布文档到语雀

将本地 markdown 文件发布/更新到语雀知识库，实现"生成即发布"。由 ZCode 定时任务（如周五 16:00「发布简报」）调用，也可手动运行。

## 工作原理

- 认证：`X-Auth-Token` 请求头（凭证存于本技能目录 `.env`，勿外传）
- 上传：文档存在则 `PUT /api/v2/repos/{namespace}/docs/{slug}` 更新；不存在则 `POST` 创建，随后 `PUT /repos/{namespace}/toc`（`appendNode` + `doc_ids`）挂到目标目录（创建接口本身不支持 parentUuid）
- slug 取自文件名中的日期（如 `周报-2026-08-14` → `weekly-report-2026-08-14`），每周一篇、保留历史、可重复更新
- 知识库 `namespace=yuqiusuo/wvcp3q`，目标目录 `1. 周报` 的节点 uuid（**必须带 repoId 前缀**）= `29025828:1BWbIuNuYWbxn9bQ`（工作相关 → 1.交控信息 → 3.工作记录 → 1.周报）
- 完整对接细节、接口明细与踩坑记录见 `docs/语雀API对接文档.md`（新环境对接前必读）

## 使用方式

脚本路径（相对本技能目录）：`scripts/push.py`

```bash
# 发布最新周报（自动找 ~/.zcode/workspace/default 下最新的 周报-*.md）
python scripts/push.py

# 指定文件
python scripts/push.py --file C:/path/to/周报-2026-08-14.md
```

输出文档 URL 即为发布成功；返回 4xx/5xx 时脚本打印错误详情并退出码非 0。

## 注意事项

- 凭证：`.env` 中的 `YUQUE_TOKEN`（语雀个人 Token）、`YUQUE_NAMESPACE`、`YUQUE_PARENT_UUID`（TOC 节点 uuid，**必须带 repoId 前缀**）。更换目标目录时用 `GET /api/v2/repos/{namespace}/toc` 查目录树 uuid。
- 网络环境要求能访问 `https://www.yuque.com`。
- 幂等：同一文件重复执行只更新不重复创建。
