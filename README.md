# DevOps Command Room AI

<p align="center">
  <a href="https://youtu.be/tjjwNbnUvLg">
    <img src="https://img.youtube.com/vi/tjjwNbnUvLg/maxresdefault.jpg"
         alt="DevOps Command Room AI Demo"
         width="850">
  </a>
  <br>
  <strong>▶ Watch the Project Demo</strong>
</p>

**Flip the Switch Hackathon Submission**

- **Hackathon:** Flip the Switch Hackathon
- **Organizers:** WeMakeDevs × DevTools Academy × Switch
- **Selected Track:** Track 01: Best Business Workflow ($2,000 Cash Prize)
- **Project:** DevOps Command Room AI

---

## Business Problem & Solution Overview

In production engineering, autonomous AI agents running without human oversight introduce operational risk. Unsupervised code edits in production environments can worsen incidents, breach organizational boundaries, and complicate version control. Conversely, purely manual triage by engineers during off-hours can cause delays in diagnosing regressions.

**DevOps Command Room AI** addresses this challenge by integrating specialized AI agents into a coordinated human-agent incident response workflow:

1. **Shared War Room Collaboration:** Incident triage is conducted collaboratively in a Mattermost channel (`#DevOps Command Room`) where human SREs and specialized AI agents interact.
2. **Specialized Multi-Agent Coordination:** Switch Console coordinates agent interactions through the Switch-Mattermost Bridge, dispatching `fullstack-dev` (Codex ACP) under the coordination of `switch-buddy-admin`.
3. **Configured Workspace Boundaries:** The developer agent inspects codebase context and applies targeted source-level remediation within configured workspace limits.
4. **Human-in-the-Loop Governance:** The human operator independently reviews code changes, runs automated API test validation in the local environment, and retains exclusive authority over Git version control.

> [!NOTE]
> This project demonstrates a **human-supervised incident-response workflow**. The target microservice does not automatically detect production incidents or alert external services; simulated incident triage is initiated and supervised by the human operator.

---

## Multi-Agent System Architecture

The following ASCII architecture diagram illustrates the communication and governance hierarchy:

```text
+-----------------------------------------------------------------------------------------+
|                                  HUMAN OPERATOR / SRE                                   |
| (Antigravity IDE / Terminal / Local Python .venv / Manual Git CLI: add, commit, push)   |
+------------------------------------+------------------------------------+---------------+
                                     |                                    ^
                 Incident Escalation | Chat / Dispatch                    | Verification
                 & Operational Review|                                    | & Manual Commit
                                     v                                    |
+-------------------------------------------------------------------------+---------------+
|                                    MATTERMOST (DOCKER)                                  |
|                               Channel: #DevOps Command Room                             |
|                                                                                         |
|   +-----------------------------+               +-----------------------------------+   |
|   |     switch-buddy-admin      |               |          @fullstack-dev           |   |
|   | (Room Admin & Agent Manager)|               |   (Codex ACP Scoped Dev Agent)    |   |
+---+--------------+--------------+---------------+-----------------+-----------------+---+
                   |                                                |
                   +-----------------------+------------------------+
                                           |
                                           | Switch-Mattermost Bridge
                                           v
+-----------------------------------------------------------------------------------------+
|                               SWITCH CONSOLE DESKTOP APP                                |
|                        (Local Switch Orchestration Server)                              |
|   * Workspace Path Restriction: devops-command-room-ai                                  |
|   * Bypass Mode: Disabled                                                               |
|   * Approval Checks: Enforced                                                           |
+-------------------------------------------------+---------------------------------------+
                                                  |
                                                  | Scoped Source-Level Modifications
                                                  v
+-----------------------------------------------------------------------------------------+
|                               SCOPED LOCAL WORKSPACE FILES                              |
|  devops-command-room-ai                                                                 |
|                                                                                         |
|   |-- app/                                      |-- tests/                              |
|   |   |-- __init__.py                           |   |-- __init__.py                     |
|   |   `-- main.py (Target Microservice)         |   `-- test_health.py (4 API Tests)    |
|   |-- requirements.txt                          |-- Dockerfile                          |
|   `-- docker-compose.yml (service: devops-api)                                          |
+-----------------------------------------------------------------------------------------+
```

---

## Component Responsibilities Matrix

| Component | Technology | Responsibility |
| --- | --- | --- |
| **Target Service** | FastAPI / Uvicorn | Provides `GET /` and `GET /health`; health status is controlled by `SERVICE_STATUS`. |
| **API Test Suite** | Pytest / Starlette TestClient | Runs four API tests covering root status and health-check behavior. |
| **Orchestration** | Switch Console | Coordinates agents and applies configured workspace and approval settings. |
| **Collaboration Room** | Mattermost (Docker) | Provides the shared incident-response channel. |
| **Room Administrator** | `switch-buddy-admin` | Manages the Mattermost room and agents. |
| **Developer Agent** | `fullstack-dev` (Codex ACP) | Inspects source files and makes targeted code changes. |
| **Human Operator** | Antigravity IDE / Terminal | Initiates triage, reviews changes, runs tests, and controls Git commits. |

---

## Understanding the Three Runtime & Incident States

To evaluate the project accurately, understand the three distinct runtime states:

### A. Resolved Main Branch
- The current resolved `main` branch defaults to `SERVICE_STATUS=healthy` in `app/main.py`.
- Running the test suite passes all contract checks.
- The local default `/health` endpoint returns HTTP 200 (`{"status":"healthy","uptime_s":3600}`).

In PowerShell:
```powershell
.\.venv\Scripts\python.exe -m pytest -q
```
Expected output:
```text
4 passed, 1 warning
```

### B. Demo Incident Branch
- Baseline scaffold commit: `2797ccf`.
- Demo branch name: `demo/incident-resolution`.
- The demo branch is to be created from baseline commit `2797ccf` by the human operator for demonstration purposes; it does not exist automatically.
- In this baseline state, `app/main.py` defaults to `SERVICE_STATUS=degraded`.
- Running the automated API test suite on this baseline produces an intentional failure on the default health check (expects HTTP 200, receives HTTP 500).
- This reproduces the simulated production incident for live hackathon demonstration without altering the main branch history.

In PowerShell:
```powershell
.\.venv\Scripts\python.exe -m pytest -q
```
Expected output:
```text
1 failed, 3 passed
```

### C. Docker Compose Simulated Degradation
- `docker-compose.yml` explicitly sets the container environment variable `SERVICE_STATUS=degraded`.
- This setting deliberately overrides the application's default inside the container.
- When running under Docker Compose, `GET /health` returning HTTP 500 with `{"detail":"Service degraded: memory leak detected"}` is the **expected simulated container behavior**, proving environment-variable injection functions as intended.

In bash/terminal:
```bash
docker compose up --build -d
curl -i http://localhost:8000/health
```
Expected response:
```json
HTTP/1.1 500 Internal Server Error
{"detail":"Service degraded: memory leak detected"}
```

---

## Local Quickstart

### Prerequisites
- Python 3.11+
- Git
- Docker Desktop (optional, for containerized execution)

### 1. Environment Setup

**Windows PowerShell:**
```powershell
# Create virtual environment
python -m venv .venv

# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

**Linux / macOS:**
```bash
# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Run Automated API Tests
```powershell
.\.venv\Scripts\python.exe -m pytest -q
```
Expected resolved result: `4 passed, 1 warning`.

### 3. Start Local Microservice
```powershell
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Endpoints:
- **Root Status:** `GET http://localhost:8000/` returns `{"status":"online","system":"DevOps Command Room"}`
- **Health Check:** `GET http://localhost:8000/health` returns `{"status":"healthy","uptime_s":3600}`
- **OpenAPI Documentation:** `GET http://localhost:8000/docs`

---

## Docker Deployment

### Run with Docker Compose (Simulated Degradation Mode)
```bash
# Build and start container with SERVICE_STATUS=degraded
docker compose up --build -d

# Verify simulated degraded status (HTTP 500)
curl -i http://localhost:8000/health

# Stop and clean up
docker compose down
```

### Run Standalone Docker Container

**Simulated Degraded Mode:**
```bash
docker build -t devops-command-room-ai .
docker run -d --name devops-api -p 8000:8000 -e SERVICE_STATUS=degraded devops-command-room-ai
curl -i http://localhost:8000/health
docker rm -f devops-api
```

**Healthy Mode:**
```bash
docker run -d --name devops-api -p 8000:8000 -e SERVICE_STATUS=healthy devops-command-room-ai
curl -i http://localhost:8000/health
docker rm -f devops-api
```

---

## Security, Governance & Guardrails

The operational model relies on verified guardrails and clear boundaries:

- **Configured Workspace Boundaries:** The developer agent is configured with a workspace path restriction to the project root directory (`devops-command-room-ai`).
- **Bypass Mode Disabled:** Safety guardrail bypass mode is explicitly turned off in Switch Console.
- **Approval Checks Enforced:** Tool execution approval checks remain active to supervise file modifications.
- **Transparent Execution Boundary:** The agent inspected project source files and applied targeted code changes to `app/main.py`. When the agent attempted to execute pytest from within its sandbox, its test execution attempt was unsuccessful due to a host Python interpreter path access boundary involving the host `.venv`.
- **Independent Human Verification:** The human operator independently verified the code modifications by running the automated API tests in the host virtual environment.
- **Human-Governed Version Control:** The human operator retains exclusive control over staging (`git add`) and committing (`git commit`) changes to Git history.

---

## Track 01 Alignment: Best Business Workflow

DevOps Command Room AI is submitted for **Track 01: Best Business Workflow** ($2,000 Cash Prize). It targets the operational reality of software organizations by demonstrating how multi-agent automation integrates into business workflows:

1. **Centralized Team Communication:** Consolidates incident notifications, human discussion, and agent triage into a standard Mattermost team channel.
2. **Human-Agent Teaming:** Integrates a room manager (`switch-buddy-admin`) and a code remediator (`fullstack-dev`) alongside the human SRE.
3. **AI-Assisted Root Cause Diagnosis:** Automates the repetitive task of reading source files, tracing failing assertions, and proposing code remedies.
4. **Independent Human Verification:** Enforces organizational compliance by having the human SRE validate tests locally before changes enter the version-controlled codebase.
5. **Human-Governed Accountability:** Ensures all Git commits and deployment decisions remain accountable to human operators within a configured agent workspace.

---

## Related Documentation

- **[ARCHITECTURE.md](ARCHITECTURE.md):** Detailed technical architecture, ASCII and Mermaid system diagrams, component matrix, guardrail specifications, and incident resolution lifecycle.
- **[DEMO_RUNBOOK.md](DEMO_RUNBOOK.md):** Three-minute presentation pitch, pre-flight checklist, step-by-step live demo walkthrough using an isolated demo branch, and judge Q&A cheat sheet.
