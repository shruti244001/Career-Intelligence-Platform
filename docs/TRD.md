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
