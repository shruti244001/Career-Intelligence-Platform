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
