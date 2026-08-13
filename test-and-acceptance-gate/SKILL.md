---
name: test-and-acceptance-gate
description: Verify feature completeness for the AI online training management system. Use before marking any frontend, backend, AI, report, exam, learning, permission, deployment, or documentation work complete; especially when checking practical acceptance criteria and regression risks.
---

# Test And Acceptance Gate

Use this skill at the end of each module and before final delivery.

## Acceptance Checklist

For each feature, verify:

- The intended role can complete the workflow.
- Unauthorized roles cannot access or mutate data.
- Backend validation rejects bad input.
- Frontend displays loading, empty, error, and success states where applicable.
- Data persists and can be refreshed.
- Related docs are updated.

## Core Workflow Tests

Run through these flows regularly:

- Login as admin, teacher, and student.
- Admin creates or publishes a training plan.
- Teacher creates course content and questions.
- Student continues learning and progress is retained.
- Student submits an exam and receives an automatic score.
- Admin views progress, score analysis, archive, and report export.
- AI generation succeeds and failure is handled cleanly.

## Backend Checks

- Run available backend tests.
- Check API status codes and error messages.
- Check pagination and filters.
- Check security rules on protected endpoints.
- Check database records for correct ownership and status.

## Frontend Checks

- Run type checking and build.
- Check route guards.
- Check form validation.
- Check dashboard and table rendering.
- Check exam timer and submission behavior.

## Documentation Checks

Do not consider work complete unless docs reflect:

- feature behavior
- API changes
- database changes
- AI prompt/model usage when relevant
- test results
- known limitations

## Final Delivery Gate

Before final answer or submission, report:

- Tests run
- Manual workflows verified
- Documents updated
- Remaining risks
