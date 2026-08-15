# Business Requirements Document (BRD)

## CareerGraph AI

**Working Product Name:** CareerGraph AI  
**Project:** Patchamomma 2026 Build Phase  
**Document:** Business Requirements Document  
**Version:** 0.2  
**Date:** 16 August 2026  
**Status:** Draft

# 1. Executive Summary

**CareerGraph AI** is a data-driven, multi-agent AI platform designed to help Software Engineering candidates understand their current interview readiness, identify their highest-impact skill gaps, prepare strategically, and continuously evaluate their progress.

Software Engineering candidates today have access to an enormous amount of preparation material, including coding platforms, courses, videos, roadmaps, job descriptions, mock-interview platforms, professional communities, and AI assistants.

However, these resources are largely fragmented.

Candidates are often required to determine for themselves:

- What they should study.

- Which resources they should follow.

- Which skills are most important for their target role.

- Whether they actually understand a topic or can apply it independently.

- Whether their performance is improving.

- How much preparation is enough.

- Whether they are ready for a particular interview.

CareerGraph AI aims to address this gap by creating a continuous feedback loop between career goals, candidate data, preparation activity, assessment performance, and interview simulation.

The platform will initially focus on Software Engineering roles across SDE-1, SDE-2 and SDE-3 levels, while maintaining an architecture that can eventually be extended to other professional career domains.

# 2. Problem Statement
## 2.1 Background

Candidates preparing for Software Engineering interviews have abundant access to learning and preparation resources.

A typical candidate may use:

LeetCode or other coding platforms for DSA.

YouTube and courses for concepts.

AI assistants for explanations.

LinkedIn and online communities for career guidance.

Job portals for job descriptions.

Mock-interview platforms for practice.

Multiple roadmaps created by different educators and professionals.


While this abundance of resources is useful, it can also create information overload and fragmented preparation.

Candidates may follow one roadmap for some time, discover another recommendation, switch to it, and continue without having a reliable understanding of whether the chosen approach is actually improving their interview readiness.

## 2.2 Core Problem

The fundamental problem is not the absence of preparation resources.

The problem is the absence of an intelligent system that continuously answers:

**Where am I now?

Where do I need to be for my target role?

What are my most important gaps?

What should I do next?

Is my preparation actually improving my interview readiness?

Current preparation workflows generally treat these activities independently.**

For example:

Resume
   ↓
Job Search


LeetCode
   ↓
DSA Practice


YouTube
   ↓
Learning


Mock Interview
   ↓
Interview Practice


ChatGPT
   ↓
Questions / Explanations

There is often no unified intelligence connecting these activities.

# 3. User Pain Points

CareerGraph AI addresses the following major pain points.

## 3.1 Resource and Roadmap Overload

Candidates encounter numerous preparation roadmaps, courses, videos, problem lists and recommendations.

They may struggle to determine which path is appropriate for their specific target role, experience level and current skill level.

## 3.2 Unclear Skill Readiness

Completing a certain number of coding questions or watching educational content does not necessarily demonstrate interview readiness.

For example:

A candidate may have solved 30 Array problems but still struggle to independently solve an unseen medium-level Array problem within an interview time constraint.

The platform therefore needs to evaluate actual demonstrated performance, rather than relying only on activity counts.

## 3.3 Lack of Objective Progress Tracking

Candidates may feel that they are improving but may not have a structured way to measure:

Accuracy.
Difficulty progression.
Problem-solving speed.
Topic-level performance.
Repeated mistakes.
Interview performance.
Improvement over time.

## 3.4 Unclear Preparation Priorities

Candidates often know that they need to prepare DSA, System Design, CS fundamentals, behavioral questions and other areas.

However, they may not know:

**Which area should I prioritize right now?**

The answer should depend on the candidate's target role and evidence from their performance.

## 3.5 Disconnected Job and Candidate Information

A candidate's:

Resume
Current experience
Skills
Target job description
Coding performance
Learning activity
Mock interview results

are usually evaluated separately.

