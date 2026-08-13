---
name: agency-agents
description: Use The Agency role-based AI agent personas. Load when the user asks for an agency agent, specialist persona, multi-role review, role-based brainstorming, or wants expert perspectives such as frontend developer, backend architect, UX researcher, code reviewer, product manager, tester, marketer, strategist, or agents orchestrator.
---

# Agency Agents

This skill provides access to The Agency agent personas installed under `agents/`.

Use this skill when the user wants:
- a specialist role or persona to review, plan, or critique work
- multiple expert perspectives on a product, design, code, marketing, support, or strategy problem
- a named Agency agent such as Frontend Developer, Backend Architect, Code Reviewer, UX Researcher, Product Manager, QA Tester, or Agents Orchestrator
- role-based brainstorming before implementation

## Workflow

1. Identify the user's domain and choose one or more matching agent files under `agents/`.
2. Read only the relevant agent markdown files.
3. Apply the persona's mission, constraints, workflow, and deliverable expectations.
4. If multiple agents are useful, synthesize their perspectives in the main response instead of creating unnecessary indirection.
5. For coding tasks, still follow the project's existing skills, repo instructions, tests, and verification gates.

## Agent Directory

Agent files are grouped by division:

- `agents/academic/`
- `agents/design/`
- `agents/engineering/`
- `agents/finance/`
- `agents/game-development/`
- `agents/marketing/`
- `agents/paid-media/`
- `agents/product/`
- `agents/project-management/`
- `agents/sales/`
- `agents/spatial-computing/`
- `agents/specialized/`
- `agents/strategy/`
- `agents/support/`
- `agents/testing/`

## Selection Hints

- Frontend/UI work: `agents/engineering/engineering-frontend-developer.md`, `agents/design/design-ui-designer.md`, `agents/design/design-ux-architect.md`
- Backend/API work: `agents/engineering/engineering-backend-architect.md`, `agents/engineering/engineering-software-architect.md`
- Code review: `agents/engineering/engineering-code-reviewer.md`
- Testing/QA: files under `agents/testing/`
- Product planning: files under `agents/product/` and `agents/project-management/`
- Multi-agent orchestration: `agents/specialized/agents-orchestrator.md`

## Notes

The source repository is `msitarzewski/agency-agents`. These files are role instructions, not executable tools. Treat them as expert guidance layered on top of Codex's normal tool use and safety constraints.
