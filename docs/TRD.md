# Technical Requirements Document (TRD)

# CareerGraph AI

**Project:** Patchamomma 2026 Build Phase  
**Document:** Technical Requirements Document  
**Version:** 0.1  
**Status:** Draft  
**Related Document:** [Business Requirements Document](./BRD.md)

---

# 1. Technical Overview

CareerGraph AI is a cloud-native, data-driven, multi-agent AI application designed to help Software Engineering candidates evaluate interview readiness, identify skill gaps, receive personalized preparation recommendations, and continuously measure improvement.

The system will connect:

- Candidate profile data
- Resume information
- Target role and level
- Job description requirements
- Skill assessments
- Interview responses
- Interview evaluations
- Skill-gap information
- Preparation history
- Progress data

The technical architecture will use Google Cloud and Google AI technologies as the primary platform.

The MVP will prioritize:

- A focused multi-agent architecture
- Evidence-based AI evaluation
- Structured candidate and job data
- Continuous readiness updates
- Cost-aware AI inference
- Serverless deployment
- Secure handling of candidate information

---

# 2. Technical Goals

The technical implementation should achieve the following goals:

## 2.1 AI Intelligence

- Use Gemini for generative AI capabilities.
- Use structured outputs wherever possible.
- Ground recommendations in candidate and assessment data.
- Avoid relying on unexplained AI-generated scores.
- Provide evidence supporting important evaluations.

## 2.2 Agentic Architecture

- Use Google ADK for meaningful agent orchestration.
- Use a small number of agents with clearly defined responsibilities.
- Avoid creating separate agents for simple deterministic operations.
- Maintain clear boundaries between agents and application logic.

## 2.3 Data-Driven Architecture

- Store candidate state in structured form.
- Maintain historical assessment and interview data.
- Support skill-level performance tracking.
- Enable analytics over time.
- Separate transactional application data from analytical workloads where appropriate.

## 2.4 Cloud-Native Deployment

The MVP should be deployable using Google Cloud services.

The architecture should prefer:

- Serverless infrastructure where practical.
- Managed services.
- Minimal infrastructure administration.
- Secure secret management.
- Cost monitoring.

## 2.5 Cost Efficiency

The system should be designed for the Patchamomma Build Phase free credits.

The implementation should:

- Minimize unnecessary Gemini calls.
- Use appropriate models for different tasks.
- Reuse previously extracted information.
- Avoid sending unnecessary context to models.
- Limit interview-session length.
- Monitor cloud and AI usage.
- Support budget alerts.

---

# 3. MVP Technical Scope

The MVP will implement the following technical capabilities.

## 3.1 Candidate Profile

The system should allow a candidate to create and maintain:

- Basic profile information
- Education
- Experience
- Skills
- Projects
- Technologies
- Target role
- Target level
- Target company

---

## 3.2 Resume Processing

The system should:

1. Accept a resume document.
2. Store the original document securely.
3. Extract relevant candidate information.
4. Convert extracted information into structured data.
5. Validate the structured output.
6. Store the resulting candidate profile.

---

## 3.3 Job Description Processing

The system should:

1. Accept a target job description.
2. Extract relevant requirements.
3. Identify required and preferred skills.
4. Identify role-level expectations.
5. Convert the information into structured target requirements.
6. Store the resulting target profile.

---

## 3.4 Skill Gap Analysis

The system should compare:

```text
Candidate Profile
        +
Candidate Evidence
        +
Target Role Requirements
        |
        v
Skill Gap Analysis
```
The output should include:

- Current capability
- Target capability
- Identified gap
- Priority
- Supporting evidence

## 3.5 Recommendation Engine

The system should generate a prioritized next-best action.

The recommendation should consider:

- Target role
- Target level
- Current skill profile
- Skill gaps
- Recent assessments
- Interview performance
- Previous recommendations
- Available evidence

The system should avoid producing an overwhelming list of generic recommendations.

## 3.6 Interview Simulation

The MVP will support:

- Coding interview
- Behavioral interview
- Representative system-design interview

The depth of implementation will differ.

