# Evaluation Framework

## 1. Purpose

The Evaluation Framework defines how Career-Intelligence-Platform evaluates candidate performance using structured evidence, predefined competency models, and explicit evaluation rubrics.

The framework is designed to ensure that candidate evaluations are:

- Evidence-based.
- Explainable.
- Consistent.
- Role-aware.
- Level-aware.
- Company-aware when a target company is provided.
- Traceable over time.
- Resistant to arbitrary AI-generated scores.

The framework supports the core product loop:

Candidate Evidence
→ Evaluation
→ Skill State Update
→ Skill Gap
→ Next Best Action
→ Further Preparation / Assessment
→ New Evidence

The system should evaluate what the candidate has demonstrated rather than make unsupported predictions about hiring outcomes.

The platform must not generate guaranteed hiring outcomes or unsupported probability-of-hire claims.

## 2. Evaluation Philosophy

Career-Intelligence-Platform evaluates candidates based on demonstrated evidence rather than assumptions about capability.

The evaluation process follows these principles:

### 2.1 Evidence Before Score

The system should identify observable evidence from a candidate's:

- Interview responses.
- Code submissions.
- Problem-solving approach.
- Communication.
- System-design reasoning.
- Behavioral responses.
- Previous assessment results.
- Preparation and assessment history.

A score should be derived from the available evidence rather than generated independently of it.

### 2.2 Rubric-Based Evaluation

Each interview type uses predefined evaluation dimensions and rubrics.

The AI evaluator should assess the candidate against these dimensions rather than assigning an unrestricted overall score.

For example, a coding interview may evaluate:

- Problem understanding.
- Approach.
- Algorithm and data-structure selection.
- Correctness.
- Complexity analysis.
- Code quality.
- Communication.

### 2.3 Role and Level Awareness

Evaluation should consider the candidate's selected target:

- Role.
- Level.
- Target company, when provided.
- Job description, when provided.

The same demonstrated capability may have different expectations depending on the target level.

For example, system-design expectations for SDE-1 should not be evaluated using the same expectations as SDE-3.

### 2.4 Company-Aware Evaluation

When a target company is provided, company-specific requirements may be incorporated through:

- The provided job description.
- Configured competency expectations.
- Approved company-specific preparation profiles.

Company-specific information must not be fabricated by the AI.

When company-specific information is unavailable, the system should fall back to role- and level-based expectations.

### 2.5 Separation of Evidence and Inference

The system should distinguish between:

- Explicit evidence — directly demonstrated by the candidate.
- Supported inference — a reasonable conclusion based on available evidence.
- Missing evidence — a capability for which insufficient evidence exists.

The system should not treat missing evidence as proof of weakness.

### 2.6 Confidence and Evidence Coverage

Evaluation results should communicate how strongly the available evidence supports a conclusion.

A candidate may receive a lower-confidence assessment when:

- The interview response is incomplete.
- The candidate was not given an opportunity to demonstrate a competency.
- The available evidence is limited.
- The response is ambiguous.

Confidence should not be used as a replacement for the actual evaluation score.

### 2.7 Deterministic Aggregation

The AI is responsible for interpreting candidate evidence against the defined rubric.

The application is responsible for deterministic operations such as:

- Score aggregation.
- Weight application.
- Threshold checks.
- Skill-state updates according to defined rules.
- Readiness calculations.
- Evidence coverage calculations.

This prevents the final result from depending entirely on unrestricted model reasoning.

### 2.8 Historical Evaluation

Evaluations should be retained as historical evidence.

A new assessment should not erase previous results.

The system should be able to compare:

- Previous performance.
- Current performance.
- Skill-state changes.
- Repeated evidence.
- Previous recommendations.
- Current recommendations.

This enables the platform to answer:

> "Am I actually improving?"

rather than simply showing the candidate their latest score.

### 2.9 No Hiring Prediction

The evaluation system measures interview-readiness and demonstrated competencies.

It must not claim:

- That a candidate will receive an offer.
- That a candidate will pass a specific company's interview.
- A guaranteed hiring outcome.
- An unsupported probability of getting hired.

The system should communicate preparation insights and evidence-backed recommendations instead.

### 2.10 Evaluation Output

A meaningful evaluation should contain more than a single score.

At minimum, an evaluation should provide:

- Dimension-level results.
- Supporting evidence.
- Strengths.
- Improvement areas.
- Confidence.
- Evidence coverage.
- Skill-state implications.
- Recommended next action.

The goal is not merely to tell the candidate how they performed.

The goal is to explain:

> What did I demonstrate?

> Where am I currently weak?

> What evidence supports that conclusion?

> What should I do next?

## 3. Evidence Model

The platform represents candidate capability through structured evidence collected from multiple sources.

Evidence is the foundation for:

- Skill-state estimation.
- Skill-gap identification.
- Interview evaluation.
- Readiness assessment.
- Personalized recommendations.
- Progress tracking.

The system should preserve the original evidence and maintain a traceable relationship between evidence, evaluation results, skill states, and recommendations.

### 3.1 Evidence Sources

Evidence may be collected from:

- Resume.
- Job description alignment.
- Candidate profile.
- Coding interview responses.
- Code submissions.
- Behavioral interview responses.
- System-design interview responses.
- Previous assessments.
- Preparation activity.
- Repeated demonstrations of the same competency.

Different evidence sources should not automatically be treated as equally strong.

### 3.2 Evidence Types

The system should classify evidence according to what it represents.

#### Explicit Evidence

Information directly demonstrated or explicitly provided by the candidate.

Examples:

- Candidate explains an algorithm correctly.
- Candidate writes a working solution.
- Candidate describes a project using a specific technology.
- Candidate explains a system-design trade-off.
- Candidate provides a concrete behavioral example.

#### Supported Inference

A reasonable conclusion derived from multiple pieces of explicit evidence.

Examples:

- Repeated successful solutions suggest improving proficiency in a particular DSA topic.
- Multiple interviews demonstrate consistent communication strengths.
- Repeated difficulty with complexity analysis provides evidence of a recurring weakness.

Supported inference must remain distinguishable from directly observed evidence.

#### Missing Evidence

A competency for which the platform does not have sufficient evidence.

Missing evidence must not automatically be interpreted as a weakness.

For example:

> If a candidate has never been evaluated on dynamic programming, the system should represent DP as "insufficient evidence" rather than automatically marking the candidate as weak in DP.

### 3.3 Evidence Attributes

Each evidence record should contain, where applicable:

- Evidence ID.
- Candidate ID.
- Evidence source.
- Evidence type.
- Competency ID.
- Related target ID.
- Related assessment or interview ID.
- Original evidence reference.
- Extracted evidence statement.
- Timestamp.
- Evaluation status.
- Confidence.
- Evidence strength.
- Supporting metadata.

The exact persistence model will be finalized during the data-model design phase.

### 3.4 Evidence Traceability

Every important evaluation result should be traceable back to the evidence that contributed to it.

The relationship should conceptually follow:

Candidate Input
→ Evidence
→ Evaluation
→ Skill State
→ Skill Gap
→ Recommendation

For example:

```text
Coding Response
      ↓
Evidence:
"Candidate selected BFS and correctly explained
time complexity, but could not justify the
visited-set implementation."
      ↓
Evaluation:
Graph Traversal = Developing
      ↓
Skill State Update
      ↓
Skill Gap:
Graph implementation consistency
      ↓
Next Best Action:
Practice graph traversal implementation
```
This traceability allows the candidate to understand why the system reached a particular conclusion.

### 3.5 Evidence Strength

Evidence should have a strength classification based on the quality and directness of the demonstration.

A proposed classification is:

- Strong
- Moderate
- Weak
- Insufficient

Evidence strength should consider factors such as:

- Directness of demonstration
- Completeness
- Correctness
- Consistency
- Relevance to the target competency
- Quality of supporting information

Evidence strength should not be determined solely by the LLM without applying the defined evaluation rules.

### 3.6 Evidence Recency

Evidence may become more or less representative of the candidate's current state over time.

The system should therefore retain the original evidence while allowing recent evidence to have greater relevance when calculating current skill state, where appropriate.

Historical evidence must never be deleted merely because newer evidence exists.

For example:
```text
January
Graph skill → Developing


March
Graph skill → Proficient


May
Graph skill → Strong
```
The platform should preserve all three observations while identifying the May result as the most recent state.

### 3.7 Repeated Evidence

Repeated demonstrations of a competency can provide stronger evidence than a single observation.

