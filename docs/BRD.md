# Business Requirements Document (BRD)

# CareerGraph AI

**Working Product Name:** CareerGraph AI  
**Project:** Patchamomma 2026 Build Phase  
**Document:** Business Requirements Document  
**Version:** 0.3  
**Date:** 16 August 2026  
**Status:** Draft - Refined MVP  
**Repository:** Career-Intelligence-Platform

---

# 1. Executive Summary

CareerGraph AI is a data-driven, multi-agent AI platform designed to help Software Engineering candidates understand their current interview readiness, identify their highest-impact skill gaps, prepare strategically, and continuously measure whether their preparation is actually improving their readiness.

Software Engineering candidates today have access to a large number of preparation resources, including coding platforms, courses, videos, roadmaps, job descriptions, mock-interview platforms, professional communities, and AI assistants.

However, these resources are fragmented.

Candidates are often required to determine for themselves:

- What they should study.
- Which roadmap they should follow.
- Which skills matter most for their target role.
- Whether they actually understand a topic or have only studied it.
- Whether they can independently solve unseen interview problems.
- Whether their performance is improving.
- What they should study next.
- How much preparation is enough.
- Whether they are ready for an interview.

CareerGraph AI addresses this gap by connecting:

- Career goals.
- Candidate profile.
- Resume.
- Target job description.
- Skill requirements.
- Preparation activity.
- Assessment performance.
- Mock interview performance.

The platform converts these signals into a continuously updated candidate readiness profile.

The core product principle is:

> **Do not just prepare. Measure whether your preparation is moving you toward interview readiness.**

The initial MVP focuses on Software Engineering roles, particularly SDE-1, SDE-2, and SDE-3, while keeping the underlying architecture extensible to other technical careers in the future.

---

# 2. Problem Statement

## 2.1 Background

Candidates preparing for Software Engineering interviews commonly use multiple disconnected tools.

A typical preparation workflow may look like:

- LeetCode or coding platforms for DSA.
- YouTube and courses for concepts.
- ChatGPT or other AI assistants for explanations.
- LinkedIn and online communities for career guidance.
- Job portals for job descriptions.
- Mock interview platforms for interview practice.
- Multiple online roadmaps for preparation planning.

Each tool solves a specific problem.

However, there is usually no unified intelligence layer connecting the information generated across these activities.

---

## 2.2 Core Problem

The fundamental problem is not the absence of preparation resources.

The problem is the absence of a system that continuously answers:

> **Where am I now?**

> **Where do I need to be for my target role?**

> **What are my highest-priority gaps?**

> **What should I do next?**

> **Did my preparation actually improve my performance?**

> **Am I becoming interview-ready?**

Current preparation workflows are largely activity-driven rather than readiness-driven.

A candidate may solve 100 coding problems, watch dozens of videos, and follow multiple roadmaps without being able to objectively determine whether their interview readiness has improved.

---

# 3. User Pain Points

## 3.1 Resource and Roadmap Overload

Candidates encounter numerous:

- Roadmaps.
- Courses.
- Videos.
- Problem lists.
- Interview guides.
- AI recommendations.
- Preparation strategies.

They may continuously switch between resources because each new roadmap appears useful.

This can create fragmented preparation rather than a focused progression.

---

## 3.2 Unclear Skill Readiness

Completing preparation activities does not necessarily demonstrate interview readiness.

For example:

> A candidate may have solved 50 Array problems but still struggle to independently solve an unfamiliar medium-level Array problem under interview conditions.

The system therefore needs to distinguish between:

- Exposure.
- Practice.
- Demonstrated competence.
- Interview readiness.

---

## 3.3 Lack of Objective Progress Tracking

Candidates may feel that they are improving but lack structured evidence showing:

- Topic-level performance.
- Difficulty progression.
- Accuracy.
- Problem-solving speed.
- Repeated mistakes.
- Assessment performance.
- Interview performance.
- Improvement over time.

---

## 3.4 Unclear Preparation Priorities

Candidates often know they need to study:

- DSA.
- CS Fundamentals.
- System Design.
- Behavioral skills.
- Coding.
- Communication.