| Module | Technical Scope |
|---|---|
| Coding | Deep implementation |
| Behavioral | Moderate implementation |
| System Design | Representative implementation |

## 3.7 Interview Evaluation

Interview responses should be evaluated using predefined rubrics.

The technical pipeline should be:
```text
Candidate Response
|
v
Evidence Extraction
|
v
Rubric Evaluation
|
v
Dimension Scores
|
v
Weighted Score
|
v
Skill Profile Update
```
The evaluation system should retain the evidence used to produce important scores.

## 3.8 Readiness Profile

The system should maintain an evolving readiness profile.

The profile may contain dimensions such as:

- DSA
- Coding
- Computer Science Fundamentals
- System Design
- Behavioral
- Communication

The exact dimensions and scoring methodology will be finalized in the Evaluation Framework.

## 3.9 Progress Analytics

The system should retain historical performance so that it can display:

- Skill progression
- Assessment progression
- Interview progression
- Repeated weaknesses
- Improvement trends
- Recommendation outcomes

## 4. High-Level System Architecture

The initial technical architecture is:
```text
                         USER
                           |
                           v
                    +--------------+
                    |   Frontend   |
                    |    Web App   |
                    +------+-------+
                           |
                           v
                    +--------------+
                    |   Backend    |
                    |   Cloud Run  |
                    +------+-------+
                           |
                           v
                 +--------------------+
                 | Agent Orchestrator |
                 +---------+----------+
                           |
          +----------------+----------------+
          |                |                |
          v                v                v
   +-------------+  +-------------+  +----------------+
   | Profile &   |  | Interviewer |  | Evaluation &   |
   | Requirement |  |    Agent    |  | Recommendation |
   |    Agent    |  |             |  |     Agent      |
   +------+------+  +------+------+  +-------+--------+
          |                |                 |
          +----------------+-----------------+
                           |
                           v
                    +--------------+
                    |    Gemini    |
                    +------+-------+
                           |
              +------------+------------+
              |                         |
              v                         v
       +-------------+           +-------------+
       |  Firestore  |           |  BigQuery   |
       | Application |           | Analytics   |
       |    Data     |           |    Data    |
       +-------------+           +-------------+
              |                         |
              +------------+------------+
                           |
                           v
                    +-------------+
                    |  Dashboard  |
                    +-------------+
```
This architecture is a working baseline.

The final architecture will be refined after defining:

- Agent workflows
- Data model
- Evaluation framework
- API contracts
- Security requirements
- Deployment requirements

## 5. Google Cloud Technology Stack

CareerGraph AI will prioritize Google and Google Cloud technologies.

The following stack is the initial technical direction.

| Requirement | Technology | Primary Purpose |
|---|---|---|
| Generative AI | Gemini | Extraction, reasoning, interview interaction and evaluation |
| Agentic AI | Google ADK | Agent orchestration and agent workflows |
| Application Backend | Cloud Run | Serverless backend deployment |
| Candidate/Application Data | Firestore | Transactional application data |
| Document Storage | Cloud Storage | Resume and document storage |
| Analytics | BigQuery | Historical and analytical data |
| Reporting | Looker Studio / Looker | Analytics and dashboards |
| Authentication | Firebase Authentication | User authentication |
| Event Processing | Pub/Sub | Asynchronous workflows where required |
| Database Agent Access | MCP Toolbox | Controlled database access for agents where justified |

Not every listed technology is required to be used in the MVP.

Each technology will be included only when it provides a clear technical benefit.

The final technology selection will be documented before implementation.

# 6. Multi-Agent Architecture

CareerGraph AI will use a focused multi-agent architecture built with Google ADK (Agent Development Kit).

The architecture will use a small number of specialized agents with clearly defined responsibilities rather than creating separate agents for every individual feature.

The primary objective is to ensure that each agent has a clear purpose, limited responsibility, and access only to the context and tools required for its task.

---

## 6.1 Agent Architecture

The initial MVP will consist of four core agent components:

```text
                         +----------------------+
                         |   Orchestrator Agent |
                         +----------+-----------+
                                    |
              +---------------------+---------------------+
              |                     |                     |
              v                     v                     v
   +-------------------+   +-------------------+   +-----------------------+
   | Profile &         |   | Interviewer       |   | Evaluation &          |
   | Requirement Agent |   | Agent             |   | Recommendation Agent  |
   +-------------------+   +-------------------+   +-----------------------+
              |                     |                     |
              +---------------------+---------------------+
                                    |
                                    v
                              Gemini Models
                                    |
                    +---------------+---------------+
                    |                               |
                    v                               v
               Firestore                       BigQuery
```
The four core components are:

- Orchestrator Agent
- Profile & Requirement Agent
- Interviewer Agent
- Evaluation & Recommendation Agent

## 6.2 Orchestrator Agent

The Orchestrator Agent is responsible for coordinating the overall agent workflow.

### Responsibilities

- Understand the user's current task or workflow state.
- Determine which specialized agent should handle the request.
- Provide relevant context to the selected agent.
- Coordinate sequential or conditional agent execution.
- Maintain workflow state.
- Handle transitions between profile analysis, interview, evaluation, and recommendation workflows.
- Return structured results to the application layer.

### Example
```text
User uploads Resume
|
v
Orchestrator Agent
|
v
Profile & Requirement Agent
|
v
Candidate Profile
```
After an interview:
```text
Interview Completed
        |
        v
Orchestrator Agent
        |
        v
Evaluation & Recommendation Agent
```
### Constraints

The Orchestrator Agent should not independently perform specialized analysis when an appropriate specialized agent is available.

Its primary responsibility is coordination rather than becoming a general-purpose agent that performs every task.

## 6.3 Profile & Requirement Agent

The Profile & Requirement Agent is responsible for converting unstructured candidate and job information into structured representations.

### Responsibilities

**Candidate-side processing**

- Analyze uploaded resumes.
- Extract education information.
- Extract professional experience.
- Extract technical skills.
- Extract projects.
- Extract technologies.
- Identify evidence supporting claimed skills.
- Build a structured candidate profile.

**Job-side processing**

- Analyze job descriptions.
- Extract required skills.
- Extract preferred skills.
- Identify role expectations.
- Identify experience requirements.
- Identify relevant technical competencies.
- Build a structured target-role profile.

### Comparison

The agent can compare:
```text
Candidate Profile
        +
Target Role Profile
        |
        v
Potential Skill Gaps
```
### Constraints

The agent should distinguish between:

- Explicit evidence
- Inferred information
- Missing information

The system should avoid treating unsupported assumptions as confirmed candidate skills.

## 6.4 Interviewer Agent

The Interviewer Agent is responsible for conducting interactive interview sessions.

The MVP will support representative interview experiences across:

- Coding
- Behavioral
- System Design

### Responsibilities

- Start an interview session.
- Select or generate appropriate questions.
- Maintain interview context.
- Ask follow-up questions when required.
- Adapt difficulty based on the interview flow.
- Collect candidate responses.
- Maintain session state.
- End the interview according to the defined session rules.
- Pass completed interview information to the evaluation workflow.

### Example
```text
Candidate starts Coding Interview
        |
        v
Interviewer Agent
        |
        v
Question 1
        |
        v
Candidate Response
        |
        v
Follow-up / Question 2
        |
        v
Interview Completed
```
### Constraints

The Interviewer Agent should focus on conducting the interview.

It should not independently determine the final candidate readiness score.

Evaluation should be handled by the Evaluation & Recommendation Agent using the defined evaluation framework.

## 6.5 Evaluation & Recommendation Agent

The Evaluation & Recommendation Agent is responsible for converting interview and assessment evidence into structured evaluation and actionable recommendations.

### Responsibilities

- Analyze candidate responses.
- Extract relevant evidence.
- Apply predefined evaluation rubrics.
- Evaluate individual competency dimensions.
- Generate structured scores.
- Identify strengths.
- Identify weaknesses.
- Update the candidate's skill profile.
- Identify priority skill gaps.
- Generate the next best preparation action.

### Evaluation Flow