For example:
```text
Assessment 1 → Graphs → Weak
Assessment 2 → Graphs → Developing
Assessment 3 → Graphs → Proficient
```
This sequence provides evidence of improvement.

However, repeated assessments should not blindly accumulate into an inflated score.

The system should consider:

- Recency
- Consistency
- Assessment quality
- Evidence strength
- Target competency
- Context of the assessment

### 3.8 Conflicting Evidence

Candidate evidence may sometimes conflict.

For example:
```text
Interview 1 → Strong understanding of trees
Interview 2 → Difficulty with tree traversal
```
The system should not arbitrarily discard either observation.

Instead, conflicting evidence should be retained and reflected in the resulting confidence or skill-state assessment.

Possible interpretation:
```text
"Current evidence is mixed. The candidate has demonstrated strong conceptual understanding but inconsistent implementation performance."
```
### 3.9 Evidence and Target Context

Evidence should be interpreted relative to the candidate's selected target.

The same evidence may have different implications depending on:

- Target role
- Target level
- Target company
- Job description
- Required competency

For example, basic system-design knowledge may be sufficient evidence for an SDE-1 target but insufficient evidence for an SDE-3 target.

### 3.10 Evidence for Skill-State Updates

Evidence should not directly overwrite a candidate's skill state.

The conceptual flow is:
```text
Evidence
   ↓
Evaluation
   ↓
Confidence + Evidence Coverage
   ↓
Skill-State Update Rules
   ↓
Current Skill State
```
This separation ensures that the current skill state remains a derived representation rather than an arbitrary AI-generated value.

### 3.11 Evidence for Recommendations

Recommendations should be based on the candidate's current evidence and target requirements.

The recommendation flow is:
```text
Target Requirements
        +
Candidate Evidence
        ↓
Current Skill State
        ↓
Skill Gaps
        ↓
Priority
        ↓
Next Best Action
```
The system should be able to explain why a recommendation was generated.

For example:
```text
"Practice graph traversal problems because recent coding assessments show inconsistent BFS/DFS implementation and the target SDE-1 competency profile requires stronger graph problem-solving."
```
### 3.12 Evidence Privacy

Candidate evidence may contain sensitive personal or professional information.

The platform should:

- Store only required candidate information.
- Avoid unnecessary logging of raw interview responses.
- Avoid exposing candidate data to unrelated users.
- Avoid placing candidate content in application logs where possible.
- Follow the project's authentication, authorization, and data-retention rules.
- Never use confidential employer information as test data.

### 3.13 Evidence Quality Guardrail

The system must distinguish between:

- No evidence.
- Weak evidence.
- Strong evidence.
- Contradictory evidence.

The absence of evidence must never automatically become a negative evaluation.

The platform should communicate uncertainty when the available evidence is insufficient to support a strong conclusion.

## 4. Competency Model

The Competency Model defines the capabilities that Career-Intelligence-Platform evaluates for Software Development Engineer candidates.

The model should be configurable so that competency expectations can vary based on:

- Target role.
- Target level.
- Target company, when applicable.
- Job description requirements.
- Assessment type.

The platform should avoid hard-coding a single universal definition of interview readiness.

### 4.1 Primary Competency Areas

The initial SDE competency model contains:

- Coding / Data Structures and Algorithms.
- Computer Science Fundamentals.
- System Design.
- Behavioral / Communication.
- Ownership and Problem Solving.
- Technical Leadership.
- Architecture.

Not every competency has equal importance for every target level.

### 4.2 Coding / Data Structures and Algorithms

The Coding / DSA competency may include:

- Arrays.
- Strings.
- Hashing.
- Two Pointers.
- Sliding Window.
- Stack and Queue.
- Linked Lists.
- Binary Search.
- Sorting.
- Trees.
- Binary Search Trees.
- Heaps / Priority Queues.
- Graphs.
- Greedy Algorithms.
- Backtracking.
- Dynamic Programming.
- Recursion.
- Bit Manipulation.

The competency model should support topic-level tracking so that the system can identify specific gaps rather than reporting only a broad "DSA weakness."

For example:

```text
Coding / DSA
├── Arrays → Proficient
├── Trees → Developing
├── Graphs → Weak
└── Dynamic Programming → Insufficient Evidence
```

### 4.3 Computer Science Fundamentals

