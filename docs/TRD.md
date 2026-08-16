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
```text
Candidate Profile
├── Skills
├── Experience
├── Education
├── Projects
├── Technologies
├── Target Role
├── Target Level
└── Evidence
```
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

# 7. Agent Responsibilities, Tools & Interfaces

This section defines the operational responsibilities, inputs, outputs, tool access, and boundaries of each agent in the CareerGraph AI MVP.

Each agent should have a clearly defined contract describing:

- What information it receives.
- What tasks it performs.
- Which tools it can access.
- What information it produces.
- Which agent or application component receives its output.
- What the agent is explicitly not responsible for.

The goal is to maintain a controlled, testable, and explainable agentic architecture.

---

## 7.1 Agent Interface Model

The general interaction pattern is:

```text
User / Application
        |
        v
Orchestrator Agent
        |
        v
Specialized Agent
        |
        +----> Gemini
        |
        +----> Approved Tools
        |
        v
Structured Output
        |
        v
Orchestrator / Application Layer
        |
        v
Database / User Interface
```
Agents should not communicate through arbitrary free-form instructions when a structured contract can be used.

## 7.2 Orchestrator Agent

### Purpose

The Orchestrator Agent coordinates CareerGraph workflows and delegates tasks to specialized agents.

### Inputs

The Orchestrator may receive:

- User request
- User identity
- Current workflow
- Candidate ID
- Target role
- Target level
- Current application state
- Results from previously executed agents

### Responsibilities

- Identify the required workflow.
- Determine which specialized agent should execute the next task.
- Pass only relevant context to the selected agent.
- Maintain workflow state.
- Coordinate sequential agent execution.
- Handle successful and unsuccessful agent execution.
- Return the final structured result to the application layer.

### Tool Access

The Orchestrator may have access to:

- Agent invocation tools
- Workflow/state management
- Candidate context retrieval
- Application-level service interfaces

The Orchestrator should not have unrestricted access to every database collection or service.

### Output

The Orchestrator should produce a structured workflow result.

Example:

```json
{
  "workflow": "skill_gap_analysis",
  "status": "completed",
  "next_action": "generate_recommendation",
  "agent_result": {
    "agent": "profile_requirement_agent",
    "result_id": "result_123"
  }
}
```

### Explicitly Out of Scope

The Orchestrator should not:

- Conduct the interview itself.
- Perform detailed resume extraction.
- Perform detailed job-description extraction.
- Assign final interview scores.
- Replace the evaluation agent.
- Implement deterministic business rules that belong in the application layer.

## 7.3 Profile & Requirement Agent

### Purpose

The Profile & Requirement Agent converts candidate and job information into structured representations.

### Inputs

The agent may receive:

- Resume document
- Candidate profile
- Job description
- Target role
- Target level
- Existing candidate skill information

### Responsibilities

**Resume Processing**

- Extract candidate information.
- Identify technical skills.
- Identify experience.
- Identify projects.
- Identify education.
- Identify technologies.
- Identify supporting evidence.

**Job Description Processing**

- Extract required skills.
- Extract preferred skills.
- Identify role expectations.
- Identify experience requirements.
- Identify technical competencies.

### Profile Comparison

When requested, the agent can compare:
```text
Candidate Profile
        +
Target Role Requirements
        |
        v
Skill Gap Candidates
```
### Tool Access

The agent may access:

- Resume/document retrieval service
- Candidate profile retrieval
- Job-description retrieval
- Gemini
- Structured-output validation

The agent should not directly modify unrelated application data.

### Output

The agent should return structured information.

Example:

```json
{
  "candidate_profile": {
    "skills": [
      {
        "name": "Python",
        "evidence": [
          "Professional experience",
          "Project experience"
        ]
      }
    ],
    "experience": [],
    "education": [],
    "projects": []
  }
}
```

A target-role analysis may return:

```json
{
  "target_role": {
    "role": "Software Engineer",
    "level": "SDE-1",
    "required_skills": [
      "Data Structures",
      "Algorithms",
      "Python",
      "Object-Oriented Programming"
    ],
    "preferred_skills": [
      "Cloud",
      "System Design"
    ]
  }
}
```

### Explicitly Out of Scope

The agent should not:

- Conduct interviews.
- Assign interview performance scores.
- Generate final readiness scores.
- Make unsupported claims about candidate capability.
- Automatically declare a candidate job-ready.

