# DevOps Command Room AI

Target microservice and demonstration harness for **Flip the Switch Hackathon**.

The target service simulates a real-world production incident within an automated DevOps incident response loop featuring **Human SRE + Switch Console + Mattermost + Codex Agent**.

---

## 🏛 Multi-Agent Architecture

```text
+---------------+        Alert / Health Probe        +--------------------+
|  FastAPI App  |  --------------------------------> |   Switch Console   |
| (Target Svc)  | <--------------------------------- | (Workflow Orchestr)|
+---------------+      Automated Resolution / Fix    +---------+----------+
                                                               |
                                                               v
                                                    +--------------------+
                                                    |  Mattermost Channel|
                                                    | (Ops Incident Room)|
                                                    +---------+----------+
                                                               |
                                                               v
                                                    +--------------------+
                                                    |  @fullstack-dev    |
                                                    |   (Codex Agent)    |
                                                    +--------------------+
```

1. **Target Service (FastAPI):** Exposes health and operational endpoints; defaults to an intentional degraded state (`HTTP 500`) to simulate an active production failure.
2. **Switch Console:** Orchestrates incident monitoring, triggers playbooks, and coordinates human/agent collaboration.
3. **Mattermost:** Serves as the central DevOps war room where alerts are broadcasted and triage threads take place.
4. **Codex Agent (`@fullstack-dev`):** Dispatched via Switch Console to inspect root causes, propose fixes, and resolve the outage.

---

## 🚀 Local Development

### Prerequisites
- Python 3.11+
- Git

### Setup & Run
1. Create and activate a virtual environment:
   ```bash
   # Windows PowerShell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1

   # Linux / macOS
   python3 -m venv .venv
   source .venv/bin/activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the microservice locally:
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

4. Endpoints:
   - Root Status: `GET http://localhost:8000/`
   - Health Probe: `GET http://localhost:8000/health`
   - OpenAPI Docs: `GET http://localhost:8000/docs`

---

## 🐳 Docker Deployment

### Run with Docker Compose
```bash
docker compose up --build
```

### Run with Docker Standalone
```bash
docker build -t devops-command-room-ai .
docker run -p 8000:8000 -e SERVICE_STATUS=degraded devops-command-room-ai
```

---

## 🚨 Intentional Production Incident Demo

By default, `app/main.py` evaluates the `SERVICE_STATUS` environment variable:
- When unset or set to `"degraded"`: `GET /health` returns **HTTP 500** (`"Service degraded: memory leak detected"`).
- When set to `"healthy"`: `GET /health` returns **HTTP 200** (`{"status": "healthy", "uptime_s": 3600}`).

### Test Suite Behavior
Run tests with:
```bash
pytest -q
```

- **Passing (3):**
  - `test_root`: Validates root online status.
  - `test_health_explicit_healthy`: Validates healthy response when `SERVICE_STATUS=healthy`.
  - `test_health_explicit_degraded`: Validates degraded 500 response when `SERVICE_STATUS=degraded`.
- **Failing (1 - Intentional):**
  - `test_default_health_check_production_incident`: Fails because production default is degraded (`500 != 200`).

This failing test represents the active production incident that will be triaged and resolved by `@fullstack-dev` through Switch Console during the live hackathon demo.