However, they may not know which area should receive priority today.

CareerGraph AI should identify the highest-impact next action based on the candidate's target and available performance evidence.

---

## 3.5 Disconnected Candidate and Job Information

A candidate's:

- Resume.
- Experience.
- Skills.
- Target role.
- Target level.
- Job description.
- Coding performance.
- Mock interview performance.

are usually evaluated separately.

CareerGraph AI aims to connect these signals into a unified candidate intelligence profile.

---

## 3.6 Lack of Realistic Interview Simulation

Interview preparation often focuses on isolated questions.

Real Software Engineering interviews may evaluate multiple dimensions, including:

- Coding.
- Problem solving.
- System Design.
- Computer Science Fundamentals.
- Behavioral communication.
- Ownership.
- Technical decision-making.
- Leadership for senior levels.

Candidates need a way to practice these dimensions and receive structured feedback.

---

# 4. Product Vision

## Vision

> **Build an intelligent career-readiness system that transforms fragmented interview preparation into a measurable, personalized, and continuously adaptive process.**

CareerGraph AI aims to move candidates from:

> **"I have studied a lot, but I don't know whether I am ready."**

to:

> **"I understand where I stand, what I need to improve, what I should do next, and whether my performance is improving."**

---

# 5. Product Goal

The goal of CareerGraph AI is to help Software Engineering candidates systematically improve their interview readiness through:

- Evidence-based skill assessment.
- Personalized gap analysis.
- Prioritized preparation.
- Adaptive recommendations.
- Realistic interview simulation.
- Structured evaluation.
- Progress tracking.
- Continuous feedback.

CareerGraph AI will **not** claim to guarantee that a candidate will clear an interview or receive a job offer.

Instead, it will provide evidence-based insights into the candidate's current preparation state and areas for improvement.

---

# 6. Target Users

## 6.1 Primary Users

Software Engineering candidates preparing for:

- SDE-1.
- SDE-2.
- SDE-3.
- Software Engineer.
- Senior Software Engineer roles.

The candidate selects a target role and level so that expectations can be adapted accordingly.

---

## 6.2 Initial MVP Focus

The MVP will primarily demonstrate the Software Engineering interview journey.

The system will support role-level adaptation across:

- SDE-1.
- SDE-2.
- SDE-3.

The depth of evaluation will vary according to the target level.

---

## 6.3 Future Users

The architecture may eventually be extended to other technical career paths, such as:

- Data Science.
- Machine Learning Engineering.
- Data Analytics.
- Cloud Engineering.
- Cybersecurity.

These are future expansion areas and are not part of the initial MVP.

---

# 7. Target Role Adaptation

CareerGraph AI should not evaluate every Software Engineering candidate using identical expectations.

The target profile should vary based on:

- Role.
- Level.
- Target company where applicable.
- Job description.

A conceptual capability model is:

| Capability | SDE-1 | SDE-2 | SDE-3 |
|---|---|---|---|
| Coding / DSA | High | High | High |
| CS Fundamentals | High | Medium/High | Medium |
| System Design | Basic/Medium | High | Very High |
| Behavioral | High | High | High |
| Ownership | Medium | High | Very High |
| Technical Leadership | Low/Medium | Medium | High |
| Architecture | Basic | High | Very High |

These expectations should eventually be represented as configurable role profiles rather than hard-coded assumptions.

---

# 8. Proposed Solution

CareerGraph AI will create a unified career intelligence layer connecting candidate data, target requirements, preparation activity, and demonstrated performance.

The high-level flow is:

```text
Candidate Profile
        +
Resume
        +
Target Role
        +
Job Description
        +
Preparation Data
        +
Assessment Data
        +
Interview Data
        |
        v
Career Intelligence Engine
        |
        v
Current Skill Profile
        |
        v
Skill Gap Analysis
        |
        v
Priority Identification
        |
        v
Personalized Action
        |
        v
Practice / Interview
        |
        v
Evidence-Based Evaluation
        |
        v
Updated Skill Profile
        |
        v
Next Best Action
        |
        +----------------------+
                               |
                               v
                         Continuous Loop
```