## 7.4 Interviewer Agent

### Purpose

The Interviewer Agent conducts an interactive interview session based on the candidate's target role and selected interview type.

### Inputs

The agent may receive:

- Candidate profile
- Target role
- Target level
- Interview type
- Relevant skills
- Previous interview context
- Current interview state

### Responsibilities

- Initialize an interview session.
- Select an appropriate question.
- Present the question to the candidate.
- Maintain interview context.
- Ask follow-up questions when appropriate.
- Adjust difficulty within defined limits.
- Track questions asked.
- Track candidate responses.
- Determine when the interview session should end.
- Pass the completed session to the evaluation workflow.

### Supported Interview Types

The MVP will support:

- Coding
- Behavioral
- System Design

The depth of each interview type will depend on the MVP implementation scope.

### Tool Access

The Interviewer Agent may access:

- Candidate profile
- Target role requirements
- Interview question repository
- Interview session state
- Gemini
- Approved interview-related tools

### Output

The agent should produce structured interview events.

Example:

```json
{
  "session_id": "session_123",
  "interview_type": "coding",
  "question_id": "coding_001",
  "question": "Two Sum",
  "response": {
    "text": "..."
  },
  "status": "in_progress"
}
```

At completion:

```json
{
  "session_id": "session_123",
  "status": "completed",
  "questions_attempted": 3,
  "responses": [
    {
      "question_id": "coding_001",
      "response": "..."
    }
  ]
}
```

### Explicitly Out of Scope

The Interviewer Agent should not:

- Produce the final interview score.
- Modify the candidate's permanent skill profile directly.
- Generate final readiness decisions.
- Override evaluation rubrics.

## 7.5 Evaluation & Recommendation Agent

### Purpose

The Evaluation & Recommendation Agent evaluates candidate performance using predefined rubrics and converts the results into actionable preparation recommendations.

### Inputs

The agent may receive:

- Interview session
- Candidate responses
- Interview questions
- Target role
- Target level
- Relevant competency definitions
- Evaluation rubric
- Previous performance data

### Responsibilities

**Evidence Extraction**

Identify evidence from the candidate's response that is relevant to the evaluation criteria.

**Evaluation**

Evaluate the candidate against predefined dimensions.

**Skill Update**

Identify whether the evidence supports:

- Strength
- Weakness
- Improvement
- Insufficient evidence

**Recommendation**

Generate a prioritized next-best action based on:

- Skill gap
- Recent performance
- Target role
- Target level
- Historical performance

### Tool Access

The agent may access:

- Interview session data
- Candidate skill profile
- Evaluation rubrics
- Historical assessment data
- Gemini
- Recommendation service
- Structured-output validation

### Output

Example:

```json
{
  "evaluation": {
    "session_id": "session_123",
    "dimensions": [
      {
        "dimension": "Problem Solving",
        "score": 3,
        "max_score": 5,
        "evidence": [
          "Identified an efficient approach",
          "Explained time complexity"
        ]
      }
    ]
  },
  "skill_updates": [
    {
      "skill": "Data Structures",
      "change": "needs_improvement"
    }
  ],
  "recommendation": {
    "priority": "high",
    "action": "Practice medium-level array and hashing problems",
    "reason": "Recent coding evaluation identified weaknesses in problem decomposition."
  }
}
```

### Explicitly Out of Scope

The agent should not:

- Conduct the interview.
- Modify unrelated candidate information.
- Generate unsupported scores.
- Make claims about actual hiring probability.
- Replace a human hiring decision.

## 7.6 Tool Access Matrix

Agent tool access should follow the principle of least privilege.

| Tool / Resource | Orchestrator | Profile & Requirement | Interviewer | Evaluation & Recommendation |
|---|---|---|---|---|
| Gemini | Yes | Yes | Yes | Yes |
| Candidate Profile Read | Limited | Yes | Yes | Yes |
| Candidate Profile Write | No | Controlled | No | Controlled |
| Resume Storage Read | No | Yes | No | No |
| Job Description Read | Limited | Yes | Yes | Yes |
| Interview State Read | Limited | No | Yes | Yes |
| Interview State Write | No | No | Yes | Controlled |
| Evaluation Rubric Read | No | No | Limited | Yes |
| Historical Assessment Read | Limited | No | Limited | Yes |
| Recommendation Write | No | No | No | Yes |
| Analytics Data | No | No | No | Controlled |

