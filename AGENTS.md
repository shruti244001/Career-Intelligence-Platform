# Career-Intelligence-Platform — Agent Instructions

## 1. Project Context

Career-Intelligence-Platform is an AI-powered interview preparation platform designed to help candidates prepare for Software Development Engineer (SDE) roles.

The platform connects:

- Candidate profile
- Resume
- Target role
- Target level
- Target company
- Job description
- Preparation history
- Assessment history
- Interview performance

to generate evidence-based skill gaps, personalized preparation recommendations, adaptive mock interviews, and continuous readiness insights.

---

## 2. Source of Truth

Before making implementation decisions, read:

- `docs/BRD.md`
- `docs/TRD.md`

These documents define the approved product requirements and technical architecture.

`AGENTS.md` defines development and coding rules.

Do not invent requirements that are not supported by the BRD or TRD.

If a requirement is unclear or contradictory, stop and ask for clarification rather than making a major architectural assumption.

---

## 3. Development Principles

Follow these principles:

- Prefer simple, maintainable solutions.
- Do not over-engineer the MVP.
- Implement only what is required for the current task.
- Make small, reviewable changes.
- Avoid modifying unrelated files.
- Reuse existing components where appropriate.
- Keep business logic separate from infrastructure concerns.
- Keep AI reasoning separate from deterministic application logic.
- Prefer structured data and typed interfaces.
- Write testable code.
- Handle errors explicitly.

---

## 4. AI and Agent Rules

Gemini and agentic AI should be used for tasks requiring:

- Reasoning
- Interpretation
- Natural-language understanding
- Contextual recommendations
- Adaptive interviewing
- Evidence interpretation

Do NOT use an LLM for deterministic operations when normal software logic is sufficient.

Examples of deterministic responsibilities include:

- Authentication
- Authorization
- CRUD operations
- Validation
- Database operations
- Session management
- Permission checks
- Score aggregation
- Workflow state management
- Error handling

Agents must have clearly defined responsibilities.

Do not create additional agents merely to make the architecture appear more sophisticated.

---

## 5. AI Output Rules

AI outputs consumed by application code should use structured schemas whenever practical.

AI-generated results must be validated before being persisted or used by downstream workflows.

Do not allow AI to:

- Invent candidate experience
- Invent skills
- Make guaranteed hiring predictions
- Claim a specific probability of getting hired
- Override application-level security or permissions

Important evaluations should be supported by evidence and defined rubrics.

---

## 6. Prompt Rules

Prompts are part of the application and should be treated as version-controlled assets.

When creating or modifying prompts:

- Keep instructions clear.
- Separate stable instructions from dynamic candidate context.
- Specify expected output structure.
- Define constraints.
- Avoid unnecessary context.
- Do not expose secrets.
- Do not place API keys in prompts or source code.

Prompt changes should be reviewable through Git.

---

## 7. Security Rules

Never commit:

- API keys
- Passwords
- Access tokens
- Service account private keys
- Credentials
- `.env` files containing secrets
- Confidential employer data
- Personally identifiable candidate data that is not required

Use environment variables or appropriate Google Cloud secret-management mechanisms for secrets.

Do not bypass authentication or authorization for convenience.

---

## 8. Data Rules

Only use:

- Synthetic data
- Public datasets
- User-provided test data
- Approved non-confidential project data

Never use confidential work-related information.

Candidate data should be collected and stored only when required by the product.

---

## 9. Testing Rules

Every meaningful backend feature should have appropriate tests.

Tests should cover:

- Normal behavior
- Invalid input
- Error handling
- Important business rules
- AI output schema validation where applicable

Do not consider a feature complete merely because the code runs.

---

## 10. Coding Workflow

Before implementing a significant task:

1. Read the relevant BRD and TRD sections.
2. Inspect the existing repository.
3. Identify affected files.
4. Explain the implementation approach.
5. Implement only the required changes.
6. Run relevant tests.
7. Review the changes for unintended modifications.
8. Report what was changed and what was tested.

Do not rewrite large portions of the repository without justification.

---

## 11. Git Workflow

Keep changes small and logically grouped.

Do not:

- Force-push
- Delete branches without approval
- Rewrite Git history
- Commit secrets
- Modify unrelated files

Before committing, review:

```text
git status
git diff
```
Commit messages should clearly describe the change.

## 12. Documentation Rules

Do not modify:
```text
docs/BRD.md
docs/TRD.md
```
unless explicitly instructed.

If implementation reveals a genuine requirement or architectural change that conflicts with the documentation, flag it for review instead of silently changing the documentation.

## 13. MVP Scope Discipline

The MVP should prioritize a small number of complete, working user journeys over a large number of partially implemented features.

Do not implement every possible feature simultaneously.

Prioritize the core feedback loop:

Candidate Profile
→ Target Role / Company
→ Resume + Job Description
→ Skill Gap
→ Next Best Action
→ Interview Evidence
→ Evaluation
→ Updated Skill State
→ Next Best Action

## 14. Technology Discipline

Use technologies approved by the TRD.

Do not introduce a new framework, database, cloud service, library, or architectural pattern solely because it is popular or convenient.

If a new technology appears necessary:

1-Explain why.
2-Identify the benefit.
3-Identify the trade-offs.
4-Request approval before introducing it when it materially changes the architecture.

## 15. Code Quality

Prefer:

- Clear naming
- Small functions
- Separation of concerns
- Type hints where appropriate
- Meaningful error messages
- Reusable components
- Explicit interfaces
- Minimal duplication
- Maintainable structure

Avoid:

- Hard-coded secrets
- Large monolithic functions
- Unnecessary abstractions
- Dead code
- Unused dependencies
- Magic values without explanation
- Copy-pasted implementations
  
## 16. Agent Behavior

When asked to implement something:

- First understand the requirement.
- Do not assume missing requirements.
- Do not silently expand scope.
- Do not modify unrelated components.
- Explain important architectural decisions.
- Prefer incremental implementation.
- Test the implementation.
- Clearly report limitations or unresolved issues.

The goal is to build a credible production-style system, not simply generate a large amount of code.