## 9. Core Product Capabilities

### 9.1 Candidate Profile Intelligence

The platform should maintain a structured candidate profile containing:

- Education.
- Experience.
- Skills.
- Projects.
- Technologies.
- Target role.
- Target level.
- Target company.
- Preparation history.
- Assessment history.
- Interview history.

### 9.2 Resume Intelligence

The candidate can provide a resume.

The system should extract relevant information such as:

- Technical skills.
- Programming languages.
- Frameworks.
- Experience.
- Projects.
- Technologies.
- Cloud skills.
- Relevant achievements.

The extracted information should contribute to the candidate's structured profile.

### 9.3 Job Description Intelligence

The candidate can provide a target job description.

The system should identify:

- Required skills.
- Preferred skills.
- Experience requirements.
- Technical requirements.
- Responsibilities.
- Role expectations.
- Relevant competencies.

These requirements should be converted into a structured target profile.

### 9.4 Skill Gap Analysis

The system should compare **Current Candidate State** against **Target Role State** to identify:

- Strengths.
- Skill gaps.
- High-priority gaps.
- Medium-priority gaps.
- Lower-priority gaps.

Example:

| Capability | Current Score | Target | Gap |
|---|---|---|---|
| DSA | 72 | 85 | 13 |
| CS Fundamentals | 64 | 80 | 16 |
| System Design | 48 | 70 | 22 |
| Behavioral | 76 | 80 | 4 |
| Coding | 81 | 85 | 4 |

The score itself should **not** be presented as an unexplained AI-generated number.

Every important assessment should have supporting evidence.

---

## 10. Evidence-Based Evaluation

This is a core technical and product requirement.

CareerGraph AI should **not** rely on a simple:

```
Candidate Answer
   ↓
Gemini
   ↓
68/100
```

Instead, evaluation should follow:

```
Candidate Response
   ↓
Structured Evidence Extraction
   ↓
Evaluation Rubric
   ↓
Dimension-Level Scores
   ↓
Supporting Evidence
   ↓
Weighted Overall Score
   ↓
Skill Profile Update
```

For example:

| Evaluation Dimension | Score | Weight |
|---|---|---|
| Requirement Understanding | 8/10 | 10% |
| Architecture | 14/20 | 20% |
| Scalability | 11/20 | 20% |
| Database Design | 9/15 | 15% |
| Reliability | 8/15 | 15% |
| Trade-offs | 7/10 | 10% |
| Communication | 8/10 | 10% |

The system should also provide evidence.

Example:

> Candidate identified load balancing and caching but did not address database replication or cache invalidation.

This makes the evaluation more transparent and defensible.

---

## 11. Personalized Preparation Engine

CareerGraph AI should not provide a generic roadmap to every candidate.

Recommendations should be based on:

- Target role.
- Target level.
- Current skill profile.
- Skill gaps.
- Previous assessment performance.
- Interview performance.
- Available preparation time.
- Preparation history.

Example:

> **Current highest-priority gap:**
> System Design - Scalability
>
> **Recommended next action:**
> Study horizontal scaling and load balancing.
>
> **Reason:**
> Recent system-design evaluation showed weaknesses in scalability and architecture decisions.
>
> **Next:**
> Complete a short design exercise and reassess.

The system should prioritize a small number of high-impact actions rather than overwhelming the candidate with dozens of recommendations.

---

## 12. Adaptive Feedback Loop

The core product loop is:

```
TARGET
   |
   v
ASSESS
   |
   v
IDENTIFY GAPS
   |
   v
PRIORITIZE
   |
   v
PREPARE
   |
   v
PRACTICE
   |
   v
SIMULATE
   |
   v
EVALUATE
   |
   v
UPDATE PROFILE
   |
   v
RECOMMEND NEXT ACTION
   |
   +----------------------+
                          |
                          v
                       REPEAT
```

This feedback loop is the central differentiator of CareerGraph AI.

The platform should continuously learn from new candidate evidence rather than generating a static roadmap once.

---

## 13. AI Mock Interview