The exact implementation of these permissions will be finalized during the security and application architecture design.

## 7.7 Structured Agent Contracts

Each agent should have a defined input and output contract.

The preferred pattern is:
```text
Input
  ↓
Validation
  ↓
Agent Execution
  ↓
Structured Output
  ↓
Output Validation
  ↓
Persistence / Next Agent
```
Structured outputs should be validated before being persisted or passed to another component.

Invalid or incomplete outputs should trigger an appropriate retry, fallback, or error-handling workflow.

## 7.8 Agent Context Management

Agents should receive only the context required for the current task.

The system should avoid sending the entire candidate history to every model call.

Context should be selected based on:

- Current workflow
- Target role
- Target level
- Relevant skills
- Recent assessments
- Relevant interview history
- Required evaluation criteria

This approach is intended to improve:

- Model reliability
- Response quality
- Latency
- Cost efficiency
- Privacy

## 7.9 Deterministic vs. Agentic Responsibilities

Not every system operation requires an AI agent.

The architecture should use deterministic application logic for tasks such as:

- Input validation
- Authentication
- Authorization
- Database writes
- Database reads
- Score calculations where formulas are predefined
- Threshold checks
- Session management
- Rate limiting
- Error handling
- Cost controls

Agents should primarily be used for tasks requiring:

- Natural language understanding
- Reasoning
- Interpretation
- Adaptive interaction
- Evidence extraction
- Contextual recommendations

This separation is intended to make the system more reliable, testable, and explainable.

## 7.10 Agent Failure Handling

Agent failures should not automatically terminate the entire application.

Potential failure cases include:

- Invalid model output
- Missing required fields
- Model timeout
- API failure
- Tool failure
- Insufficient candidate information
- Inconsistent agent output

The system should support appropriate recovery mechanisms such as:

- Output validation
- Retry with controlled limits
- Fallback responses
- Workflow interruption with user notification
- Logging and observability
- Manual review for critical failures where appropriate

Detailed failure-handling behavior will be defined in the Reliability section of this TRD.

## 7.11 Agent Observability

Each agent execution should produce traceable metadata where technically feasible.

Potential metadata includes:

- Agent name
- Workflow ID
- Session ID
- Execution timestamp
- Input reference
- Output status
- Tool calls
- Model used
- Error status
- Latency
- Token usage where available

Sensitive candidate content should not be unnecessarily written to logs.

Detailed observability requirements will be defined later in this TRD.

## 7.12 Agent Extensibility

The architecture should allow additional specialized agents to be introduced without redesigning the entire system.

Future agents may include:

- Learning & Resource Agent
- Resume Optimization Agent
- Career Intelligence Agent
- Job Discovery Agent
- Analytics Agent

These agents will only be introduced when a clear product or technical requirement justifies their inclusion.

The MVP will prioritize reliability and depth of the four core agents over increasing the number of agents.

# 8. Agent Workflows

CareerGraph AI will use coordinated agent workflows to transform candidate information into personalized preparation actions and continuously update the candidate's preparation profile based on new evidence.

The core workflow is designed as a continuous feedback loop:

```text
Candidate Profile
        +
Target Profile
        |
        v
Skill Gap Analysis
        |
        v
Next Best Action
        |
        v
Preparation / Interview
        |
        v
Performance Evidence
        |
        v
Evaluation
        |
        v
Skill Profile Update
        |
        +--------------------+
        |                    |
        v                    |
Updated Skill Gaps           |
        |                    |
        v                    |
Next Best Action <-----------+
```
The MVP will implement three primary workflows:

1. Target Profile and Skill Gap Workflow
2. Personalized Next Best Action Workflow
3. Interview, Evaluation and Skill Update Workflow

## 8.1 Workflow 1 — Target Profile and Skill Gap Analysis

### Objective

Convert the candidate's background and target career requirements into a structured target profile and identify the most important skill gaps.

### Inputs

The workflow may use:

- Candidate profile
- Resume
- Target role
- Target level
- Target company, if provided
- Target job description, if provided
- Existing candidate skill evidence
- Previous assessment history, if available

### Workflow
```text
Candidate
    |
    v
Resume / Profile
    |
    v
Orchestrator Agent
    |
    v
Profile & Requirement Agent
    |
    +----------------------+
    |                      |
    v                      v
Candidate Profile     Target Requirements
                           |
                           v
                    Target Profile
                           |
                           v
                    Skill Gap Analysis
                           |
                           v
                    Structured Gap Result
```
### Step 1 — Candidate Profile Processing

