import { useState } from "react";
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

function App() {
  const [candidate, setCandidate] = useState<CandidateProfile | null>(null);
  const [target, setTarget] = useState<TargetProfile | null>(null);

  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [education, setEducation] = useState("");
  const [experience, setExperience] = useState("0");
  const [skills, setSkills] = useState("");
  const [technologies, setTechnologies] = useState("");
  const [projects, setProjects] = useState("");
  const [summary, setSummary] = useState("");

  const [role, setRole] = useState("Software Engineer");
  const [level, setLevel] = useState("SDE-1");
  const [company, setCompany] = useState("");

  const [loading, setLoading] = useState(false);
  const [targetLoading, setTargetLoading] = useState(false);
  const [error, setError] = useState("");
  const [targetError, setTargetError] = useState("");

  const createCandidate = async () => {
    setLoading(true);
    setError("");

    try {
      const response = await fetch("http://127.0.0.1:8000/candidates", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          name,
          email: email || null,
          education: education
            .split(",")
            .map((item) => item.trim())
            .filter(Boolean),
          years_of_experience: Number(experience),
          skills: skills
            .split(",")
            .map((item) => item.trim())
            .filter(Boolean),
          technologies: technologies
            .split(",")
            .map((item) => item.trim())
            .filter(Boolean),
          projects: projects
            .split(",")
            .map((item) => item.trim())
            .filter(Boolean),
          summary: summary || null,
        }),
      });

      if (!response.ok) {
        throw new Error(`Request failed with status ${response.status}`);
      }

      const data: CandidateProfile = await response.json();
      setCandidate(data);
    } catch {
      setError(
        "Unable to create candidate profile. Make sure the backend is running.",
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

    try {
      const response = await fetch("http://127.0.0.1:8000/api/v1/targets", {
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
        throw new Error(`Request failed with status ${response.status}`);
      }

      const data: TargetProfile = await response.json();
      setTarget(data);
    } catch {
      setTargetError(
        "Unable to create target profile. Make sure the backend is running.",
      );
    } finally {
      setTargetLoading(false);
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
            Create your candidate profile, select a target role, and build an
            evidence-based path toward interview readiness.
          </p>
        </section>

        <section className="workspace">
          <div className="card">
            <div className="card-header">
              <div>
                <h3>Candidate Profile</h3>
                <p>Tell us about your current experience.</p>
              </div>
            </div>

            <div className="form-grid">
              <label>
                Name
                <input
                  value={name}
                  onChange={(event) => setName(event.target.value)}
                  placeholder="Your full name"
                />
              </label>

              <label>
                Email
                <input
                  type="email"
                  value={email}
                  onChange={(event) => setEmail(event.target.value)}
                  placeholder="you@example.com"
                />
              </label>

              <label>
                Education
                <input
                  value={education}
                  onChange={(event) => setEducation(event.target.value)}
                  placeholder="B.Tech CSE, AI"
                />
              </label>

              <label>
                Years of Experience
                <input
                  type="number"
                  min="0"
                  step="0.1"
                  value={experience}
                  onChange={(event) => setExperience(event.target.value)}
                />
              </label>

              <label className="full-width">
                Skills
                <input
                  value={skills}
                  onChange={(event) => setSkills(event.target.value)}
                  placeholder="Python, SQL, Data Structures"
                />
                <span>Separate skills with commas.</span>
              </label>

              <label className="full-width">
                Technologies
                <input
                  value={technologies}
                  onChange={(event) => setTechnologies(event.target.value)}
                  placeholder="FastAPI, React, Azure, Git"
                />
                <span>Separate technologies with commas.</span>
              </label>

              <label className="full-width">
                Projects
                <input
                  value={projects}
                  onChange={(event) => setProjects(event.target.value)}
                  placeholder="CareerGraph AI, ML projects"
                />
                <span>Separate projects with commas.</span>
              </label>

              <label className="full-width">
                Professional Summary
                <textarea
                  value={summary}
                  onChange={(event) => setSummary(event.target.value)}
                  placeholder="Briefly describe your experience and career goals."
                  rows={4}
                />
              </label>
            </div>

            {error && <div className="error">{error}</div>}

            <button
              className="primary-button"
              onClick={createCandidate}
              disabled={loading || !name.trim()}
            >
              {loading ? "Creating Profile..." : "Create Candidate Profile"}
            </button>
          </div>

          <div className="card profile-preview">
            <div className="card-header">
              <div>
                <h3>Profile State</h3>
                <p>Your current CareerGraph evidence state.</p>
              </div>
            </div>

            {!candidate ? (
              <div className="empty-state">
                <div className="empty-icon">◈</div>
                <h4>No profile created yet</h4>
                <p>
                  Complete the form and create your profile to start building
                  your career graph.
                </p>
              </div>
            ) : (
              <div className="candidate-result">
                <div className="profile-heading">
                  <div className="avatar">
                    {candidate.name.charAt(0).toUpperCase()}
                  </div>

                  <div>
                    <h4>{candidate.name}</h4>
                    <p>{candidate.email ?? "No email provided"}</p>
                  </div>
                </div>

                <div className="stat-grid">
                  <div>
                    <span>Experience</span>
                    <strong>{candidate.years_of_experience} years</strong>
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

                <div className="profile-section">
                  <span>Skills</span>
                  <div className="tags">
                    {candidate.skills.map((skill) => (
                      <span key={skill}>{skill}</span>
                    ))}
                  </div>
                </div>

                <div className="profile-section">
                  <span>Technologies</span>
                  <div className="tags">
                    {candidate.technologies.map((technology) => (
                      <span key={technology}>{technology}</span>
                    ))}
                  </div>
                </div>

                {candidate.summary && (
                  <div className="summary">
                    <span>Summary</span>
                    <p>{candidate.summary}</p>
                  </div>
                )}
              </div>
            )}
          </div>
        </section>

        {candidate && (
          <section className="card target-card">
            <div className="card-header">
              <div>
                <h3>Target Profile</h3>
                <p>
                  Define the role you are preparing for. This becomes the
                  baseline for future skill-gap analysis.
                </p>
              </div>
            </div>

            {!target ? (
              <>
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
                      placeholder="Optional — e.g. Google"
                    />
                    <span>
                      Leave blank for a general target profile.
                    </span>
                  </label>
                </div>

                {targetError && <div className="error">{targetError}</div>}

                <button
                  className="primary-button"
                  onClick={createTarget}
                  disabled={targetLoading || !role.trim() || !level.trim()}
                >
                  {targetLoading ? "Creating Target..." : "Create Target Profile"}
                </button>
              </>
            ) : (
              <div className="candidate-result">
                <div className="profile-heading">
                  <div className="avatar">🎯</div>

                  <div>
                    <h4>
                      {target.role} — {target.level}
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
                    <strong>{target.active ? "Active" : "Inactive"}</strong>
                  </div>
                </div>

                <div className="success">
                  Target profile created successfully. This target can now be
                  used for competency and skill-gap analysis.
                </div>
              </div>
            )}
          </section>
        )}
      </main>
    </div>
  );
}

export default App;