The mock interview is a major capability but will be implemented with controlled scope.

The MVP will demonstrate three interview dimensions:

- Coding.
- Behavioral.
- System Design.

However, each module will have a different implementation depth.

| Interview Module | MVP Depth | Purpose |
|---|---|---|
| Coding | Deep | Primary interview simulation and evaluation |
| Behavioral | Moderate | Demonstrate structured behavioral assessment |
| System Design | Representative | Demonstrate system-design evaluation concept |

This approach allows CareerGraph AI to represent the broader interview journey without attempting to build a complete interview platform in every dimension.

---

## 14. Coding Interview

Coding will be the deepest interview module in the MVP.

The system should evaluate:

- Problem understanding.
- Approach selection.
- Problem-solving process.
- Correctness.
- Time complexity.
- Space complexity.
- Code quality.
- Communication.
- Time management.

The system should distinguish between:

> "The candidate has studied this topic."

and:

> "The candidate can independently solve an unfamiliar interview problem."

Possible evidence includes:

- Problem difficulty.
- Topic.
- Time taken.
- Hints used.
- Attempts.
- Correctness.
- Explanation quality.
- Complexity analysis.

---

## 15. Behavioral Interview

The MVP will support a representative behavioral interview.

The candidate may answer questions such as:

> "Tell me about a time when you handled a difficult production incident."

Evaluation dimensions may include:

- Structure.
- Clarity.
- Ownership.
- Specificity.
- Communication.
- Impact.
- Relevance.
- STAR-style completeness where appropriate.

The goal is **not** to determine whether a candidate is a "good person" or make subjective personality judgments.

The system should evaluate the response against a defined interview rubric.

---

## 16. System Design Interview

The MVP will support a representative system-design interview rather than a large library of design scenarios.

Example:

> Design a scalable notification system.

The system may evaluate:

- Requirement clarification.
- Architecture.
- APIs.
- Data storage.
- Scalability.
- Availability.
- Reliability.
- Caching.
- Failure handling.
- Trade-offs.
- Communication.

The evaluation should provide both scores and evidence.

Example:

> Candidate identified load balancing and caching but did not discuss database replication or failure recovery.

---

## 17. Unified Interview Evaluation

After the interview modules, CareerGraph AI should generate a consolidated report.

Example:

| Evaluation Area | Score |
|---|---|
| Coding | 78 |
| System Design | 68 |
| Behavioral | 81 |
| Communication | 84 |
| Problem Solving | 76 |
| **Overall Interview Readiness** | **74** |

The report should include:

- Strengths.
- Weaknesses.
- Evidence.
- High-priority gaps.
- Recommended next actions.
- Areas requiring reassessment.

---

## 18. Career Readiness Intelligence

CareerGraph AI should maintain a continuously updated readiness profile.

Example:

**Career Target:** Software Engineer - SDE-1

**Current Readiness**

| Area | Score |
|---|---|
| Coding | 78 |
| DSA | 74 |
| CS Fundamentals | 65 |
| System Design | 52 |
| Behavioral | 79 |
| Communication | 84 |

The system should also identify:

- Strong areas.
- Weak areas.
- Highest-impact gaps.
- Recent improvement.
- Areas with insufficient evidence.

The readiness assessment should be:

- Explainable.
- Role-specific.
- Evidence-based.
- Continuously updated.
- Accompanied by limitations where appropriate.

CareerGraph AI should **not** claim:

> "You have a 92% probability of getting hired."

Instead, it should communicate:

> "Based on the evidence currently available, these are your strengths, weaknesses, and highest-priority preparation areas."

---

## 19. Multi-Agent Architecture

The MVP will use a focused multi-agent architecture.

Instead of creating a separate agent for every feature, agents will represent meaningful autonomous responsibilities.

The MVP will use **four primary agents**.

### 19.1 Orchestrator Agent

Responsibilities:

- Understand the current workflow.
- Determine which agent should act.
- Maintain workflow context.
- Coordinate multi-step tasks.
- Handle agent failures and retries where appropriate.

### 19.2 Profile and Requirement Agent