The Profile & Requirement Agent analyzes available candidate information.

The system may extract:

- Education
- Experience
- Skills
- Projects
- Technologies
- Existing evidence of competency

The extracted information should be represented in a structured format.

### Step 2 — Target Requirement Processing

The Profile & Requirement Agent analyzes the target requirements.

The baseline target is determined using:
```text
Target Role
+
Target Level
```
Optional information can further refine the target:
```text
Target Company
+
Target Job Description
```
The resulting target profile should contain relevant competency expectations.

### Step 3 — Candidate vs. Target Comparison

The system compares the candidate profile against the target profile.

Example:

| Target Competency | Candidate Evidence |
|---|---|
| Data Structures | Moderate |
| Algorithms | Moderate |
| Graphs | Weak |
| Dynamic Programming | Weak |
| OOP | Strong |
| System Design | Beginner |
| Behavioral | Insufficient Evidence |

### Step 4 — Skill Gap Identification

The system identifies gaps based on available evidence.

Each gap should contain:

- Skill / competency
- Current evidence
- Target expectation
- Gap status
- Confidence
- Priority

Example:

```json
{
  "skill": "Graphs",
  "current_level": "weak",
  "target_level": "high",
  "gap_status": "needs_improvement",
  "priority": "high",
  "confidence": 0.86
}
```

The confidence value represents confidence in the available evidence and should not be interpreted as hiring probability.

### Step 5 — Persist Result

The structured target profile and skill-gap result should be stored for future workflows.

The result can subsequently be used by:

- Recommendation workflows
- Interview workflows
- Evaluation workflows
- Progress tracking
- Dashboard analytics

## 8.2 Workflow 2 — Personalized Next Best Action

### Objective

Determine what the candidate should do next based on the current target profile, skill gaps, and available performance evidence.

The system should not simply generate a static roadmap.

Instead, it should prioritize the next action dynamically.

### Inputs

The workflow may use:

- Target profile
- Current skill gaps
- Skill priorities
- Recent assessments
- Interview performance
- Preparation history
- Previous recommendations
- Target role
- Target level

### Workflow
```text
Current Candidate State
        |
        v
Orchestrator Agent
        |
        v
Evaluation & Recommendation Agent
        |
        +-------------------+
        |                   |
        v                   v
Skill Gaps             Recent Evidence
        |                   |
        +---------+---------+
                  |
                  v
          Priority Analysis
                  |
                  v
          Next Best Action
                  |
                  v
             Candidate
```
### Step 1 — Collect Current State

The system retrieves the candidate's latest available evidence.

This may include:

- Current skill levels
- Recent assessment results
- Interview results
- Previously completed actions
- Outstanding skill gaps

### Step 2 — Prioritize Gaps

The system determines which competency should receive attention first.

Potential prioritization factors include:

- Severity of skill gap
- Importance to target role
- Importance to target level
- Evidence from recent assessments
- Recency of performance
- Previous unsuccessful attempts
- Candidate preparation history

The prioritization logic should be explainable.

### Step 3 — Generate Next Best Action

The Evaluation & Recommendation Agent generates an actionable recommendation.

Examples:

> **High Priority:** Practice medium-level graph traversal problems.
>
> **Reason:** Recent coding performance indicates difficulty with BFS/DFS while graph competency is important for the selected target profile.

or:

> **High Priority:** Complete a behavioral interview session focused on ownership.
>
> **Reason:** The candidate has insufficient evidence for the ownership competency required by the selected target profile.

The recommendation should be specific enough for the candidate to act on.

### Step 4 — Store Recommendation

The recommendation should be stored as part of the candidate's preparation history.

The system should track:

- Recommended action
- Reason
- Priority
- Related competency
- Creation timestamp
- Completion status
- Result, when available

## 8.3 Workflow 3 — Interview, Evaluation and Skill Update

### Objective

Conduct an interview, evaluate the candidate using predefined rubrics, update the candidate's competency evidence, and generate the next best action.

This workflow creates the primary feedback loop of CareerGraph AI.

### Inputs

The workflow may use:

- Candidate profile
- Target profile
- Target role
- Target level
- Interview type
- Interview configuration
- Evaluation rubric
- Previous relevant performance