The initial CS Fundamentals competency may include:

- Object-Oriented Programming
- Operating Systems
- Database Management Systems
- Computer Networks
- SQL
- Concurrency / Multithreading
- Software Engineering principles

The exact competency list may be expanded based on target role and job-description requirements.

### 4.4 System Design

System Design may include:

- Requirement clarification
- Functional requirements
- Non-functional requirements
- Scalability
- Availability
- Reliability
- Data modeling
- API design
- Caching
- Databases
- Message queues
- Load balancing
- Distributed-system concepts
- Trade-off analysis
- Capacity estimation

System-design expectations must be adjusted according to target level.

For example:
```text
SDE-1 → Basic / foundational system-design expectations
SDE-2 → Strong system-design expectations
SDE-3 → Advanced architecture and distributed-system expectations
```
### 4.5 Behavioral and Communication

Behavioral evaluation may include:

- Communication
- Collaboration
- Conflict handling
- Ownership
- Problem solving
- Adaptability
- Learning ability
- Handling failure
- Decision making
- Impact and results

Behavioral evaluation should focus on demonstrated examples rather than personality judgments.

### 4.6 Ownership

Ownership represents the candidate's ability to:

- Take responsibility for outcomes
- Identify and solve problems
- Drive work to completion
- Handle ambiguity
- Make appropriate technical decisions
- Learn from failures
- Consider operational impact

Ownership expectations should increase with seniority.

### 4.7 Technical Leadership

Technical Leadership may include:

- Technical decision making
- Mentoring
- Influencing technical direction
- Cross-team collaboration
- Driving engineering improvements
- Handling technical ambiguity
- Communicating technical trade-offs

Technical leadership should have limited importance for SDE-1 and progressively greater importance for SDE-2 and SDE-3.

### 4.8 Architecture

Architecture represents the ability to reason about larger technical systems.

It may include:

- Architectural decomposition.
- Service boundaries.
- Distributed systems.
- Scalability.
- Reliability.
- Availability.
- Maintainability.
- Technology trade-offs.
- Long-term technical decisions.

Architecture expectations should be strongly level-dependent.

### 4.9 Level-Based Expectations

The initial model uses the following high-level expectations:

| Capability           | SDE-1        | SDE-2       | SDE-3     |
|-----------------------|--------------|-------------|-----------|
| Coding / DSA          | High         | High        | High      |
| CS Fundamentals       | High         | Medium/High | Medium    |
| System Design         | Basic/Medium | High        | Very High |
| Behavioral             | High         | High        | High      |
| Ownership              | Medium       | High        | Very High |
| Technical Leadership   | Low/Medium   | Medium      | High      |
| Architecture           | Basic        | High        | Very High |

These values represent expected importance and depth, not candidate scores.

They must not be interpreted as direct percentages or hiring probabilities.

### 4.10 Target-Specific Competencies

The competency model should support a hierarchy of expectations:
```text
Target
│
├── Role
│   └── SDE
│
├── Level
│   └── SDE-1
│
├── Company
│   └── Optional
│
└── Job Description
    └── Optional
```
The system should use the most specific reliable information available.

For example:
```text
Generic SDE
      ↓
SDE-1 competency profile


Google + SDE-1
      ↓
Company + level context
      ↓
Google-specific requirements when supported


Google + SDE-1 + specific JD
      ↓
JD requirements
      ↓
Target-specific competency profile
```
Company-specific expectations must be based on approved or provided information.

The AI must not invent company-specific interview requirements.

### 4.11 Competency Proficiency Levels

Each competency may have a current candidate proficiency state.

The initial proficiency states are:

- Insufficient Evidence
- Weak
- Developing
- Proficient
- Strong

These states describe demonstrated capability and available evidence.

They are not hiring decisions.

### 4.12 Topic-Level Competency

Competencies should support hierarchical decomposition.
```text
For example:

Coding / DSA
│
├── Arrays
├── Strings
├── Linked Lists
├── Trees
│   ├── Traversal
│   ├── BST
│   └── Tree DP
├── Graphs
│   ├── BFS
│   ├── DFS
│   ├── Shortest Path
│   └── Union Find
└── Dynamic Programming
    ├── 1D DP
    ├── 2D DP
    ├── Knapsack
    └── Subsequences
```
This enables the platform to identify specific learning and assessment priorities.