Responsibilities:

- Process resumes.
- Extract candidate information.
- Process job descriptions.
- Extract target-role requirements.
- Structure candidate and target profiles.

### 19.3 Interviewer Agent

Responsibilities:

- Conduct coding interviews.
- Conduct behavioral interviews.
- Conduct system-design interviews.
- Maintain interview context.
- Ask appropriate follow-up questions.
- Adapt questioning based on the candidate's response where appropriate.

### 19.4 Evaluation and Recommendation Agent

Responsibilities:

- Evaluate candidate responses against predefined rubrics.
- Extract evidence.
- Generate dimension-level scores.
- Identify skill gaps.
- Update readiness insights.
- Recommend the next best action.

---

## 20. Agentic Design Principle

Agents should only be used where autonomous reasoning and context management provide meaningful value.

Deterministic application logic should handle tasks such as:

- Authentication.
- Data validation.
- Database writes.
- Score calculation.
- Access control.
- API routing.
- Configuration.
- Workflow state management.

This prevents unnecessary agent complexity and improves reliability and cost control.

---

## 21. Data Requirements

The platform should be data-driven.

### 21.1 Candidate Data

Potential candidate data includes:

- Profile information.
- Education.
- Experience.
- Skills.
- Projects.
- Technologies.
- Resume.
- Target role.
- Target level.
- Target company.
- Preparation history.
- Assessment history.
- Interview history.

### 21.2 Job Data

Potential job-related data includes:

- Job description.
- Required skills.
- Preferred skills.
- Experience requirements.
- Responsibilities.
- Role level.
- Technical competencies.

### 21.3 Performance Data

The system may capture:

- Assessment scores.
- Topic-level scores.
- Difficulty.
- Time taken.
- Attempts.
- Hints.
- Interview scores.
- Evaluation dimensions.
- Repeated mistakes.
- Skill progression.

### 21.4 Synthetic and Public Data

The project may use:

- Synthetic candidate profiles.
- Synthetic assessment histories.
- Public datasets.
- Public job-related datasets where licensing permits.

No confidential employer data or proprietary work-related information should be used.

---

## 22. Data-Driven Career Graph

The underlying candidate model can be represented conceptually as:

```
Candidate
  ├── Skills
  ├── Experience
  ├── Projects
  ├── Target Role
  ├── Target Level
  ├── Target Job
  ├── Assessments
  ├── Interview Results
  ├── Preparation Activity
  ├── Skill Gaps
  ├── Recommendations
  └── Progress History
```

This interconnected structure is the foundation of the "CareerGraph" concept.

---

## 23. Analytics Requirements

The platform should track meaningful trends rather than only activity counts.

Potential metrics include:

- Skill progression.
- Topic-level performance.
- Coding accuracy.
- Difficulty progression.
- Problem-solving time.
- Interview performance.
- Preparation consistency.
- Repeated weaknesses.
- Improvement after recommendations.
- Readiness changes over time.

Example:

| Week | Graph Performance |
|---|---|
| Week 1 | 42 |
| Week 2 | 51 |
| Week 3 | 64 |
| Week 4 | 73 |

The objective is to show evidence of improvement.

---

## 24. Dashboard Requirements

The dashboard should provide a consolidated view.

### 24.1 Career Target

- Target role.
- Target level.
- Target company.
- Target job description.

### 24.2 Readiness Overview

- Overall readiness.
- Skill distribution.
- Progress trend.
- Confidence / evidence coverage.

### 24.3 Skill Gaps

- High-priority gaps.
- Medium-priority gaps.
- Lower-priority gaps.

### 24.4 Preparation Recommendation

The system should display the most important next action.

Example:

> **Next Best Action:** Practice Graph BFS/DFS
>
> **Reason:** Recent assessments show repeated difficulty with graph traversal while other DSA topics are currently above the target threshold.

### 24.5 Interview History

| Mock Interview | Score |
|---|---|
| #1 | 61 |
| #2 | 68 |
| #3 | 74 |

### 24.6 Progress Trend

The dashboard should visualize meaningful improvement over time.