```text
Candidate Response
        |
        v
Evidence Extraction
        |
        v
Evaluation Rubric
        |
        v
Dimension-level Evaluation
        |
        v
Structured Score
        |
        v
Skill Profile Update
        |
        v
Next Best Action
```
### Constraints

The agent should not produce unsupported numerical scores.

Scores should be associated with:

- Evaluation dimensions
- Evidence
- Rubric criteria
- Relevant candidate response

The detailed scoring methodology will be defined in the Evaluation Framework section of this TRD.

## 6.6 Agent Responsibility Matrix

| Agent | Primary Responsibility | Input | Output |
|---|---|---|---|
| Orchestrator Agent | Workflow coordination | User request, workflow state | Agent task / workflow result |
| Profile & Requirement Agent | Candidate and job understanding | Resume, job description, profile data | Structured profiles and requirements |
| Interviewer Agent | Conduct interview | Candidate profile, target role, interview type | Questions, responses, interview session |
| Evaluation & Recommendation Agent | Evaluate performance and recommend next actions | Interview responses, assessment data, rubrics | Evaluation, skill updates, recommendations |

## 6.7 Agent Communication

Agents should communicate through structured data rather than relying on free-form textual handoffs wherever practical.

Example:
```text
Profile & Requirement Agent
            |
            v
Structured Candidate Profile
            |
            v
Orchestrator
            |
            v
Interviewer Agent
```
A structured candidate profile may contain:

Candidate Profile
├── Skills
├── Experience
├── Education
├── Projects
├── Technologies
├── Target Role
├── Target Level
└── Evidence

Structured outputs will improve:

- Reliability
- Validation
- Debugging
- Observability
- Data persistence
- Agent interoperability

## 6.8 Agent Boundaries

The system will maintain clear boundaries between agent responsibilities.

| Responsibility | Owner |
|---|---|
| Workflow coordination | Orchestrator Agent |
| Resume understanding | Profile & Requirement Agent |
| Job description understanding | Profile & Requirement Agent |
| Candidate/job comparison | Profile & Requirement Agent |
| Interview interaction | Interviewer Agent |
| Evidence extraction from responses | Evaluation & Recommendation Agent |
| Rubric-based evaluation | Evaluation & Recommendation Agent |
| Skill profile updates | Evaluation & Recommendation Agent |
| Next-best-action recommendation | Evaluation & Recommendation Agent |
| Data persistence | Application / Database Layer |
| Authentication | Application / Identity Layer |
| Deterministic business rules | Application Layer |

Agents should not directly perform responsibilities that belong to the application or infrastructure layer unless explicitly required by the architecture.

## 6.9 Agent Design Principles

The multi-agent architecture will follow these principles:

1. **Specialization** — Each agent should have a clearly defined purpose.
2. **Minimalism** — New agents should be introduced only when there is a meaningful separation of responsibility.
3. **Structured Communication** — Agents should exchange structured information whenever possible.
4. **Evidence-Based Reasoning** — Important evaluations and recommendations should be grounded in available candidate evidence.
5. **Deterministic Logic Outside Agents** — Simple calculations, validation, database operations, authentication, and other deterministic operations should remain in the application layer where practical.
6. **Controlled Tool Access** — Agents should receive access only to the tools and data required for their responsibilities.
7. **Observability** — Agent executions should be traceable for debugging, evaluation, and system monitoring.
8. **Cost Awareness** — Agent workflows should minimize unnecessary model calls and excessive context.
9. **Failure Isolation** — Failure of one agent should not unnecessarily bring down the entire application workflow.
10. **Extensibility** — The architecture should allow additional specialized agents to be introduced in future versions without requiring a complete redesign.

## 6.10 Future Agent Extensions

Additional specialized agents may be introduced after MVP validation.

Potential future agents include:

- Learning & Resource Agent
- Career Intelligence Agent
- Resume Optimization Agent
- Job Discovery Agent
- Analytics Agent

These agents are intentionally outside the initial MVP architecture unless a clear technical requirement emerges during implementation.

The MVP will prioritize depth and reliability of the four core agents over the number of agents.