### Workflow
```text
Candidate
    |
    v
Start Interview
    |
    v
Orchestrator Agent
    |
    v
Interviewer Agent
    |
    v
Questions / Follow-ups
    |
    v
Candidate Responses
    |
    v
Interview Completed
    |
    v
Evaluation & Recommendation Agent
    |
    +-----------------------+
    |                       |
    v                       v
Evidence Extraction      Rubric
    |                       |
    +-----------+-----------+
                |
                v
        Competency Evaluation
                |
                v
         Skill Profile Update
                |
                v
         Updated Skill Gaps
                |
                v
        Next Best Action
```
## 8.4 Interview Initialization

The Orchestrator Agent receives the interview request.

Example:
```text
Interview Type:
Coding

Target Role:
Software Engineer

Target Level:
SDE-1

Target Company:
Optional

Job Description:
Optional
```
The Orchestrator retrieves the relevant target context and invokes the Interviewer Agent.

## 8.5 Interview Execution

The Interviewer Agent conducts the interview.

The interview may contain:

- Initial question
- Candidate response
- Follow-up question
- Additional candidate response
- Difficulty adjustment where appropriate
- Interview completion

The agent maintains the session state throughout the interview.

Example:
```text
Question
   |
   v
Candidate Response
   |
   v
Interviewer Analysis
   |
   +----> Follow-up required
   |             |
   |             v
   |        Follow-up Question
   |
   +----> Continue
                 |
                 v
           Next Question
```
The Interviewer Agent should focus on conducting the interview rather than assigning the final evaluation.

## 8.6 Interview Evidence Collection

After the interview, the system should retain structured evidence.

Potential evidence includes:

- Questions presented
- Candidate responses
- Follow-up questions
- Time-related information where available
- Candidate approach
- Candidate explanation
- Final solution or response
- Interview type
- Target competency

The raw candidate response and derived evaluation should remain distinguishable.

## 8.7 Rubric-Based Evaluation

The completed interview is passed to the Evaluation & Recommendation Agent.

The evaluation should be based on predefined competency dimensions.

Example for a coding interview:
```text
Coding Interview
├── Problem Understanding
├── Problem Solving
├── Algorithm Selection
├── Correctness
├── Complexity Analysis
├── Communication
└── Code Quality
```
Example for a behavioral interview:
```text
Behavioral Interview
├── Communication
├── Ownership
├── Collaboration
├── Conflict Handling
├── Decision Making
└── Impact
```
Example for a system design interview:
```text
System Design Interview
├── Requirement Understanding
├── Architecture
├── Scalability
├── Reliability
├── Data Design
├── Trade-offs
└── Communication
```
The exact rubric dimensions may vary according to the selected interview type and target level.

## 8.8 Evidence-Based Scoring

Evaluation should follow:
```text
Candidate Response
        |
        v
Relevant Evidence
        |
        v
Rubric Criteria
        |
        v
Dimension Evaluation
        |
        v
Structured Score
```
The system should avoid producing unexplained scores.

Each evaluation dimension should, where possible, contain:

- Score
- Maximum score
- Evidence
- Strength
- Improvement area

Example:

```json
{
  "dimension": "Problem Solving",
  "score": 3,
  "max_score": 5,
  "evidence": [
    "Identified a valid approach",
    "Required assistance to optimize the solution"
  ],
  "improvement_area": "Practice identifying optimal approaches independently"
}
```

## 8.9 Skill Profile Update

After evaluation, the system determines whether the new evidence should modify the candidate's competency profile.

Example:
```text
Before Interview

Graphs
Current Evidence: Weak


        ↓


Interview Performance

Candidate struggled with BFS traversal


        ↓


After Evaluation

Graphs
Status: Needs Improvement
Priority: High
Evidence Count: Updated
```
The system should preserve historical assessment information rather than overwriting previous evidence without traceability.

## 8.10 Next Best Action After Interview

The updated skill profile is passed into the recommendation workflow.

Example:
```text
Interview Result
      |
      v
Graph competency identified as weak
      |
      v
Target role requires strong problem solving
      |
      v
Priority increases
      |
      v
Recommendation:
Practice BFS/DFS problems
      |
      v
Candidate completes action
      |
      v
Future assessment
```
This creates a continuous preparation loop rather than treating each mock interview as an isolated event.

## 8.11 End-to-End CareerGraph Loop