### 4.13 Competency Expectations vs Candidate State

The platform must distinguish between:

#### Expected competency

What the target requires.

and:

#### Candidate competency state

What the candidate has demonstrated.

The conceptual comparison is:
```text
Target Competency
       +
Candidate Skill State
       ↓
Skill Gap
```
For example:
```text
Target:
Graphs → Proficient


Candidate:
Graphs → Developing


Result:
Graph competency gap
```
If the candidate has not been assessed:
```text
Target:
Dynamic Programming → Proficient


Candidate:
Dynamic Programming → Insufficient Evidence


Result:
Insufficient evidence
→ Assessment recommended
```
The system should not automatically classify insufficient evidence as a skill weakness.

### 4.14 Competency Configuration

Competency definitions should be stored as configurable reference data rather than embedded throughout application code.

Reference data may contain:

- Competency ID
- Competency name
- Parent competency
- Description
- Applicable roles
- Applicable levels
- Expected proficiency
- Importance / weight
- Assessment types
- Related skills or topics

This allows the competency model to evolve without requiring major application-code changes.

### 4.15 Competency Model Guardrails

The competency model must:

- Avoid unsupported company-specific assumptions.
- Avoid treating all SDE levels identically.
- Avoid reducing readiness to a single DSA score.
- Preserve topic-level visibility.
- Distinguish expected capability from demonstrated capability.
- Preserve insufficient-evidence states.
- Support historical changes in candidate competency.
- Remain configurable as the product evolves.

## 5. Score Scale

The platform uses a structured proficiency scale to represent demonstrated candidate capability.

The primary candidate-facing proficiency states are:

- Insufficient Evidence.
- Weak.
- Developing.
- Proficient.
- Strong.

These states represent demonstrated capability against a defined competency and target context.

They are not hiring decisions and must not be interpreted as probabilities of interview success or employment.

### 5.1 Proficiency Levels

| Level | Meaning |
|---|---|
| Insufficient Evidence | The available evidence is not sufficient to make a reliable assessment of the competency. |
| Weak | The candidate has demonstrated significant gaps and requires substantial improvement for the target expectation. |
| Developing | The candidate demonstrates partial understanding or capability but performance is inconsistent or incomplete. |
| Proficient | The candidate consistently demonstrates the expected capability for the target context. |
| Strong | The candidate demonstrates capability beyond the expected baseline, with strong consistency, reasoning, and execution. |

### 5.2 Insufficient Evidence

Insufficient Evidence means the platform does not have enough relevant evidence to confidently assess the competency.

Examples include:

- The competency has not been assessed.
- The candidate was not given an opportunity to demonstrate the competency.
- The available response is too incomplete.
- The evidence is highly ambiguous.
- The evidence is contradictory without enough additional information to resolve the contradiction.

Insufficient Evidence must not be converted automatically into Weak.

For example:

```text
Dynamic Programming
Candidate State → Insufficient Evidence
```

means:

> "The platform does not yet have enough evidence to assess Dynamic Programming."

It does not mean:

> "The candidate is weak in Dynamic Programming."

### 5.3 Weak

Weak indicates that the candidate has demonstrated meaningful difficulty with the competency.

Typical characteristics may include:

- Fundamental concepts are missing or misunderstood.
- The candidate cannot independently apply the relevant concept.
- The solution contains major correctness issues.
- The candidate requires substantial assistance.
- Reasoning is incomplete or technically incorrect.
- Performance is consistently below the target expectation.

Weak should be assigned only when sufficient evidence exists.

### 5.4 Developing

Developing indicates partial capability.

Typical characteristics may include:

- Basic concepts are understood.
- The candidate can solve simpler cases.
- The candidate can make progress but struggles with complexity or edge cases.
- The candidate requires occasional guidance.
- Performance is inconsistent across related tasks.
- The candidate demonstrates improvement but has not yet reached consistent proficiency.

Developing represents a meaningful intermediate state rather than a failure.

### 5.5 Proficient

Proficient indicates that the candidate consistently demonstrates the expected capability for the target context.

Typical characteristics may include:

- Correct understanding of relevant concepts.
- Appropriate approach selection.
- Correct or mostly correct execution.
- Appropriate handling of edge cases.
- Reasonable complexity analysis.
- Independent problem solving.
- Clear enough technical communication.

