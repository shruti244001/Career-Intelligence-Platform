import { useRef, useState } from "react";
import "./App.css";

interface CandidateProfile {
  id: string;
  candidate_id: string;
  name: string;
  email: string | null;
  education: string[];
  years_of_experience: number;
  skills: string[];
  technologies: string[];
  projects: string[];
  summary: string | null;
  resume_reference?: string | null;
}

interface TargetProfile {
  id: string;
  candidate_id: string;
  role: string;
  level: string;
  company: string | null;
  job_description_id: string | null;
  active: boolean;
}

interface SkillGap {
  competency_id: string;
  competency_name: string;
  classification: string;
  current_proficiency: string;
  expected_proficiency: string;
  priority: string | null;
  rationale: string | null;
}

interface Recommendation {
  id: string;
  competency_id: string;
  source_gap_id: string;
  priority: string;
  action_type: string;
  title: string;
  rationale: string;
  rank: number;
}

interface SkillGapAnalysis {
  target_id: string;
  candidate_id: string;
  assessment_type: string;
  skill_gaps: SkillGap[];
  recommendations: Recommendation[];
}

function formatLabel(value: string | null) {
  if (!value) {
    return "�";
  }

  return value
    .replaceAll("_", " ")
    .replace(/\b\w/g, (character) => character.toUpperCase());
}

