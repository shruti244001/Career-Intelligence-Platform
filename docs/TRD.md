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