---

## 25. MVP Scope

The MVP will focus on demonstrating the complete intelligence loop rather than implementing every possible feature at production scale.

### 25.1 MVP Must Work Well

The following capabilities are core:

- Candidate profile creation.
- Resume analysis.
- Target role definition.
- Job description analysis.
- Skill profile generation.
- Skill gap analysis.
- Evidence-based evaluation.
- Personalized next-best-action recommendation.
- Coding interview.
- Behavioral interview.
- Representative system-design interview.
- Unified interview evaluation.
- Readiness dashboard.
- Progress tracking.
- Adaptive feedback loop.

### 25.2 MVP Depth

| Capability | MVP Depth |
|---|---|
| Candidate Profile | Full |
| Resume Intelligence | Full |
| Job Description Intelligence | Full |
| Skill Gap Analysis | Full |
| Personalized Recommendation | Full |
| Coding Interview | Deep |
| Behavioral Interview | Moderate |
| System Design | Representative |
| Unified Evaluation | Full |
| Readiness Dashboard | Full |
| Adaptive Feedback Loop | Full |
| Multi-Agent Architecture | Focused |

---

## 26. MVP User Journey

The primary demonstration flow should be:

1. Candidate creates profile
          |
          v
2. Candidate selects target role and level
          |
          v
3. Candidate uploads resume
          |
          v
4. Candidate provides target job description
          |
          v
5. System creates target profile
          |
          v
6. System identifies skill gaps
          |
          v
7. System recommends the highest-priority action
          |
          v
8. Candidate completes interview assessment
          |
          v
9. System evaluates performance using a rubric
          |
          v
10. Candidate profile is updated
          |
          v
11. System identifies the next best action
          |
          v
12. Dashboard shows measurable progress

This end-to-end loop is the primary MVP demonstration.

---

## 27. Out of Scope for MVP

The following will **not** be primary MVP priorities:

- Large-scale job marketplace.
- Direct job application automation.
- Recruiter marketplace.
- Guaranteed interview or job outcomes.
- Automated hiring decisions.
- Large social networking functionality.
- Support for dozens of career domains.
- Integration with every coding platform.
- Perfect replication of any company's proprietary interview process.
- Large-scale enterprise recruitment workflows.
- Extensive interview-question libraries.
- Fully autonomous career decision-making.

These may be considered in future versions.

---

## 28. Cost and Resource Management

Cost efficiency is a technical requirement.

The platform should avoid using expensive AI inference unnecessarily.

Potential strategies include:

- Use efficient models for extraction and classification.
- Reserve stronger models for complex reasoning and evaluation.
- Cache reusable candidate information.
- Avoid repeatedly sending identical context.
- Limit interview duration and unnecessary agent calls.
- Store structured results for reuse.
- Monitor AI usage.
- Track cost per workflow.
- Apply cloud budget alerts.
- Apply appropriate service limits.

The goal is to demonstrate that the architecture is technically feasible within the Patchamomma Build Phase resources.

---

## 29. Security and Privacy Requirements

The platform may process sensitive candidate information.

It should protect:

- Resume data.
- Personal information.
- Interview responses.
- Candidate performance data.
- Authentication information.
- API credentials.

Security requirements include:

- Secure authentication.
- Access control.
- Protected storage.
- Secure API communication.
- Secret management.
- Appropriate logging.
- Avoidance of unnecessary sensitive data collection.

No confidential employer data should be used in the project.

---

## 30. Explainability Requirements

Important AI-generated assessments should provide understandable reasoning.

For example, instead of:

> System Design: 62/100

The platform should provide:

> **System Design: 62/100**
>
> **Strengths:**
> - Identified major service boundaries.
> - Considered caching.
>
> **Gaps:**
> - Limited discussion of database replication.
> - No clear failure-recovery strategy.
> - Scalability trade-offs were not fully explained.

This allows the candidate to understand what to improve.

---

## 31. Functional Requirements

The MVP should support:

1. User can create a candidate profile.
2. User can define a target Software Engineering role.
3. User can define a target level.
4. User can optionally provide a target company.
5. User can provide a resume.
6. System can extract structured candidate information.
7. User can provide a job description.
8. System can extract target-role requirements.
9. System can compare candidate and target profiles.
10. System can identify skill gaps.
11. System can prioritize skill gaps.
12. System can recommend the next best preparation action.
13. System can conduct a coding interview.
14. System can conduct a behavioral interview.
15. System can conduct a representative system-design interview.
16. System can evaluate interview responses using predefined rubrics.
17. System can provide evidence supporting evaluation results.
18. System can generate an interview report.
19. System can update candidate readiness information.
20. System can maintain historical performance data.
21. System can display readiness and progress through a dashboard.
22. System can generate a new recommendation after assessment.

---

## 32. Non-Functional Requirements

### 32.1 Performance

The application should provide reasonable response times for interactive user workflows.

### 32.2 Scalability

The architecture should be capable of supporting additional users and interview sessions without requiring a fundamental redesign.

### 32.3 Reliability

The system should gracefully handle:

- AI failures.
- API failures.
- Invalid input.
- Agent timeouts.
- Temporary service failures.

### 32.4 Explainability

Important assessments and recommendations should be supported by evidence.

### 32.5 Observability

Important application and agent workflows should be monitored.

Logs should avoid unnecessary exposure of sensitive candidate information.

### 32.6 Maintainability

The architecture should separate:

- UI.
- Backend.
- AI agents.
- Evaluation logic.
- Data storage.
- Analytics.

This should allow individual components to be improved independently.

---

## 33. Success Metrics

The project should define measurable success criteria.

### 33.1 Product Metrics

- Successful completion of the end-to-end candidate workflow.
- Successful completion of mock interview workflow.
- Recommendation generation success rate.
- Dashboard availability.
- Successful readiness-profile update.

### 33.2 AI Metrics

- Structured output validity.
- Evaluation consistency against predefined rubrics.
- Recommendation relevance.
- Agent workflow completion rate.
- Evidence extraction quality.

### 33.3 Candidate Metrics

Potential outcome metrics include:

- Improvement between repeated assessments.
- Reduction in high-priority skill gaps.
- Improvement in mock interview performance.
- Improvement in topic-level performance.

### 33.4 Technical Metrics

Potential metrics include:

- API reliability.
- Agent execution success rate.
- Response latency.
- Cost per workflow.
- Cost per interview simulation.
- Failure rate.

---

## 34. Risks and Mitigations

| Risk | Mitigation |
|---|---|
| MVP becomes too large | Maintain strict MVP depth and scope |
| AI produces unreliable evaluations | Use predefined rubrics and structured evaluation |
| Readiness scores become arbitrary | Use transparent weighted scoring |
| Recommendations become generic | Ground recommendations in candidate performance data |
| Job requirements are incorrectly extracted | Validate structured extraction |
| Excessive agent complexity | Use four meaningful agents |
| High AI costs | Use model routing, caching, limits, and monitoring |
| Candidate data exposure | Use authentication, access control, secure storage, and secret management |
| Mock interview feels unrealistic | Use structured interview flows and defined evaluation rubrics |
| Dashboard becomes only a visualization layer | Make dashboard outputs directly connected to recommendation and readiness logic |
| Product becomes another AI interview bot | Keep the continuous career-readiness feedback loop as the core product |
| Insufficient evidence for a score | Display confidence/evidence coverage and avoid overclaiming |

---

## 35. Product Differentiation

CareerGraph AI is **not** intended to be simply another:

- Coding practice platform.
- Course platform.
- Resume analyzer.
- AI chatbot.
- Mock interview tool.

The key differentiation is the connection between these activities.

Conceptually:

```
Job Description
      +
Candidate Profile
      +
Preparation Data
      +
Coding Performance
      +
Interview Performance
      |
      v
Career Intelligence
      |
      v
Skill Gap
      |
      v
Next Best Action
      |
      v
Practice
      |
      v
Reassessment
      |
      v
Updated Career Profile
```

The product is therefore positioned as an **adaptive career-readiness intelligence layer**, rather than a single-purpose preparation tool.