CareerGraph AI aims to connect these sources into a unified candidate profile.

## 3.6 Lack of Realistic Interview Simulation

Many preparation tools focus primarily on individual questions.

A real Software Engineering interview, however, can involve multiple evaluation dimensions, including:

Coding.
Problem solving.
System Design.
Computer Science fundamentals.
Behavioral communication.
Ownership.
Leadership and technical decision-making for senior levels.

Candidates need the ability to practice these dimensions together in a realistic interview environment.

# 4. Product Vision
Vision

To build an intelligent career-readiness system that transforms fragmented interview preparation into a measurable, personalized and continuously adaptive process.

CareerGraph AI aims to move candidates from:

"I have studied a lot, but I don't know whether I am ready."

to:

"I understand where I stand, what I need to improve, what I should do next, and whether my performance is improving."

# 5. Product Goal

The goal of CareerGraph AI is to help Software Engineering candidates systematically improve their interview readiness and increase their probability of interview success.

The platform will not claim to guarantee that a candidate will clear an interview.

Instead, it will provide:

Evidence-based skill assessment.
Personalized gap analysis.
Prioritized preparation.
Adaptive learning recommendations.
Realistic interview simulation.
Continuous performance evaluation.
Progress tracking.
Interview-readiness insights.

# 6. Target Users
Primary Users

Software Engineering candidates preparing for:

SDE-1
SDE-2
SDE-3
Software Engineer
Senior Software Engineer roles

The candidate selects a target role and experience level, allowing the platform to adapt its expectations and assessment criteria.

Secondary Users — Future Scope

The underlying framework could eventually support other technical and professional careers where suitable assessment data and role-specific evaluation criteria are available.

Examples could include:

Data Science
Machine Learning Engineering
Data Analytics
Product Management
Cybersecurity
Cloud Engineering

These are future expansion areas, not part of the initial MVP.

# 7. Target Role Adaptation

The platform should not treat every Software Engineering candidate identically.

The expected skill profile should vary based on:

Role

Software Engineer / SDE

Level

SDE-1 / SDE-2 / SDE-3

Target Company

Where relevant, the candidate may provide a target company or job description.

Target Job Description

The system can extract requirements from the provided job description.

For example:

Capability	SDE-1	SDE-2	SDE-3
Coding / DSA	High	High	High
CS Fundamentals	High	Medium/High	Medium
System Design	Basic/Medium	High	Very High
Behavioral	High	High	High
Ownership	Medium	High	Very High
Technical Leadership	Low/Medium	Medium	High
Architecture	Basic	High	Very High

These expectations should eventually be represented as configurable role profiles rather than hard-coded assumptions.

# 8. Proposed Solution

CareerGraph AI will create a unified candidate intelligence layer connecting:

Candidate Profile
       +
Resume
       +
Target Role
       +
Job Description
       +
Skill Profile
       +
Learning Activity
       +
Coding Performance
       +
Mock Interview Performance
       ↓
Career Intelligence Engine
       ↓
Skill Gap Analysis
       ↓
Priority Identification
       ↓
Personalized Preparation
       ↓
Interview Simulation
       ↓
Performance Evaluation
       ↓
Updated Candidate Profile

This creates a continuous feedback loop.

# 9. Core Product Capabilities
## 9.1 Candidate Profile Intelligence

The platform should maintain a structured profile containing information such as:

Education.
Experience.
Skills.
Projects.
Technologies.
Target role.
Target level.
Target company.
Preparation history.
Assessment history.

## 9.2 Resume Intelligence

The candidate can provide a resume.

The system extracts relevant information such as:

Technical skills.
Programming languages.
Experience.
Projects.
Domain experience.
Cloud technologies.
Relevant achievements.

The system can then compare the candidate profile against a target role.

## 9.3 Job Description Intelligence

The candidate can provide a job description.

The system identifies:

Required skills.
Preferred skills.
Experience requirements.
Technical requirements.
Role responsibilities.
Interview-relevant competencies.

The requirements are converted into a structured target profile.

## 9.4 Skill Gap Analysis