The three workflows combine into the core product loop:
```text
             ┌───────────────────────┐
             │   Candidate Profile   │
             └───────────┬───────────┘
                         |
                         v
             ┌───────────────────────┐
             │    Target Profile     │
             │                       │
             │ Role + Level          │
             │ + Company (optional)  │
             │ + JD (optional)       │
             └───────────┬───────────┘
                         |
                         v
             ┌───────────────────────┐
             │    Skill Gap          │
             │      Analysis         │
             └───────────┬───────────┘
                         |
                         v
             ┌───────────────────────┐
             │   Next Best Action    │
             └───────────┬───────────┘
                         |
                         v
             ┌───────────────────────┐
             │ Preparation /         │
             │ Mock Interview        │
             └───────────┬───────────┘
                         |
                         v
             ┌───────────────────────┐
             │ Performance Evidence │
             └───────────┬───────────┘
                         |
                         v
             ┌───────────────────────┐
             │ Rubric-Based         │
             │ Evaluation            │
             └───────────┬───────────┘
                         |
                         v
             ┌───────────────────────┐
             │ Skill Profile Update  │
             └───────────┬───────────┘
                         |
                         v
             ┌───────────────────────┐
             │ Updated Skill Gaps    │
             └───────────┬───────────┘
                         |
                         └───────────────> Next Best Action
```
## 8.12 Workflow State

Each workflow should maintain a defined state.

Example:
```text
Workflow State

CREATED
   ↓
IN_PROGRESS
   ↓
WAITING_FOR_USER
   ↓
PROCESSING
   ↓
COMPLETED
```
Error states may include:

- `FAILED`
- `CANCELLED`
- `RETRYING`

The exact state machine may be refined during implementation.

## 8.13 Workflow Persistence

Important workflow state should be persisted so that a candidate can resume an incomplete workflow.

Potential persisted information includes:

- Workflow ID
- Candidate ID
- Workflow type
- Current state
- Target profile reference
- Agent execution references
- Interview session reference
- Evaluation reference
- Recommendation reference
- Timestamps
- Error status where applicable

The system should avoid storing unnecessary duplicate copies of large model responses.

## 8.14 Workflow Error Handling

If an agent fails during a workflow, the system should:

- Record the failure.
- Identify whether the operation is safely retryable.
- Retry within a controlled limit where appropriate.
- Preserve the existing workflow state.
- Avoid duplicating persisted records.
- Notify the user when the workflow cannot continue.
- Allow the workflow to resume where technically feasible.

Example:
```text
Interviewer Agent
       |
       X
   API Failure
       |
       v
Retry
       |
       +----> Success → Continue
       |
       +----> Failure → Preserve State → Notify User
```
## 8.15 Workflow Design Principles

The workflows should follow these principles:

1. Each workflow should have a clearly defined objective.
2. Agent responsibilities should remain separated.
3. Structured data should be used for agent handoffs.
4. Important evaluation decisions should be evidence-based.
5. Candidate history should be preserved.
6. The system should avoid unnecessary model calls.
7. Deterministic operations should remain outside agents where practical.
8. Workflows should be observable and traceable.
9. Failed workflows should be recoverable where possible.
10. The architecture should support future expansion without requiring a complete redesign.

## 8.16 MVP Workflow Boundaries

The MVP will prioritize the following complete workflow:
```text
Target Profile
      ↓
Skill Gap
      ↓
Next Best Action
      ↓
Interview
      ↓
Evaluation
      ↓
Skill Update
      ↓
Next Best Action
```
The MVP should prioritize making this loop functional and reliable rather than implementing a large number of independent workflows.

Additional workflows and specialized agents may be introduced after the core loop is validated.
# 9. Data Architecture & Database Schema

CareerGraph AI is a data-driven system. The data architecture should connect candidate information, target requirements, preparation activity, assessment evidence, interview performance, and recommendations into a unified candidate intelligence model.

The database design should support:

- Candidate profile management.
- Target role and level definition.
- Optional company-specific targeting.
- Job description analysis.
- Skill and competency tracking.
- Skill-gap identification.
- Preparation recommendations.
- Interview sessions.
- Interview questions and responses.
- Rubric-based evaluations.
- Evidence-based skill updates.
- Progress tracking.
- Historical performance analysis.

The data model should preserve historical evidence rather than continuously overwriting previous results.

---

