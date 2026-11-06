# DevOps Command Room AI: Hackathon Live Demo Runbook

Step-by-step presentation runbook and live demonstration guide for the **Flip the Switch Hackathon**.

---

## 1. Three-Minute Presentation Pitch

| Timestamp | Phase | Visual Anchor | Key Message |
| --- | --- | --- | --- |
| 0:00-0:45 | Problem & Setup | Mattermost and architecture diagram | Introduce the problem of isolated AI agents and present DevOps Command Room AI. |
| 0:45-1:30 | Incident | Terminal and test output | Demonstrate the simulated HTTP 500 health-check incident. |
| 1:30-2:15 | Agent Triage & Patch | Switch Console and Mattermost | Show `fullstack-dev` diagnosing and fixing the issue under configured guardrails. |
| 2:15-2:45 | Human Verification | Antigravity terminal | Explain the execution boundary and demonstrate independent human verification. |
| 2:45-3:00 | Resolution | Mattermost and Git | Show the human-reviewed commit and summarize the collaboration workflow. |

---

## 2. Pre-Flight Checklist

Before recording or presenting live to judges, verify the following:

1. Working tree is clean (`git status` shows no uncommitted changes).
2. Original branch name is recorded before switching (run `git branch --show-current`).
3. Baseline commit `2797ccf` is available in the local repository (`git cat-file -e "2797ccf^{commit}"`).
4. Mattermost container is running and the `#DevOps Command Room` channel is accessible.
5. `switch-buddy-admin` and `fullstack-dev` are available.
6. Switch Console is running.
7. Workspace path restriction is configured to the project root.
8. Bypass mode is disabled and approval checks are enabled.
9. Antigravity IDE has the project workspace open.
10. `.venv` exists and dependencies are installed.
11. Port 8000 is available for the local service demonstration.

---

## 3. Live Demo Workflow

### Step 1: Prepare an Isolated Demo Branch

The healthy fallback fix is already committed in the main project history:

- Initial scaffold commit: `2797ccf`
- Existing fix commit: `8ff99a6`

Simply reverting the fallback in the current branch and allowing the agent to restore it would not produce a meaningful new Git diff. Therefore, the human operator should demonstrate the incident on a separate branch based on the original scaffold commit.

Execute the following commands manually in PowerShell:

```powershell
# First ensure the current working tree is clean
git status

# Record the current branch name so you can return to it later
git branch --show-current

# Create an isolated demo branch from the original scaffold commit
git switch -c demo/incident-resolution 2797ccf
```

> [!NOTE]
> If `demo/incident-resolution` already exists, choose a different unused name (e.g., `demo/incident-resolution-2`). This branch reproduces the original incident without changing the existing main development branch.

### Step 2: Stage the Simulated Incident

On the `demo/incident-resolution` branch, the original `app/main.py` contains the degraded fallback:

```python
service_status = os.getenv("SERVICE_STATUS", "degraded")
```

Run the automated API tests in PowerShell:

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

Expected result:

```text
1 failed, 3 passed
```

The default health check fails because the fallback status is `degraded`, triggering the simulated HTTP 500 response.

### Step 3: Declare the Incident in Mattermost

In `#DevOps Command Room`, the human operator reports:

- Target endpoint: `GET /health`
- Observed behavior: HTTP 500
- Simulated cause: degraded default health status

Then dispatch `@fullstack-dev` with this request:

> "Please inspect app/main.py and tests/test_health.py, identify the root cause of the default health-check failure, and apply the appropriate source-level fix."

### Step 4: Agent Triage Through Switch Console

In Switch Console, observe the developer agent performing triage:

1. `fullstack-dev` inspects `app/main.py` and `tests/test_health.py`.
2. The agent diagnoses the incorrect default fallback causing the failure.
3. The agent changes the fallback from `"degraded"` to `"healthy"` in `app/main.py`.
4. The agent's pytest execution attempt was unsuccessful due to a host Python interpreter path access boundary.

### Step 5: Independent Human Verification

Switch to Antigravity IDE and run the automated API tests:

> [!NOTE]
> If the FastAPI application is already running, restart it after the agent's source-code modification so the updated code is loaded:
> ```powershell
> .\.venv\Scripts\python.exe -m uvicorn app.main:app --reload
> ```

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

Expected result:

```text
4 passed, 1 warning
```

Then demonstrate the local health endpoint, provided the application is running:

```powershell
Invoke-RestMethod -Uri http://localhost:8000/health
```

Expected response:

```json
{
  "status": "healthy",
  "uptime_s": 3600
}
```

The human operator independently verifies that the agent's change resolves the simulated degradation and restores healthy status.

### Step 6: Human Sign-Off and Git Commit

The human operator reviews the change and performs version control manually:

```powershell
git diff app/main.py
git add app/main.py
git commit -m "demo: resolve simulated health-check incident"
```

A unique commit message is used because the original fix commit already exists on the main development branch.

Then post the final incident resolution message in Mattermost:

> "Incident resolved. The developer agent's patch has been independently verified. All four automated API tests are passing, and the simulated health check has returned to healthy. The human operator has reviewed and committed the fix."

### Step 7: Return to the Original Development Branch

After the demonstration, return to the original branch recorded before creating `demo/incident-resolution`:

```powershell
git switch <ORIGINAL_BRANCH_NAME>
```

Do not merge the `demo/incident-resolution` branch into the main development branch as part of the recording unless explicitly choosing to do so. This ensures the existing project history remains undisturbed.

---

## 4. Judge Q&A Cheat Sheet

**Q: Why didn't the agent commit the code directly?**

A: The human operator retained responsibility for reviewing the agent's changes, independently verifying the tests, and performing Git version control. This demonstrates human accountability in the incident-resolution workflow.

**Q: What guardrails were configured?**

A: The Switch workspace path restriction was configured to the project root, bypass mode was disabled, and approval checks were enforced.

**Q: Why did the agent fail to run pytest?**

A: Its pytest execution attempt was unsuccessful due to a host Python interpreter path access boundary. The human operator independently ran the test suite using the local virtual environment.

**Q: Does the application automatically detect production incidents?**

A: No. This project demonstrates a simulated production incident initiated by a human operator and handled through human-agent collaboration.

**Q: What is the main contribution of Switch in this project?**

A: Switch provides the orchestration environment connecting the Mattermost collaboration workflow with the specialized developer agent, while configured guardrails and human oversight remain part of the process.