The system compares:

Current Candidate State

against

Target Role State

to identify gaps.

Example:

Target: Software Engineer — SDE-2


DSA                  78 / 100
System Design        54 / 100
CS Fundamentals      71 / 100
Coding                82 / 100
Behavioral            76 / 100
Target-role fit       68 / 100

The system should explain why a score or assessment was generated instead of presenting unexplained AI-generated numbers.

## 9.5 Personalized Preparation Roadmap

Instead of providing a generic roadmap, the platform should generate a roadmap based on:

Target role.
Target level.
Candidate skill gaps.
Previous performance.
Available preparation time.
Historical learning activity.
Interview timeline.

Example:

Highest-priority gap: System Design

Recommended focus:

Day 1 → Scalability fundamentals
Day 2 → Caching
Day 3 → Database design
Day 4 → Load balancing
Day 5 → Design exercise
Day 6 → Mock system-design interview
Day 7 → Reassessment

The roadmap should change as new performance data becomes available.

## 9.6 Coding Assessment

The platform should support coding/problem-solving assessment.

It should capture metrics such as:

Problem category.
Difficulty.
Attempt duration.
Successful/unsuccessful result.
Hints used.
Number of attempts.
Solution quality where measurable.
Repeated error patterns.

The objective is to distinguish:

"I have seen this topic."

from:

"I can independently solve an unseen interview problem."

## 9.7 Full AI Mock Interview

This should be one of the flagship features.

Instead of providing only isolated questions, CareerGraph AI should simulate a representative Software Engineering interview.

Interview flow
Interview Setup
      ↓
Coding Round
      ↓
System Design Round
      ↓
Behavioral Round
      ↓
Evaluation
      ↓
Interview Report
      ↓
Updated Readiness Profile

The exact interview structure can vary according to target level.

Coding Round

The candidate receives one or more coding problems.

The system evaluates dimensions such as:

Problem understanding.
Approach.
Correctness.
Complexity.
Coding quality.
Communication.
Time management.
System Design Round

The candidate receives a design scenario.

Example:

Design a scalable notification system.

The evaluation can consider:

Requirement clarification.
Architecture.
APIs.
Data storage.
Scalability.
Availability.
Reliability.
Caching.
Trade-offs.
Failure handling.
Behavioral Round

The candidate answers behavioral questions such as:

"Tell me about a time when you handled a production incident."

The system can evaluate against a defined rubric including:

Structure.
Clarity.
Ownership.
Specificity.
Communication.
Impact.
Relevance.
STAR-style completeness where appropriate.
Senior-Level Evaluation

For SDE-2/SDE-3 simulations, the platform can additionally assess areas such as:

Ownership.
Technical decision-making.
Architecture.
Mentoring.
Conflict resolution.
Leadership.
Cross-team collaboration.

# 10. Interview Evaluation Report

After a mock interview, the platform should generate a structured report.

Example:

INTERVIEW SIMULATION
────────────────────────


Overall Readiness: 74/100


Coding              78
System Design       68
Behavioral          81
Communication       84
Problem Solving     76


Highest Priority Gaps
────────────────────────
1. System Design scalability
2. Dynamic Programming
3. Quantifying behavioral impact

The system should then update the candidate's readiness profile and recommendations.

# 11. Career Readiness Intelligence

CareerGraph AI should provide a readiness view based on measurable signals.

The readiness assessment should be:

Explainable.
Based on defined metrics.
Role-specific.
Continuously updated.
Accompanied by confidence/limitations where appropriate.

The platform should not claim:

"You have a 92% probability of getting hired."

Instead, it should communicate:

"Based on your available performance data, these are your current strengths, weaknesses and highest-priority areas for improvement."

# 12. Adaptive Feedback Loop

The core intelligence loop is:

TARGET
  ↓
ASSESS
  ↓
IDENTIFY GAPS
  ↓
PRIORITIZE
  ↓
PREPARE
  ↓
PRACTICE
  ↓
SIMULATE INTERVIEW
  ↓
