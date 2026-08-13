---
name: e-learning-competition-planner
description: Plan the AI online training management competition project. Use when Codex needs to scope features, prioritize MVP versus enhancements, map requirements to modules, create schedules, define deliverables, or align Vue/Spring Boot implementation work with the competition judging focus.
---

# E-Learning Competition Planner

Use this skill before implementation planning, milestone reviews, or scope changes for the AI online training management system.

## Planning Rules

- Optimize for a real, working system first: login, roles, courses, plans, learning progress, exams, reports, archives, and AI API features.
- Keep the solo-developer constraint explicit. Prefer one complete end-to-end workflow over many partial screens.
- Treat AI usage evidence as a deliverable, not an afterthought.
- Separate must-have competition requirements from optional extensions.
- Ensure every plan maps to `docs/`, `frontend/`, and `backend/`.

## Required Deliverables

Create or update these documents when relevant:

- `docs/00-竞赛要求与需求拆解.md`
- `docs/01-产品方案.md`
- `docs/02-系统架构设计.md`
- `docs/03-数据库设计.md`
- `docs/04-接口设计.md`
- `docs/05-前端页面设计.md`
- `docs/06-AI能力设计.md`
- `docs/07-测试方案.md`
- `docs/08-部署说明.md`
- `docs/09-演示脚本.md`
- `docs/10-AI工具使用记录.md`
- `docs/daily/YYYY-MM-DD.md`

## Scope Tiers

Use this priority order:

1. Core loop: admin publishes training plan, student learns, student exams, admin sees reports and archives.
2. Role depth: admin, teacher, student menus and permissions.
3. AI features: training plan generation, course summary, question generation, learning report, archive summary.
4. Polish: export documents, charts, notification center, anti-cheating signals.

## Competition Review Focus

When proposing work, call out:

- Business value: reduced offline training cost and management workload.
- Full-process coverage: resource, plan, learning, assessment, analysis, archive.
- AI construction process: how AI helped requirements, design, coding, testing, docs, and review.
- Engineering credibility: real database, real API, real auth, stable deployment, seeded demo data.

## Output Format

For project plans, provide:

- Goal
- Scope
- Module breakdown
- Milestones
- Risks
- Documents to update
- Acceptance checks
