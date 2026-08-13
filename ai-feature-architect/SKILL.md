---
name: ai-feature-architect
description: Design and implement reliable real AI API features for the online training management system. Use when adding or changing large-model API calls, prompt templates, JSON response schemas, AI generation logs, retries, fallbacks, cost tracking, or AI-assisted training plan, summary, question, report, and archive features.
---

# AI Feature Architect

Use this skill with `openai-docs` when implementation depends on current OpenAI API details.

## Core Principle

AI should enhance the system, not block the core training workflow. Business functions must remain usable when AI generation fails.

## Required AI Features

Prioritize these features:

1. Generate training plan suggestions from department, role, level, goal, and duration.
2. Generate course summary, learning objectives, and key points.
3. Generate exam questions from course material or knowledge points.
4. Generate student learning analysis from progress, time, and score.
5. Generate archive summary from a user's training history.

## Backend Design

Implement an AI boundary:

```text
AiController -> AiService -> AiClient
```

Use configuration:

```text
AI_API_BASE_URL
AI_API_KEY
AI_MODEL
```

Never hard-code secrets. Never log API keys.

## Response Discipline

- Prefer structured JSON outputs for data that enters the database.
- Validate generated JSON before persistence.
- Store AI output as draft content when human review is appropriate.
- Keep prompt templates versioned in code or docs.

## Logging Table

Every AI call should create or update an `ai_generation_record` with:

- feature type
- model/provider
- input summary
- output summary
- status
- error message if failed
- latency
- operator
- created time

## Failure Handling

- Time out external calls.
- Surface a clear user-facing error.
- Preserve user input so the user can retry.
- Do not roll back unrelated business data because AI failed unless the operation is explicitly AI-only.

## Documentation

Update `docs/06-AI能力设计.md` and `docs/10-AI工具使用记录.md` for every new AI capability.