EVALUATE
  ↓
UPDATE PROFILE
  ↓
RECOMMEND NEXT ACTION
  ↺

This continuous loop is the central differentiator of the platform.

# 13. Multi-Agent AI Requirements

The system is expected to use a multi-agent architecture where individual agents have specialized responsibilities.

Potential agents include:

Career/Coordinator Agent

Orchestrates the overall workflow.

Resume Intelligence Agent

Extracts and structures candidate information.

Job Intelligence Agent

Analyzes job descriptions and target-role requirements.

Skill Assessment Agent

Evaluates candidate capabilities.

Skill Gap Agent

Identifies and prioritizes gaps.

Learning/Recommendation Agent

Generates adaptive preparation plans.

Interviewer Agent

Conducts the mock interview.

Evaluation Agent

Evaluates candidate responses against predefined rubrics.

Career Intelligence Agent

Synthesizes the information into readiness insights.

The final architecture will be determined during the TRD phase.

# 14. Data Requirements

The platform should be data-driven.

Potential data sources include:

Candidate-generated data
Resume.
Skills.
Target role.
Job descriptions.
Coding attempts.
Assessment results.
Mock interview responses.
Learning activity.
Public datasets

Where appropriate:

Public job datasets.
Public technology/skills datasets.
Public salary or employment datasets where relevant.
Publicly available interview-related datasets where licensing permits.
Synthetic data

Synthetic candidate profiles and performance histories may be used to demonstrate the analytics and recommendation capabilities without exposing private candidate information.

Important Privacy Requirement

No confidential employer data, internal company information, proprietary interview material, or sensitive work-related data should be used.

# 15. Analytics Requirements

The system should track trends such as:

Skill progression.
Topic-level performance.
Coding accuracy.
Difficulty progression.
Interview performance.
Preparation consistency.
Repeated weaknesses.
Improvement after recommendations.
Readiness changes over time.

Example:

Graph Performance


Week 1   42
Week 2   51
Week 3   64
Week 4   73

The objective is to show evidence of improvement, not merely activity.

# 16. Dashboard Requirements

The dashboard should provide a consolidated view containing:

Career Target
Software Engineer
SDE-2
Target Company: [Optional]
Readiness Overview
Overall Readiness
Skill Distribution
Progress Trend
Skill Gaps
High Priority
Medium Priority
Low Priority
Current Recommendations

"Focus on System Design before increasing coding difficulty."

Interview History
Mock #1 → 61
Mock #2 → 68
Mock #3 → 74
Next Best Action

A single prioritized action should be surfaced rather than overwhelming the user with recommendations.

# 17. Functional Requirements

The MVP should support:

FR-01

User can create a candidate profile.

FR-02

User can define target Software Engineering role and level.

FR-03

User can provide a resume.

FR-04

System can analyze the resume.

FR-05

User can provide a job description.

FR-06

System can extract target-role requirements.

FR-07

System can identify candidate skill gaps.

FR-08

System can generate a prioritized preparation plan.

FR-09

System can conduct coding assessments.

FR-10

System can conduct a system-design interview simulation.

FR-11

System can conduct a behavioral interview simulation.

FR-12

System can evaluate interview performance against defined rubrics.

FR-13

System can generate an interview report.

FR-14

System can maintain historical performance data.

FR-15

System can update recommendations based on new performance data.

FR-16

System can display progress and readiness insights through a dashboard.

# 18. Non-Functional Requirements
Performance

The system should provide reasonable response times for interactive AI workflows.

Scalability

The architecture should support increasing numbers of candidates and interview sessions.

Security

The system should protect:

Candidate resumes.
Personal information.
Interview responses.
API credentials.
Application data.
Privacy

Candidate data should not be unnecessarily exposed to other users.

Explainability

Important assessments and recommendations should provide understandable reasoning.

Reliability

Failures in individual AI workflows should be handled gracefully.

Observability

Important application and agent workflows should be logged for debugging and monitoring without unnecessarily logging sensitive information.

# 19. MVP Scope

