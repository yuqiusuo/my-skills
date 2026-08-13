---
name: demo-and-review-prep
description: Prepare competition demo and review materials for the AI online training management system. Use when creating demo accounts, seeded data, 30-minute presentation flow, review script, AI tool usage explanation, development summary, submission checklist, or final defense materials.
---

# Demo And Review Prep

Use this skill after major features are implemented and before submission or rehearsal.

## Demo Structure

For a 30-minute review, use:

1. Project background and value, 3 minutes.
2. Admin workflow, 7 minutes.
3. Teacher workflow and AI question generation, 5 minutes.
4. Student learning and exam workflow, 6 minutes.
5. Reports, archives, and exports, 4 minutes.
6. AI tool usage and development summary, 4 minutes.
7. Risks, extensions, and Q&A buffer, 1 minute.

## Demo Accounts

Prepare at least:

- `admin / 123456`
- `teacher / 123456`
- `student / 123456`

Record exact accounts in `docs/08-部署说明.md` and `docs/09-演示脚本.md`.

## Seed Data

Ensure the demo environment includes:

- departments, positions, and levels
- multiple users per role
- course categories
- video/document/courseware sample materials
- one published training plan
- one student with partial progress
- one student with completed progress
- question bank and exam paper
- submitted exam records
- generated AI records
- report/archive examples

## Review Talking Points

Prepare concise answers for:

- Why this system reduces training cost.
- How the full training process is digitized.
- Which features use real AI APIs.
- How AI improved development efficiency.
- How permissions protect role boundaries.
- How reports and archives support management decisions.

## Final Checklist

Before submission:

- Confirm repository contains `docs/`, `frontend/`, and `backend/`.
- Confirm demo URL is reachable.
- Confirm accounts work.
- Confirm AI API config is documented without exposing secrets.
- Confirm startup and deployment steps are repeatable.
- Confirm 30-minute script matches the deployed system.