---

## 36. Competitive Positioning

CareerGraph AI should not attempt to compete solely by claiming to have:

- More coding questions.
- More mock interviews.
- More learning resources.
- More AI features.

Instead, its differentiation should be:

> Existing preparation tools can generate activity and individual results. CareerGraph AI connects those signals into a continuous readiness loop.

The platform can complement existing resources rather than attempting to replace every preparation tool.

---

## 37. Future Scope

Potential future capabilities include:

- Integration with coding platforms.
- Learning-platform integrations.
- More advanced System Design interviews.
- More extensive Behavioral interview simulations.
- Company-specific preparation profiles using public information.
- Personalized job matching.
- Career transition recommendations.
- Skill-demand forecasting.
- Long-term career planning.
- Additional technical career paths.
- Advanced analytics.
- Recruiter-facing functionality.
- Learning-resource optimization.

These capabilities are outside the initial MVP.

---

## 38. Long-Term Vision

CareerGraph AI aims to become an **AI Career Intelligence Layer** that understands the relationship between:

```
Person → Skills → Goals → Opportunities → Preparation → Performance → Outcomes
```

The initial implementation focuses on Software Engineering interview preparation.

Over time, the same underlying intelligence framework could support additional career paths.

---

## 39. Initial Technology Direction

The project will prioritize **Google and Google Cloud technologies** as required by the Patchamomma Build Phase.

Potential technologies include:

- Google Gemini.
- Google AI Studio.
- Google ADK (Agent Development Kit).
- Google Cloud Run.
- Firebase / Firestore.
- Google Cloud Storage.
- BigQuery.
- Looker Studio / Looker.
- Pub/Sub where asynchronous processing is required.
- MCP Toolbox for Databases where it provides meaningful value.
- Google Cloud security and observability services where appropriate.

Technology selection will be finalized during the Technical Requirements Document (TRD).

A technology should only be included when it has a clear architectural purpose.

---

## 40. Technology Selection Principle

CareerGraph AI should demonstrate thoughtful use of Google Cloud rather than technology accumulation.

For example:

| Requirement | Potential Technology | Purpose |
|---|---|---|
| Generative AI | Gemini | Reasoning, extraction, evaluation |
| Multi-Agent AI | Google ADK | Agent orchestration |
| Backend | Cloud Run | Serverless application backend |
| Candidate Data | Firestore | Structured application data |
| Document Storage | Cloud Storage | Resume and document storage |
| Analytics | BigQuery | Historical and analytical data |
| Reporting | Looker Studio | Visual analytics |
| Authentication | Firebase Authentication | User identity and access |
| Async Processing | Pub/Sub | Event-driven workflows |
| Database Agent Access | MCP Toolbox | Controlled database interaction |
| Monitoring | Google Cloud tools | Observability and reliability |

The final architecture will use only the services required by the actual system design.

---

## 41. MVP Definition of Done

The MVP should be considered successful when a user can complete the following end-to-end journey:

1. Create a candidate profile.
2. Select a target Software Engineering role and level.
3. Provide a resume.
4. Provide a target job description.
5. Receive a structured candidate and target profile.
6. Receive evidence-based skill-gap analysis.
7. Receive a prioritized next-best action.
8. Complete a representative interview workflow.
9. Receive rubric-based evaluation with supporting evidence.
10. See an updated readiness profile.
11. Receive a new recommended action.
12. View progress through a dashboard.

The final demonstration should clearly show that the recommendation changes based on newly generated candidate evidence.

---

## 42. Core Product Principle

CareerGraph AI should not simply answer:

> "What should I study?"

It should continuously answer:

> "Based on my target role and actual performance, what should I do next, why should I do it, and how will we know whether it worked?"

This principle forms the foundation of the product.

---

## 43. Final Product Statement

CareerGraph AI is a data-driven, multi-agent career-readiness platform that connects a candidate's goals, skills, preparation activity, assessments, and interview performance to continuously identify skill gaps, recommend the highest-impact next action, and measure whether the candidate is actually progressing toward Software Engineering interview readiness.