Proficient is relative to the target role and level.

For example:
```text
SDE-1 Target
Graphs → Proficient
```
does not necessarily mean the candidate meets an SDE-3 graph competency expectation.

### 5.6 Strong

Strong indicates demonstrated capability above the expected baseline for the target context.

Typical characteristics may include:

```text
Strong conceptual understanding.
Consistent independent execution.
Effective handling of difficult or unfamiliar cases.
Clear trade-off reasoning.
Strong complexity analysis.
High-quality implementation.
Effective communication.
Ability to generalize knowledge to related problems.
```
Strong should require sufficient evidence and should not be awarded simply because an answer is correct.

### 5.7 Numerical Scores

The platform may use numerical scores internally to support dimension-level aggregation and progress tracking.

A proposed internal scale is:

| Proficiency            | Internal Score Range |
|------------------------|----------------------:|
| Insufficient Evidence   | No score               |
| Weak                    | 0–39                   |
| Developing              | 40–59                  |
| Proficient              | 60–79                  |
| Strong                  | 80–100                 |

These ranges are internal evaluation representations and are not hiring probabilities.

The exact thresholds may be refined during implementation and validation.

### 5.8 Score Interpretation

A numerical score should never be treated as meaningful without its associated evidence.

For example:
```text
Graphs
Score: 58
State: Developing
Confidence: High
Evidence Coverage: Strong
```
is more informative than:
```text
Overall Score: 58
```
The system should therefore retain the following together where applicable:

- Score
- Proficiency state
- Evidence
- Confidence
- Evidence coverage
- Evaluation dimensions
- Target competency

### 5.9 Dimension-Level Scoring

Interview evaluations should primarily produce scores at the evaluation-dimension level.

For example:
```text
Coding Interview

Problem Understanding     → 80
Approach                   → 75
Algorithm Selection       → 70
Correctness               → 65
Complexity Analysis       → 55
Code Quality              → 72
Communication             → 78
```
The application may then aggregate these values using predefined weights.

The LLM must not independently invent the final weighted score.

### 5.10 Deterministic Score Aggregation

Where a numerical overall score is required, the application should calculate it using predefined weights.

Conceptually:
```text
Overall Score =
    Dimension 1 × Weight 1
  + Dimension 2 × Weight 2
  + Dimension 3 × Weight 3
  + ...
```
The weights must be defined by the applicable evaluation rubric.

The application, rather than the LLM, should perform the final mathematical aggregation.

### 5.11 Score-to-Proficiency Mapping

After deterministic aggregation, the resulting score may be mapped to the defined proficiency state.

Conceptually:
```text
0–39    → Weak
40–59   → Developing
60–79   → Proficient
80–100  → Strong
```
However, the system must first verify that sufficient evidence exists.

If evidence is insufficient:
```text
Score → Not Assigned
State → Insufficient Evidence
```
This prevents an absence of evidence from becoming an artificially low score.

### 5.12 Score Does Not Equal Readiness

A competency score is not equivalent to overall interview readiness.

For example:
```text
Coding → 82
System Design → 45
Behavioral → 70
```
should not automatically result in:
```text
Overall Readiness → 65
```
unless the defined readiness model explicitly supports that calculation.

Readiness will be defined separately in the Readiness Model section.

### 5.13 Score Comparability

Scores should be compared over time only when the evaluated competency and evaluation context are sufficiently comparable.

For example:
```text
Graph Interview #1 → 48
Graph Interview #2 → 65
Graph Interview #3 → 76
```
may provide evidence of improvement when the assessments evaluate comparable competency dimensions.

The platform should avoid claiming precise improvement when:

- Different competencies were evaluated.
- Evidence quality differs substantially.
- The target level changed.
- The evaluation context changed significantly.
- Evidence coverage is insufficient.

### 5.14 Score Guardrails

The evaluation system must:

- Never treat missing evidence as Weak.
- Never generate unsupported hiring probabilities.
- Never allow the LLM to bypass predefined scoring rules.
- Preserve evidence associated with each score.
- Preserve historical scores.
- Apply deterministic aggregation.
- Clearly distinguish competency scores from overall readiness.
- Consider confidence and evidence coverage.
- Keep score thresholds configurable.
- Avoid presenting internal scores as objective measurements of a person's overall ability.

