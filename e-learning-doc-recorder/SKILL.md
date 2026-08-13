---
name: e-learning-doc-recorder
description: Maintain project documentation and evidence for the AI online training management system. Use when Codex implements or changes any feature, API, database table, AI prompt, test, deployment step, demo script, report export, or competition delivery artifact that should be recorded under docs/.
---

# E-Learning Doc Recorder

Use this skill whenever code, architecture, prompts, tests, or delivery materials change.

## Documentation Contract

Keep docs practical and current. Do not create decorative documents. Each document should help implementation, review, demonstration, or final submission.

## Update Matrix

- Requirement or scope change: update `docs/00-竞赛要求与需求拆解.md` and `docs/01-产品方案.md`.
- Architecture or module boundary change: update `docs/02-系统架构设计.md`.
- Entity/table change: update `docs/03-数据库设计.md`.
- API change: update `docs/04-接口设计.md`.
- Frontend page or workflow change: update `docs/05-前端页面设计.md`.
- AI API, prompt, response schema, fallback, or logging change: update `docs/06-AI能力设计.md` and `docs/10-AI工具使用记录.md`.
- Test or acceptance result: update `docs/07-测试方案.md`.
- Deployment, environment, account, or startup change: update `docs/08-部署说明.md`.
- Demo flow or seeded data change: update `docs/09-演示脚本.md`.
- Daily work summary: update `docs/daily/YYYY-MM-DD.md`.

## Per-Feature Record

For each meaningful feature, record:

- Feature name
- Business purpose
- Frontend files changed
- Backend files changed
- Database changes
- API endpoints
- AI prompts or model calls, if any
- Test cases run
- Known limitations
- Demo notes

## AI Usage Evidence

For AI-related work, capture:

- Task goal
- Prompt intent, not necessarily full sensitive prompt text
- Model/provider used
- Input summary
- Output summary
- Human review or edits
- Final files affected

## Completion Gate

Before marking a module complete, verify that corresponding docs exist and are not stale. If documentation is missing, update it before final response.