## 9.1 Data Architecture Principles

The data architecture should follow these principles:

- Use structured data for core candidate and application state.
- Store raw and derived information separately where practical.
- Preserve historical assessment and interview evidence.
- Maintain relationships between skills, evidence, assessments and recommendations.
- Avoid storing unnecessary duplicate model outputs.
- Use stable identifiers for major entities.
- Support future analytics and progress tracking.
- Keep personally identifiable information to the minimum required for the MVP.
- Do not store confidential employer data or proprietary interview material.
- Separate candidate-specific data from reusable reference data.

---

## 9.2 High-Level Data Model

The conceptual data relationship is:

```text
                    Candidate
                        |
                        v
                 Candidate Profile
                        |
                        v
                  Target Profile
                  /      |       \
                 /       |        \
                v        v         v
             Role      Level    Company
                \       |        /
                 \      |       /
                  \     |      /
                   v    v     v
                  Target Requirements
                         |
                         v
                   Skill / Competency
                         |
              +----------+----------+
              |                     |
              v                     v
         Candidate Evidence     Skill Gap
              |                     |
              v                     v
       Assessment History     Recommendation
              |
              v
       Interview Sessions
              |
              v
          Questions
              |
              v
          Responses
              |
              v
          Evaluation
              |
              v
       Updated Evidence
              |
              v
        Updated Skill Gap
              |
              v
       Next Best Action
```
The architecture should allow new evidence to update the candidate's current state while preserving historical records.

## 9.3 Core Entities
The MVP will use the following conceptual entities:

| Entity | Purpose |
|---|---|
| Candidate | Represents the user of the platform |
| Candidate Profile | Stores education, experience, skills and background |
| Target Profile | Represents the candidate's desired career target |
| Role | Defines the target Software Engineering role |
| Level | Defines expected seniority such as SDE-1, SDE-2 or SDE-3 |
| Company | Optional target company |
| Job Description | Optional target job description |
| Competency | Represents a measurable technical or behavioral capability |
| Skill Evidence | Represents evidence demonstrating candidate capability |
| Skill Gap | Represents the difference between current evidence and target expectation |
| Preparation Action | Represents a recommended preparation activity |
| Assessment | Represents a structured evaluation |
| Interview Session | Represents one mock interview |
| Interview Question | Represents a question used during an interview |
| Interview Response | Represents the candidate's response |
| Evaluation | Represents rubric-based assessment of performance |
| Recommendation | Represents the next best action generated by the system |
| Workflow | Represents an agentic workflow execution |
| Agent Execution | Represents an individual agent execution within a workflow |

---
### 9.4 Candidate Entity
The Candidate entity represents the platform user.

Example conceptual structure:
```json
{
  "candidate_id": "candidate_001",
  "created_at": "timestamp",
  "updated_at": "timestamp",
  "status": "active"
}
```
The Candidate entity should contain only information necessary to identify and manage the user's platform account.

Sensitive information should not be stored unless required by the application.
### 9.5 Candidate Profile

The Candidate Profile contains information used to understand the candidate's current background.

Potential fields:

- `candidate_profile_id`
- `candidate_id`
- `education`
- `experience`
- `skills`
- `projects`
- `technologies`
- `resume_reference`
- `created_at`
- `updated_at`

> Resume files should be stored in appropriate object storage rather than directly inside the database. The database should store a reference to the uploaded document and its structured extraction.

### 9.6 Target Profile

The Target Profile represents where the candidate wants to reach.

```
Target Role + Target Level + Optional Target Company + Optional Job Description
```

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

> The target profile should contain or reference the expected competencies for the selected target.

### 9.7 Role and Level Reference Data

Role and level information should be represented separately from individual candidate records where practical.

```
Role
└── Software Engineer

Levels
├── SDE-1
├── SDE-2
└── SDE-3
```

Each level can have different expected competency profiles:

```
SDE-1                       SDE-2                     SDE-3
├── Coding / DSA            ├── Coding / DSA           ├── Advanced Problem Solving
├── Problem Solving         ├── Problem Solving        ├── System Design
├── CS Fundamentals         ├── System Design          ├── Architecture
├── Basic System Design     ├── Architecture           ├── Technical Leadership
└── Behavioral              ├── Ownership               ├── Ownership
                            └── Behavioral              └── Behavioral
```

> These are reference expectations and should not be treated as universal hiring criteria for every company.