Because the Patchamomma build window is limited, the MVP will focus on demonstrating the complete intelligence loop rather than implementing every possible feature.

MVP

Candidate Profile

↓

Resume Analysis

↓

Target Role/JD Analysis

↓

Skill Gap Analysis

↓

Personalized Roadmap

↓

Full Representative Mock Interview

Coding
System Design
Behavioral

↓

AI Evaluation

↓

Readiness Dashboard

↓

Adaptive Recommendation

This provides an end-to-end demonstrable product.

# 20. Out of Scope for MVP

The following should not become priorities during the initial build:

Large-scale job marketplace.
Direct job application automation.
Recruiter marketplace.
Guaranteed interview/job outcomes.
Fully automated hiring decisions.
Large-scale social network.
Support for dozens of career domains.
Real-time integration with every coding platform.
Perfect replication of any company's proprietary interview process.

These may be considered in future versions.

# 21. Success Metrics

The project should define measurable success criteria.

Potential MVP metrics include:

Product
Percentage of core workflows successfully completed.
Successful end-to-end interview simulation.
Recommendation generation success rate.
Dashboard completion.
AI
Structured output validity.
Evaluation consistency against predefined rubrics.
Recommendation relevance.
Agent workflow completion rate.
Candidate
Improvement between repeated assessments.
Reduction in identified high-priority skill gaps.
Improvement in mock interview performance.
Technical
API reliability.
Agent execution success rate.
Response latency.
Cost per candidate/interview simulation.

The final measurable metrics and evaluation methodology will be defined during the TRD and evaluation phase.

# 22. Risks and Mitigations

Risk	Mitigation
AI produces unreliable evaluations	Use predefined evaluation rubrics and structured outputs
Readiness score becomes arbitrary	Define transparent scoring methodology
Excessive project scope	Maintain strict MVP boundaries
AI recommendations become generic	Ground recommendations in candidate performance data
Hallucinated job requirements	Use structured job-description extraction and validation
Sensitive candidate data exposure	Apply access control and secure storage
High cloud/API costs	Monitor usage and apply budget controls
Over-reliance on LLM judgment	Combine deterministic metrics with AI evaluation
Mock interview does not represent real interviews	Clearly define simulation scope and evaluation rubric

# 23. Future Scope

After establishing the Software Engineering platform, CareerGraph AI could evolve into a broader career intelligence platform.

Potential future capabilities include:

Additional technical career paths.
Personalized job matching.
Continuous job-market intelligence.
Skill-demand forecasting.
Career transition recommendations.
Learning-resource optimization.
Recruiter-facing insights.
Long-term career planning.
Integration with learning and coding platforms.

The underlying principle would remain:

Understand current state → understand target state → identify gaps → recommend action → measure outcome → adapt.

# 24. Product Differentiation

CareerGraph AI is not intended to be simply another:

Coding practice platform.
Course platform.
Resume analyzer.
AI chatbot.
Mock interview tool.

Its differentiation is the connection between these activities.

The platform combines:

Career Goal
     +
Candidate Profile
     +
Job Requirements
     +
Learning Data
     +
Coding Performance
     +
Interview Performance
     ↓
Career Intelligence
     ↓
Personalized Action
     ↓
Continuous Measurement

The central product philosophy is:

Don't just prepare. Measure whether your preparation is moving you toward interview readiness.

# 25. Product Success Vision

A successful CareerGraph AI session should allow a candidate to answer:

Before preparation

Where am I?

During preparation

What should I work on next and why?

After practice

Did I actually improve?

Before an interview

What are my remaining weaknesses?

After a mock interview

What would I need to improve before attempting the real interview?

This transforms interview preparation from a largely subjective process into a data-driven, continuously adaptive preparation cycle.

# 26. Long-Term Vision

CareerGraph AI aims to become an AI Career Intelligence Layer that understands the relationship between:

Person → Skills → Goals → Opportunities → Preparation → Performance → Outcomes

The initial implementation focuses on Software Engineering interviews, but the architecture is intended to support expansion into additional career domains over time.
