---
name: springboot-crud-quality
description: Enforce consistent Spring Boot CRUD, REST API, security, validation, persistence, logging, and testing patterns for the online training management backend. Use when editing backend/ Java code, controllers, services, repositories, DTOs, entities, migrations, security config, or report/export APIs.
---

# Spring Boot CRUD Quality

Use this skill with `java-spring-boot` for backend implementation.

## Module Shape

Prefer this structure per business module:

```text
module
├── controller
├── service
├── repository
├── entity
├── dto
├── mapper
└── enums
```

Follow existing project patterns if they differ.

## API Rules

- Use DTOs for requests and responses; do not expose entities directly.
- Validate request DTOs with Bean Validation.
- Return a consistent response envelope if the project uses one.
- Support pagination for list endpoints.
- Use clear REST paths under `/api`.
- Add authorization checks for admin, teacher, and student role boundaries.
- Keep controller logic thin; put business rules in services.

## Service Rules

- Use transactions around writes and multi-step workflows.
- Check ownership and role access before mutation.
- Make status transitions explicit, especially for training plans, exams, and archives.
- Log important operations: publish plan, upload material, start exam, submit exam, export report, AI generation.

## Persistence Rules

- Keep audit fields: `createdAt`, `updatedAt`, `createdBy`, `updatedBy` where useful.
- Prefer soft delete for user-facing business records.
- Add indexes for foreign keys and frequent filters: user, course, plan, department, status, exam.
- Avoid N+1 query patterns in dashboard and report endpoints.

## Error Handling

- Use domain exceptions for not found, forbidden, invalid state, duplicate, and external AI failures.
- Return useful messages without leaking stack traces or secrets.
- Treat AI API failures as recoverable unless the user explicitly requires generation to complete the workflow.

## Testing Checklist

For each module, cover:

- Happy path
- Validation failure
- Permission failure
- Not found
- Invalid state transition
- Pagination/filtering where applicable

Run backend tests before finalizing a backend change.
