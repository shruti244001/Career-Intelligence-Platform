# CareerGraph AI

> Evidence-based career intelligence and interview-readiness platform for software engineering candidates.

CareerGraph AI is a structured career-intelligence platform designed to help candidates understand their current demonstrated skills, compare them against a target role, identify evidence-backed skill gaps, receive prioritized next-best actions, and continuously update their readiness through interview evaluation.

The platform is designed around a closed learning loop:

```
Candidate Profile
        ↓
Target Role
        ↓
Target Competencies
        ↓
Evidence-Based Skill Gap Analysis
        ↓
Next Best Action
        ↓
Mock Interview
        ↓
Evaluation
        ↓
New Evidence
        ↓
Updated Skill State
        ↓
New Recommendation
```

The long-term goal is to build a production-oriented AI system where generative AI is used for reasoning and interpretation while deterministic domain logic remains responsible for validation, scoring, state transitions, and other critical decisions.

---

## Table of Contents

1. [Project Vision](#1-project-vision)
2. [Core Product Concept](#2-core-product-concept)
3. [Key Principles](#3-key-principles)
4. [Current Implementation Status](#4-current-implementation-status)
5. [Current Test Status](#5-current-test-status)
6. [Architecture](#6-architecture)
7. [Backend Structure](#7-backend-structure)
8. [Domain Model](#8-domain-model)
9. [Evidence Model](#9-evidence-model)
10. [Skill State](#10-skill-state)
11. [Target Profile](#11-target-profile)
12. [Target Competency Expectations](#12-target-competency-expectations)
13. [Evaluation Framework](#13-evaluation-framework)
14. [Skill Gap Analysis](#14-skill-gap-analysis)
15. [Application Services](#15-application-services)
16. [Target Profile and Skill Gap Workflow](#16-target-profile-and-skill-gap-workflow)
17. [Recommendation Engine](#17-recommendation-engine)
18. [Interview and Evaluation Loop](#18-interview-and-evaluation-loop)
19. [AI Architecture](#19-ai-architecture)
20. [Planned API](#20-planned-api)
21. [Frontend](#21-frontend)
22. [Planned User Journey](#22-planned-user-journey)
23. [Technology Stack](#23-technology-stack)
24. [Project Documentation](#24-project-documentation)
25. [Development Philosophy](#25-development-philosophy)
26. [Quality Gates](#26-quality-gates)
27. [Local Development](#27-local-development)
28. [Running Tests](#28-running-tests)
29. [Code Quality](#29-code-quality)
30. [Git Workflow](#30-git-workflow)
31. [Development Roadmap](#31-development-roadmap)
32. [MVP Definition](#32-mvp-definition)
33. [Future Enhancements](#33-future-enhancements)
34. [Design Goals](#34-design-goals)
35. [Project Status](#35-project-status)
36. [License](#36-license)
37. [Author](#37-author)

---

## 1. Project Vision

Most career and interview-preparation platforms provide static roadmaps, generic recommendations, or chatbot-style advice.

CareerGraph AI takes a different approach.

Instead of asking:

> "What should I learn for a software engineering interview?"

the platform aims to answer:

> "Given my target role, my current demonstrated evidence, my evaluation history, and the competencies required for that role, what is the most valuable thing I should do next?"

The system therefore focuses on:

- Evidence rather than unsupported claims
- Target-specific competency expectations
- Deterministic skill-state management
- Rubric-based evaluation
- Prioritized skill gaps
- Personalized next-best actions
- Continuous readiness updates
- Explainable recommendations
- AI-assisted reasoning with controlled application state

---

## 2. Core Product Concept

CareerGraph represents career readiness as a continuously evolving graph of:

```
Candidate
    |
    +---- Profile
    |
    +---- Evidence
    |
    +---- Competencies
    |
    +---- Skill States
    |
    +---- Target Profile
              |
              +---- Role
              +---- Level
              +---- Company
              +---- Job Description
              +---- Target Competencies
```

Candidate evidence is evaluated against target expectations:

```
Candidate Evidence
        +
Target Competency Expectations
        |
        v
Skill Gap Analysis
        |
        v
Gap Classification
        |
        v
Priority
        |
        v
Next Best Action
```

Interview performance creates new evidence:

```
Interview
    |
    v
Candidate Response
    |
    v
Rubric Evaluation
    |
    v
Evidence
    |
    v
Skill State Update
    |
    v
Updated Skill Gap
```

This creates the central CareerGraph feedback loop.

---

## 3. Key Principles

### 3.1 Evidence First

The platform distinguishes between:

- Explicit evidence
- Supported inference
- Missing evidence

Evidence also has a strength:

- `WEAK`
- `MODERATE`
- `STRONG`

This prevents the system from treating every resume claim or AI inference as equally reliable.

### 3.2 Deterministic Domain Logic

Critical state should not be controlled directly by an LLM.

The application uses deterministic domain models and validation for concepts such as:

- Competencies
- Target profiles
- Skill states
- Evidence
- Rubrics
- Evaluation results
- Scoring
- Gap classification
- Gap priority

AI can interpret information and propose structured outputs, but domain rules remain responsible for enforcing valid application state.

### 3.3 Target-Specific Readiness

Career readiness is not treated as one universal score.

A candidate can be **strong** for:

- Software Engineer / SDE-1

while simultaneously having **gaps** for:

- Software Engineer / SDE-2

Target expectations therefore depend on:

- Role
- Level
- Optional company
- Optional job description

### 3.4 Continuous Updating

The platform is designed as a feedback system rather than a one-time assessment.

New evidence can come from:

- Resume
- Candidate profile
- Coding interviews
- Code submissions
- Behavioral interviews
- System-design interviews
- Assessments
- Preparation activities

New evidence can update the candidate's demonstrated skill state and therefore change the recommended next action.

---

## 4. Current Implementation Status

CareerGraph is being developed incrementally using a domain-first architecture.

**Implemented**

- [x] Shared domain types
- [x] Domain validation utilities
- [x] Evidence domain models
- [x] Skill-state domain models
- [x] Rubric domain models
- [x] Deterministic scoring models
- [x] Evaluation domain models
- [x] Evaluation application service
- [x] Competency domain models
- [x] Target competency expectations
- [x] Target profile domain model
- [x] Comprehensive unit tests
- [x] Ruff validation
- [x] Mypy validation

**In Progress**

- [ ] Target profile application service
- [ ] Candidate application service
- [ ] Skill-gap domain model
- [ ] Skill-gap application service
- [ ] Repository / persistence layer
- [ ] REST API layer
- [ ] Target + skill-gap workflow
- [ ] Recommendation service
- [ ] Interview service
- [ ] Frontend
- [ ] AI agent integration
- [ ] GCP deployment

The project intentionally follows an incremental implementation strategy instead of introducing all infrastructure at once.

---

## 5. Current Test Status

The current backend test suite contains:

**56 tests passed**

Static quality checks:

| Tool | Result |
|------|--------|
| Ruff | All checks passed |
| Mypy | Success: no issues found |

The test suite currently covers:

- Health endpoint
- Skill states
- Competencies
- Target profiles
- Evaluations
- Scoring
- Evaluation application service

> **Note:** A FastAPI/Starlette dependency deprecation warning may appear during testing. It is currently an upstream dependency warning and does not cause test failures.

---

## 6. Architecture

CareerGraph follows a modular-monolith architecture during the MVP phase.

```
                    ┌─────────────────────┐
                    │      Frontend       │
                    └──────────┬──────────┘
                               │
                               │ HTTPS
                               ▼
                    ┌─────────────────────┐
                    │      API Layer      │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Application Layer   │
                    │                     │
                    │ Candidates          │
                    │ Targets             │
                    │ Evaluations         │
                    │ Interviews          │
                    │ Workflows           │
                    │ Recommendations     │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │    Domain Layer     │
                    │                     │
                    │ Competencies        │
                    │ Evidence            │
                    │ Skill States        │
                    │ Rubrics             │
                    │ Evaluations         │
                    │ Scoring             │
                    │ Targets             │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Persistence Layer   │
                    └─────────────────────┘
```

AI and workflow orchestration will interact with the application through controlled interfaces rather than directly modifying domain state.

---

## 7. Backend Structure

Current backend structure:

```
backend/
│
├── src/
│   └── careergraph/
│       │
│       ├── application/
│       │   ├── candidates/
│       │   ├── evaluations/
│       │   │   └── service.py
│       │   ├── interviews/
│       │   ├── targets/
│       │   └── workflows/
│       │
│       ├── domain/
│       │   ├── competencies/
│       │   │   ├── models.py
│       │   │   └── __init__.py
│       │   │
│       │   ├── evaluations/
│       │   ├── evidence/
│       │   ├── rubrics/
│       │   ├── scoring/
│       │   ├── skill_states/
│       │   ├── targets/
│       │   │   └── models.py
│       │   ├── types.py
│       │   └── _validation.py
│       │
│       ├── main.py
│       └── __init__.py
│
├── tests/
│   └── unit/
│       ├── application/
│       ├── domain/
│       └── test_health.py
│
├── pyproject.toml
└── README.md
```

---

## 8. Domain Model

### 8.1 Competency

A competency represents a capability that can be evaluated.

Examples:

- Graphs
- Dynamic Programming
- Object-Oriented Programming
- SQL
- Operating Systems
- System Design
- Communication
- Ownership

A competency has:

- ID
- Identifier
- Name
- Description
- Category
- Parent Competency
- Active State

Competencies use stable identifiers so that evidence and evaluations can reference the same capability consistently.

---

## 9. Evidence Model

Evidence represents information that supports a candidate's demonstrated capability.

Potential sources include:

- Resume
- Candidate profile
- Coding interview
- Code submission
- Behavioral interview
- System design interview
- Assessment
- Preparation activity

Evidence strength is represented as:

- `WEAK`
- `MODERATE`
- `STRONG`

The system can therefore distinguish between:

> "I listed Graphs on my resume."

and

> "I successfully solved multiple graph problems during an evaluated coding interview."

These should not necessarily have the same evidentiary strength.

---

## 10. Skill State

A Skill State represents the candidate's current demonstrated state for a competency.

Conceptually:

```
SkillState
├── competency
├── proficiency
├── score
├── evidence coverage
├── confidence
├── evidence IDs
└── last evaluated timestamp
```

Proficiency states include:

- `WEAK`
- `DEVELOPING`
- `PROFICIENT`
- `STRONG`

This allows CareerGraph to maintain a structured representation of the candidate's current capabilities.

---

## 11. Target Profile

A Target Profile represents where the candidate wants to reach:

```
Target Role
+
Target Level
+
Optional Company
+
Optional Job Description
```

Example:

```json
{
  "target_profile_id": "target_001",
  "candidate_id": "candidate_001",
  "role": "Software Engineer",
  "level": "SDE-1",
  "company": "Optional",
  "job_description_id": "jd_001",
  "status": "active"
}
```

The target profile is associated with expected competency levels.

---

## 12. Target Competency Expectations

A Target Competency Expectation represents the level a candidate is expected to demonstrate for a specific competency within a target.

Example:

- Target: Software Engineer / SDE-1
- Competency: Graphs
- Expected Proficiency: `PROFICIENT`
- Importance: `0.85`

The same competency can have different expectations for different targets:

| Target | Competency | Expectation |
|--------|-----------|-------------|
| SDE-1  | Graphs    | Proficient  |
| SDE-2  | Graphs    | Strong      |
| SDE-3  | Graphs    | Strong      |

This makes the competency system reusable across different career targets.

---

## 13. Evaluation Framework

CareerGraph uses rubric-based deterministic evaluation.

The evaluation pipeline is:

```
Evidence
   |
   v
Rubric
   |
   v
Rubric Dimensions
   |
   v
Dimension Evaluation
   |
   v
Evidence Coverage
   |
   v
Dimension Score
   |
   v
Weighted Evaluation
```

Evidence strength follows:

```
WEAK < MODERATE < STRONG
```

Therefore stronger evidence can satisfy a weaker evidence requirement.

The evaluation service currently performs:

- Evidence-to-competency matching
- Evidence strength evaluation
- Evidence coverage calculation
- Deterministic score calculation
- Confidence calculation
- Weighted rubric evaluation

The detailed evaluation design is documented in [`docs/evaluation-framework.md`](docs/evaluation-framework.md).

---

## 14. Skill Gap Analysis

The planned skill-gap engine compares:

```
Current Skill State
        +
Target Competency Expectation
        |
        v
Skill Gap Classification
        |
        v
Priority
```

Possible classifications include:

- `INSUFFICIENT_EVIDENCE`
- `BELOW_TARGET`
- `MEETS_TARGET`
- `EXCEEDS_TARGET`

Priorities include:

- `LOW`
- `MEDIUM`
- `HIGH`

Example:

```json
{
  "skill": "Graphs",
  "current_level": "developing",
  "target_level": "proficient",
  "classification": "below_target",
  "priority": "high",
  "confidence": 0.86
}
```

The confidence value represents confidence in the evidence and analysis, not probability of getting hired.

---

## 15. Application Services

The application layer orchestrates domain operations.

**Current services:**

- `EvaluationService`

**Planned services:**

- `CandidateService`
- `TargetProfileService`
- `SkillGapService`
- `RecommendationService`
- `InterviewService`
- `WorkflowService`

The application layer should coordinate use cases without placing business rules directly into API handlers.

---

## 16. Target Profile and Skill Gap Workflow

The first major end-to-end workflow is planned as:

```
Candidate
    |
    v
Candidate Profile
    |
    v
Target Role + Level
    |
    v
Target Requirements
    |
    v
Target Profile
    |
    v
Target Competency Expectations
    |
    v
Candidate Skill States
    |
    v
Skill Gap Analysis
    |
    v
Prioritized Skill Gaps
```

Optional information such as company and job description can refine the target.

---

## 17. Recommendation Engine

The recommendation engine will use:

- Current Skill State
- Target Profile
- Skill Gaps
- Recent Evidence
- Evaluation History

to determine the **Next Best Action**.

The goal is not to produce a generic learning roadmap. Instead, the system should dynamically prioritize the most valuable action based on the candidate's current state.

**Example:**

Current State:

- Graphs → Developing
- System Design → Weak
- OOP → Strong

Target: SDE-1

Recommendation: Practice graph traversal problems before moving to advanced system design.

---

## 18. Interview and Evaluation Loop

The long-term interview workflow is:

```
Create Interview
       |
       v
Generate Questions
       |
       v
Candidate Responds
       |
       v
Evaluate Response
       |
       v
Generate Evidence
       |
       v
Update Skill State
       |
       v
Recalculate Skill Gaps
       |
       v
Generate Next Best Action
```

This creates a continuous improvement loop rather than a one-time interview score.

---

## 19. AI Architecture

Generative AI will be used where reasoning and interpretation provide value.

Potential agents include:

```
Orchestrator Agent
        |
        +── Profile & Requirement Agent
        |
        +── Resume Analysis Agent
        |
        +── Interview Agent
        |
        +── Evaluation Interpretation Agent
        |
        +── Recommendation Agent
```

The AI layer should not directly expose or mutate raw application state. Instead:

```
AI Agent
   |
   v
Structured Output
   |
   v
Application Layer
   |
   v
Domain Validation
   |
   v
Persisted State
```

This architecture reduces the risk of hallucinated or invalid state entering the core system.

---

## 20. Planned API

The backend API is planned around versioned resources:

```
/api/v1/profile
/api/v1/targets
/api/v1/resumes
/api/v1/job-descriptions
/api/v1/skill-gaps
/api/v1/recommendations
/api/v1/interviews
/api/v1/evaluations
/api/v1/workflows
```

Example target endpoints:

```
GET    /api/v1/targets
POST   /api/v1/targets
GET    /api/v1/targets/{target_id}
PUT    /api/v1/targets/{target_id}
```

The API layer will be implemented after the core application services are established.

---

## 21. Frontend

The planned frontend will provide a candidate-facing CareerGraph dashboard.

The initial experience will include:

```
Dashboard
│
├── Candidate Profile
│
├── Target Role
│
├── Readiness Overview
│
├── Competency Map
│
├── Skill Gaps
│
├── Priority Actions
│
├── Interview Practice
│
└── Evaluation History
```

A key goal is to make the final application directly demonstrable to project organisers rather than requiring them to inspect backend code.

---

## 22. Planned User Journey

The intended user experience is:

1. Candidate creates profile
2. Candidate selects target role and level
3. Candidate uploads resume
4. Candidate provides target job description
5. System creates target profile
6. System identifies skill gaps
7. System recommends highest-priority action
8. Candidate completes interview assessment
9. System evaluates performance
10. New evidence is created
11. Skill state is updated
12. Skill gaps are recalculated
13. Next best action is generated

---

## 23. Technology Stack

**Backend**

- Python 3.12
- FastAPI
- Pydantic
- Pytest
- Ruff
- Mypy

**AI / Cloud (Planned)**

- Google Gemini
- Google Cloud
- Cloud Run
- Cloud Storage
- Managed database services
- Agent orchestration

The exact Gemini model should remain configurable because model selection may change based on:

- Quality requirements
- Latency
- Cost
- Context requirements
- Availability
- Google Cloud recommendations

**Frontend**

The frontend technology will be selected based on the final application requirements and GCP deployment strategy.

---

## 24. Project Documentation

Detailed project architecture is maintained separately from this README:

```
docs/
├── BRD.md
├── TRD.md
├── evaluation-framework.md
└── agents.md
```

**BRD** — The Business Requirements Document defines:

- Product vision
- User requirements
- Business objectives
- Functional requirements
- User journeys
- Product scope

**TRD** — The Technical Requirements Document defines:

- System architecture
- Domain concepts
- Backend architecture
- API design
- Data model
- Workflows
- AI integration
- Deployment architecture
- Security and observability considerations

**Evaluation Framework** — Defines:

- Evidence model
- Rubrics
- Evaluation
- Scoring
- Confidence
- Skill-state updates

**Agent Documentation** — Defines the intended responsibilities and boundaries of AI agents.

These documents will continue to evolve alongside implementation.

---

## 25. Development Philosophy

CareerGraph follows a domain-first development approach:

```
Requirements
     ↓
Domain Model
     ↓
Domain Rules
     ↓
Unit Tests
     ↓
Application Service
     ↓
Integration
     ↓
API
     ↓
AI Workflow
     ↓
Frontend
     ↓
Cloud Deployment
```

This approach intentionally avoids prematurely coupling the business logic to:

- FastAPI
- Database implementation
- Cloud services
- LLM providers
- Frontend frameworks

---

## 26. Quality Gates

Before moving a major component forward, the project should pass:

- `pytest`
- `ruff`
- `mypy`

Example:

```powershell
.\.venv\Scripts\python.exe -m pytest
.\.venv\Scripts\ruff.exe check .
.\.venv\Scripts\mypy.exe .
```

All three checks should remain clean before committing significant changes.

---

## 27. Local Development

**Requirements**

- Python 3.12+
- Git
- Windows, macOS, or Linux

**Create Virtual Environment**

From the backend directory:

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.\.venv\Scripts\Activate.ps1
```

**Install Dependencies**

```bash
pip install -e ".[dev]"
```

If the project configuration changes, reinstall dependencies as required.

---

## 28. Running Tests

Run the complete test suite:

```powershell
.\.venv\Scripts\python.exe -m pytest
```

Run a specific test module:

```powershell
.\.venv\Scripts\python.exe -m pytest tests/unit/domain/test_targets.py -v
```

---

## 29. Code Quality

Run Ruff:

```powershell
.\.venv\Scripts\ruff.exe check .
```

Run Mypy:

```powershell
.\.venv\Scripts\mypy.exe .
```

Expected result:

```
All checks passed!
```

```
Success: no issues found
```

---

## 30. Git Workflow

The project uses Git for incremental development.

Recommended workflow:

```
Make change
    ↓
Run tests
    ↓
Run Ruff
    ↓
Run Mypy
    ↓
Review git diff
    ↓
Commit
```

Example:

```bash
git status
git diff
.\.venv\Scripts\python.exe -m pytest
.\.venv\Scripts\ruff.exe check .
.\.venv\Scripts\mypy.exe .
git add .
git commit -m "Implement target profile service"
git push
```

---

## 31. Development Roadmap

**Phase 1 — Domain Foundation**

- [x] Shared domain types
- [x] Validation
- [x] Evidence
- [x] Skill states
- [x] Rubrics
- [x] Scoring
- [x] Evaluations
- [x] Competencies
- [x] Target profiles

**Phase 2 — Application Layer**

- [x] Evaluation service
- [ ] Target profile service
- [ ] Candidate service
- [ ] Skill-gap service
- [ ] Recommendation service
- [ ] Interview service

**Phase 3 — Persistence**

- [ ] Repository interfaces
- [ ] Database schema
- [ ] Repository implementations
- [ ] Persistence integration tests

**Phase 4 — API**

- [ ] Candidate APIs
- [ ] Target APIs
- [ ] Resume APIs
- [ ] Job description APIs
- [ ] Skill-gap APIs
- [ ] Recommendation APIs
- [ ] Interview APIs
- [ ] Evaluation APIs

**Phase 5 — Intelligent Workflows**

- [ ] Target profile generation
- [ ] Skill-gap analysis workflow
- [ ] Recommendation workflow
- [ ] Interview workflow
- [ ] Evaluation workflow
- [ ] Skill-state update workflow

**Phase 6 — AI Integration**

- [ ] Gemini integration
- [ ] Agent orchestration
- [ ] Structured AI outputs
- [ ] AI validation boundaries
- [ ] Prompt management
- [ ] Agent observability

**Phase 7 — Frontend**

- [ ] Candidate onboarding
- [ ] Target setup
- [ ] Resume upload
- [ ] Readiness dashboard
- [ ] Skill-gap visualization
- [ ] Recommendation interface
- [ ] Interview interface
- [ ] Evaluation results

**Phase 8 — Cloud Deployment**

- [ ] Google Cloud architecture
- [ ] Cloud Run deployment
- [ ] Cloud Storage
- [ ] Database deployment
- [ ] Gemini integration
- [ ] Secrets/configuration
- [ ] Monitoring
- [ ] Production testing
- [ ] Public demo environment

---

## 32. MVP Definition

The MVP should demonstrate the complete CareerGraph loop rather than attempting to implement every planned feature.

The target MVP is:

```
Candidate
    ↓
Target Role
    ↓
Target Profile
    ↓
Target Competencies
    ↓
Skill Gap Analysis
    ↓
Priority
    ↓
Next Best Action
    ↓
Mock Interview
    ↓
Evaluation
    ↓
Evidence
    ↓
Updated Skill State
```

The MVP should be accessible through a polished frontend and deployed to Google Cloud.

---

## 33. Future Enhancements

Potential future capabilities include:

- Multi-role comparison
- Company-specific interview preparation
- Job-market intelligence
- Historical readiness tracking
- Personalized learning plans
- Advanced system-design evaluation
- Behavioral competency tracking
- Portfolio analysis
- GitHub evidence integration
- Learning-resource recommendations
- Interview trend analysis
- Recruiter-facing analytics
- Career progression simulation

These features are outside the initial MVP unless implementation priorities change.

---

## 34. Design Goals

CareerGraph aims to be:

- **Evidence-based** — Recommendations should be grounded in available candidate evidence.
- **Explainable** — The system should explain why a competency is considered a gap and why an action was prioritized.
- **Deterministic where necessary** — Critical state transitions and scoring should not depend entirely on probabilistic model output.
- **AI-assisted** — Generative AI should be used where reasoning, extraction, interpretation, and conversational interaction provide meaningful value.
- **Modular** — Core business logic should remain independent from infrastructure.
- **Extensible** — New roles, levels, competencies, assessment types, and AI models should be addable without redesigning the entire system.
- **Production-oriented** — The final architecture should support deployment on Google Cloud and demonstrate realistic engineering practices.

---

## 35. Project Status

CareerGraph AI is currently in active development.

Current milestone progression:

```
Domain Foundation
        ↓
Application Services
        ↓
API + Persistence
        ↓
End-to-End Workflow
        ↓
AI Integration
        ↓
Frontend
        ↓
GCP Deployment
```

The project is intentionally being developed incrementally with automated testing and static validation at each stage.

---

## 36. License

License information will be added before public release.

---

## 37. Author

**Shruti Sharma**

CareerGraph AI — AI-powered evidence-based career intelligence platform.
