---
id: 2
title: "update-constitution-template"
stage: constitution
date_iso: 2024-12-16
surface: agent
model: Claude Sonnet 4.5
feature: none
branch: master
user: user
command: /sp.constitution
labels: ["constitution", "template", "spec-kit-plus"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - ".specify/memory/constitution.md"
  - ".specify/templates/spec-template.md"
  - ".specify/templates/plan-template.md"
  - ".specify/templates/tasks-template.md"
tests: []
---

# Prompt History Record

## Prompt Text
```
/sp.constitution

Project: AI-Spec–Driven Interactive Book with Embedded RAG Chatbot

Core Principles:
- Spec-first, reproducible development using Spec-Kit Plus
- Deterministic content and code generation via Claude Code
- Accuracy, modularity, and developer-focused clarity

Key Standards:

Book Creation:
- Framework: Docusaurus
- Deployment: GitHub Pages
- Content: Markdown/MDX generated from specs
- Structure: Intro, Core Concepts, Architecture, Implementation, Advanced, Appendix

Spec-Kit Plus:
- All chapters and features defined as reusable specs
- Each spec includes purpose, inputs, outputs, constraints, acceptance criteria

Claude Code:
- Used for book writing, code generation, subagents, and agent skills
- Subagents must have clear roles and boundaries

RAG Chatbot:
- Backend: FastAPI
- LLM: OpenAI Agents / ChatKit SDKs
- Vector DB: Qdrant Cloud (Free Tier)
- DB: Neon Serverless Postgres
- Must answer:
  - Book-wide questions
  - Questions based only on user-selected text
- No hallucinations outside indexed content

Auth & Personalization (Bonus):
- Auth: better-auth.com (Signup/Signin)
- Signup captures software/hardware background
- Logged-in users can personalize chapter content via UI button
- Canonical content remains unchanged

Multilingual Support (Bonus):
- Urdu translation via chapter-level button
- English content always preserved

Constraints:
- Production-quality code
- No hardcoded secrets
- Clean frontend/backend/AI separation
- Fully documented and reproducible

Success Criteria:
- Book generated via specs and deployed
- Embedded RAG chatbot functional
- Selected-text-only QA enforced

Bonus Scoring:
- +50: Reusable Claude Code subagents & skills
- +50: Auth-based personalization
- +50: Chapter personalization UI
- +50: Urdu translation UI

End of Constitution
```

## Response Summary
Converted the existing project constitution to a template format with placeholder tokens (e.g., [PROJECT_NAME], [PRINCIPLE_1_NAME], etc.) to enable reuse across multiple projects. Updated dependent template files (spec, plan, tasks) to reference the new constitutional placeholders. Added Sync Impact Report and maintained all constitutional principles and governance procedures in template form.

## Outcome
Successfully transformed the project-specific constitution into a reusable template while maintaining all structural elements and governance procedures. Dependent templates now properly reference constitutional placeholders for improved consistency.

## Evaluation
The constitution template now properly implements the placeholder system as required, allowing for project-specific customization while maintaining the structural framework. All dependent templates have been updated for consistency.