function App() {
  const [candidate, setCandidate] = useState<CandidateProfile | null>(null);
  const [target, setTarget] = useState<TargetProfile | null>(null);
  const [skillGapAnalysis, setSkillGapAnalysis] =
    useState<SkillGapAnalysis | null>(null);

  const [role, setRole] = useState("Software Engineer");
  const [level, setLevel] = useState("SDE-1");
  const [company, setCompany] = useState("");

  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [targetLoading, setTargetLoading] = useState(false);
  const [skillGapLoading, setSkillGapLoading] = useState(false);

  const [error, setError] = useState("");
  const [targetError, setTargetError] = useState("");
  const [skillGapError, setSkillGapError] = useState("");
  const [success, setSuccess] = useState("");

  const fileInputRef = useRef<HTMLInputElement | null>(null);

  const API_BASE_URL =
    import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

  const fetchSkillGapAnalysis = async (targetId: string) => {
    setSkillGapLoading(true);
    setSkillGapError("");

    try {
      const response = await fetch(
        `${API_BASE_URL}/api/v1/targets/${targetId}/skill-gaps`,
      );

      if (!response.ok) {
        let message = `Skill-gap analysis failed with status ${response.status}`;

        try {
          const data = await response.json();

          if (typeof data.detail === "string") {
            message = data.detail;
          }
        } catch {
          // Keep the default error message.
        }

        throw new Error(message);
      }

      const data: SkillGapAnalysis = await response.json();

      setSkillGapAnalysis(data);
      setSuccess("Skill-gap analysis generated successfully.");
    } catch (err) {
      setSkillGapError(
        err instanceof Error
          ? err.message
          : "Unable to generate skill-gap analysis.",
      );
    } finally {
      setSkillGapLoading(false);
    }
  };

  const uploadResume = async () => {
    if (!selectedFile) {
      setError("Please select a resume first.");
      return;
    }

    setLoading(true);
    setError("");
    setSuccess("");
    setCandidate(null);
    setTarget(null);
    setSkillGapAnalysis(null);
    setSkillGapError("");

    try {
      const candidateId = crypto.randomUUID();

      const formData = new FormData();
      formData.append("candidate_id", candidateId);
      formData.append("file", selectedFile);

      const response = await fetch(
        `${API_BASE_URL}/api/v1/resumes/extract-profile`,
        {
          method: "POST",
          body: formData,
        },
      );

      if (!response.ok) {
        let message = `Resume upload failed with status ${response.status}`;

        try {
          const data = await response.json();

          if (typeof data.detail === "string") {
            message = data.detail;
          }
        } catch {
          // Keep the default error message.
        }

        throw new Error(message);
      }

      const data: CandidateProfile = await response.json();

      setCandidate(data);
      setSuccess("Resume processed successfully.");
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Unable to process the resume. Make sure the backend is running.",
      );
    } finally {
      setLoading(false);
    }
  };

  const createTarget = async () => {
    if (!candidate) {
      return;
    }

    setTargetLoading(true);
    setTargetError("");
    setSkillGapError("");
    setSuccess("");

    try {
      const response = await fetch(`${API_BASE_URL}/api/v1/targets`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          candidate_id: candidate.candidate_id,
          role,
          level,
          company: company || null,
          job_description_id: null,
        }),
      });

      if (!response.ok) {
        let message = `Target creation failed with status ${response.status}`;

        try {
          const data = await response.json();

          if (typeof data.detail === "string") {
            message = data.detail;
          }
        } catch {
          // Keep the default error message.
        }

        throw new Error(message);
      }

      const data: TargetProfile = await response.json();

      setTarget(data);
      setSuccess("Target profile created. Generating skill-gap analysis...");

      await fetchSkillGapAnalysis(data.id);
    } catch (err) {
      setTargetError(
        err instanceof Error
          ? err.message
          : "Unable to create target profile. Make sure the backend is running.",
      );
    } finally {
      setTargetLoading(false);
    }
  };

  const handleFileChange = (
    event: React.ChangeEvent<HTMLInputElement>,
  ) => {
    const file = event.target.files?.[0] ?? null;

    setSelectedFile(file);
    setError("");
    setSuccess("");
  };

  const resetWorkspace = () => {
    setCandidate(null);
    setTarget(null);
    setSkillGapAnalysis(null);
    setSelectedFile(null);
    setError("");
    setTargetError("");
    setSkillGapError("");
    setSuccess("");

    if (fileInputRef.current) {
      fileInputRef.current.value = "";
    }
  };

  return (
    <div className="app">
      <header className="topbar">
        <div>
          <h1>CareerGraph AI</h1>
          <p>Evidence-based interview readiness</p>
        </div>

        <div className="status">
          <span className="status-dot" />
          Local Development
        </div>
      </header>

      <main className="content">
        <section className="hero">
          <p className="eyebrow">CAREER READINESS PLATFORM</p>

          <h2>Build your interview readiness graph.</h2>

          <p>
            Upload your resume to create an evidence-based candidate profile,
            choose a target role, and prepare for the skills that matter.
          </p>
        </section>

        {!candidate && (
          <section className="card upload-card">
            <div className="card-header">
              <div>
                <h3>Start with your resume</h3>
                <p>
                  CareerGraph will extract your profile from your resume and
                  persist it as your candidate state.
                </p>
              </div>
            </div>

            <div
              className="upload-area"
              onClick={() => fileInputRef.current?.click()}
              role="button"
              tabIndex={0}
              onKeyDown={(event) => {
                if (event.key === "Enter" || event.key === " ") {
                  fileInputRef.current?.click();
                }
              }}
            >
              <div className="upload-icon">?</div>

              <h4>
                {selectedFile
                  ? selectedFile.name
                  : "Upload your resume"}
              </h4>

              <p>
                {selectedFile
                  ? `${(selectedFile.size / 1024).toFixed(1)} KB selected`
                  : "PDF, DOCX, or TXT"}
              </p>

              <input
                ref={fileInputRef}
                type="file"
                accept=".pdf,.docx,.txt"
                onChange={handleFileChange}
                hidden
              />
            </div>

            {selectedFile && (
              <div className="selected-file">
                <div>
                  <strong>{selectedFile.name}</strong>
                  <span>
                    {selectedFile.type || "Resume file"} �{" "}
                    {(selectedFile.size / 1024).toFixed(1)} KB
                  </span>
                </div>

                <button
                  type="button"
                  className="secondary-button"
                  onClick={() => {
                    setSelectedFile(null);

                    if (fileInputRef.current) {
                      fileInputRef.current.value = "";
                    }
                  }}
                >
                  Remove
                </button>
              </div>
            )}

            {error && <div className="error">{error}</div>}

            {success && <div className="success">{success}</div>}

            <button
              className="primary-button"
              onClick={uploadResume}
              disabled={loading || !selectedFile}
            >
              {loading ? "Processing Resume..." : "Build My Profile"}
            </button>

            <p className="upload-note">
              Supported formats: PDF, DOCX, TXT. No AI provider is required
              for this step.
            </p>
          </section>
        )}

        {candidate && (
          <>
            <section className="workspace">
              <div className="card">
                <div className="card-header">
                  <div>
                    <h3>Candidate Profile</h3>
                    <p>
                      Extracted from your uploaded resume and persisted by
                      CareerGraph.
                    </p>
                  </div>
                </div>

                <div className="profile-heading">
                  <div className="avatar">
                    {candidate.name.charAt(0).toUpperCase()}
                  </div>

                  <div>
                    <h4>{candidate.name}</h4>
                    <p>
                      {candidate.email ?? "No email found in resume"}
                    </p>
                  </div>
                </div>

                <div className="stat-grid">
                  <div>
                    <span>Experience</span>
                    <strong>
                      {candidate.years_of_experience} years
                    </strong>
                  </div>

                  <div>
                    <span>Skills</span>
                    <strong>{candidate.skills.length}</strong>
                  </div>

                  <div>
                    <span>Technologies</span>
                    <strong>{candidate.technologies.length}</strong>
                  </div>
                </div>

                {candidate.education.length > 0 && (
                  <div className="profile-section">
                    <span>Education</span>

                    <div className="tags">
                      {candidate.education.map((item) => (
                        <span key={item}>{item}</span>
                      ))}
                    </div>
                  </div>
                )}

                {candidate.skills.length > 0 && (
                  <div className="profile-section">
                    <span>Skills</span>

                    <div className="tags">
                      {candidate.skills.map((skill) => (
                        <span key={skill}>{skill}</span>
                      ))}
                    </div>
                  </div>
                )}

                {candidate.technologies.length > 0 && (
                  <div className="profile-section">
                    <span>Technologies</span>

                    <div className="tags">
                      {candidate.technologies.map((technology) => (
                        <span key={technology}>{technology}</span>
                      ))}
                    </div>
                  </div>
                )}

                {candidate.projects.length > 0 && (
                  <div className="profile-section">
                    <span>Projects</span>

                    <div className="tags">
                      {candidate.projects.map((project) => (
                        <span key={project}>{project}</span>
                      ))}
                    </div>
                  </div>
                )}

                {candidate.summary && (
                  <div className="summary">
                    <span>Professional Summary</span>
                    <p>{candidate.summary}</p>
                  </div>
                )}

                {candidate.resume_reference && (
                  <div className="resume-status">
                    <span className="status-dot" />
                    Resume stored successfully
                  </div>
                )}

                <button
                  type="button"
                  className="secondary-button reset-button"
                  onClick={resetWorkspace}
                >
                  Upload Different Resume
                </button>
              </div>

              <div className="card profile-preview">
                <div className="card-header">
                  <div>
                    <h3>CareerGraph State</h3>
                    <p>Your current candidate evidence state.</p>
                  </div>
                </div>

                <div className="state-item">
                  <span>Candidate</span>
                  <strong>Created</strong>
                </div>

                <div className="state-item">
                  <span>Resume</span>
                  <strong>Processed</strong>
                </div>

                <div className="state-item">
                  <span>Profile</span>
                  <strong>Persisted</strong>
                </div>

                <div className="state-item">
                  <span>Target</span>
                  <strong>
                    {target ? "Configured" : "Not configured"}
                  </strong>
                </div>

                <div className="state-item">
                  <span>Skill Gap</span>
                  <strong>
                    {skillGapAnalysis ? "Analyzed" : "Pending"}
                  </strong>
                </div>

                <div className="graph-next">
                  <span>Next step</span>
                  <strong>
                    {skillGapAnalysis
                      ? "Prioritize your next best actions"
                      : target
                        ? "Generating skill-gap analysis"
                        : "Define your target role"}
                  </strong>
                </div>
              </div>
            </section>

            {!target && (
              <section className="card target-card">
                <div className="card-header">
                  <div>
                    <h3>Target Profile</h3>
                    <p>
                      Define the role you are preparing for. This becomes the
                      baseline for skill-gap analysis.
                    </p>
                  </div>
                </div>

                <div className="form-grid">
                  <label>
                    Target Role

                    <input
                      value={role}
                      onChange={(event) => setRole(event.target.value)}
                      placeholder="Software Engineer"
                    />
                  </label>

                  <label>
                    Target Level

                    <select
                      value={level}
                      onChange={(event) => setLevel(event.target.value)}
                    >
                      <option value="SDE-1">SDE-1</option>
                      <option value="SDE-2">SDE-2</option>
                      <option value="SDE-3">SDE-3</option>
                    </select>
                  </label>

                  <label className="full-width">
                    Company

                    <input
                      value={company}
                      onChange={(event) => setCompany(event.target.value)}
                      placeholder="Optional � e.g. Google"
                    />

                    <span>
                      Leave blank for a general target profile.
                    </span>
                  </label>
                </div>

                {targetError && (
                  <div className="error">{targetError}</div>
                )}

                <button
                  className="primary-button"
                  onClick={createTarget}
                  disabled={
                    targetLoading ||
                    !role.trim() ||
                    !level.trim()
                  }
                >
                  {targetLoading
                    ? "Analyzing Readiness..."
                    : "Create Target & Analyze Skills"}
                </button>
              </section>
            )}

            {target && (
              <section className="card target-card">
                <div className="card-header">
                  <div>
                    <h3>Target Profile</h3>
                    <p>
                      Your target is now part of the CareerGraph state.
                    </p>
                  </div>
                </div>

                <div className="profile-heading">
                  <div className="avatar">?</div>

                  <div>
                    <h4>
                      {target.role} � {target.level}
                    </h4>

                    <p>
                      {target.company
                        ? `Targeting ${target.company}`
                        : "General target profile"}
                    </p>
                  </div>
                </div>

                <div className="stat-grid">
                  <div>
                    <span>Role</span>
                    <strong>{target.role}</strong>
                  </div>

                  <div>
                    <span>Level</span>
                    <strong>{target.level}</strong>
                  </div>

                  <div>
                    <span>Status</span>
                    <strong>
                      {target.active ? "Active" : "Inactive"}
                    </strong>
                  </div>
                </div>

                <div className="success">
                  Target profile created successfully.
                </div>
              </section>
            )}

            {target && (
              <section className="skill-gap-section">
                <div className="card">
                  <div className="card-header">
                    <div>
                      <p className="eyebrow">READINESS ANALYSIS</p>
                      <h3>Skill Gap Analysis</h3>
                      <p>
                        CareerGraph compares your current evidence against
                        the competency expectations for your target role.
                      </p>
                    </div>

                    {skillGapAnalysis && (
                      <div className="resume-status">
                        <span className="status-dot" />
                        Analysis complete
                      </div>
                    )}
                  </div>

                  {skillGapLoading && (
                    <div className="empty-state">
                      <h4>Analyzing your readiness...</h4>
                      <p>
                        Comparing your current evidence with the target
                        competency baseline.
                      </p>
                    </div>
                  )}

                  {skillGapError && (
                    <div className="error">{skillGapError}</div>
                  )}

                  {skillGapAnalysis && (
                    <>
                      <div className="stat-grid">
                        <div>
                          <span>Competencies assessed</span>
                          <strong>
                            {skillGapAnalysis.skill_gaps.length}
                          </strong>
                        </div>

                        <div>
                          <span>Evidence gaps</span>
                          <strong>
                            {
                              skillGapAnalysis.skill_gaps.filter(
                                (gap) =>
                                  gap.classification ===
                                  "insufficient_evidence",
                              ).length
                            }
                          </strong>
                        </div>

                        <div>
                          <span>Next best actions</span>
                          <strong>
                            {skillGapAnalysis.recommendations.length}
                          </strong>
                        </div>
                      </div>

                      <div className="skill-gap-list">
                        {skillGapAnalysis.skill_gaps.map((gap) => (
                          <div
                            className="skill-gap-item"
                            key={gap.competency_id}
                          >
                            <div className="skill-gap-heading">
                              <div>
                                <h4>{gap.competency_name}</h4>
                                <p>
                                  {gap.rationale ||
                                    "Current evidence has been assessed against the target expectation."}
                                </p>
                              </div>

                              <span
                                className={`gap-status ${gap.classification}`}
                              >
                                {formatLabel(gap.classification)}
                              </span>
                            </div>

                            <div className="skill-gap-meta">
                              <div>
                                <span>Current</span>
                                <strong>
                                  {formatLabel(gap.current_proficiency)}
                                </strong>
                              </div>

                              <div>
                                <span>Target</span>
                                <strong>
                                  {formatLabel(gap.expected_proficiency)}
                                </strong>
                              </div>

                              <div>
                                <span>Priority</span>
                                <strong>
                                  {formatLabel(gap.priority)}
                                </strong>
                              </div>
                            </div>
                          </div>
                        ))}
                      </div>
                    </>
                  )}
                </div>

                {skillGapAnalysis &&
                  skillGapAnalysis.recommendations.length > 0 && (
                    <div className="card">
                      <div className="card-header">
                        <div>
                          <p className="eyebrow">NEXT BEST ACTION</p>
                          <h3>What to work on next</h3>
                          <p>
                            Recommendations are ranked from the current skill
                            gaps and target importance.
                          </p>
                        </div>
                      </div>

                      <div className="recommendation-list">
                        {skillGapAnalysis.recommendations.map(
                          (recommendation) => {
                            const competency = skillGapAnalysis.skill_gaps.find(
                              (gap) =>
                                gap.competency_id ===
                                recommendation.competency_id,
                            );

                            return (
                              <div
                                className="recommendation-item"
                                key={recommendation.id}
                              >
                                <div className="recommendation-rank">
                                  {recommendation.rank}
                                </div>

                                <div>
                                  <div className="skill-gap-heading">
                                    <div>
                                      <h4>{recommendation.title}</h4>
                                      <p>
                                        {competency?.competency_name ||
                                          "Target competency"}
                                      </p>
                                    </div>

                                    <span
                                      className={`gap-status ${recommendation.priority}`}
                                    >
                                      {formatLabel(recommendation.priority)}
                                    </span>
                                  </div>

                                  <p className="recommendation-rationale">
                                    {recommendation.rationale}
                                  </p>
                                </div>
                              </div>
                            );
                          },
                        )}
                      </div>
                    </div>
                  )}
              </section>
            )}
          </>
        )}
      </main>
    </div>
  );
}

export default App;
