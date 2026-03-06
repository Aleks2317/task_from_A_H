# Backend service with monitoring capabilities: metrics, logs, visualization

This project demonstrates the creation of a backend service with monitoring support: metrics collection (Prometheus), structured logs, and visualization in Grafana.

## Technologies

* Python 3.10+ — implementation language.

* FastAPI — API framework.

* SQLAlchemy + PostgreSQL — database management.

* Prometheus — application metrics collection.

* Node Exporter — system metrics collection (CPU, memory, etc.).

* Grafana — data visualization, dashboards.

* Loki + Promtail — log collection and storage.

* Docker + Docker Compose — containerization and orchestration.

* **Pytest** — testing.

* **Structured Logging** (JSON Logs) — Structured logging.

## Functionality

The FastAPI application exposes the following endpoints:

* `GET /health` — returns `$\{"status": "healthy"\}$`.

* `GET /message/{id}` — returns a static message from a simulated database (table `messages`: `id`, `text`).

* `POST /process` — accepts JSON `$\{"data": str\}$`, simulates processing (`sleep ~0.5$ sec`), returns echo.

* `GET /metrics` — exports metrics for Prometheus.

**Custom Metrics:**
* request counter by endpoint (`Counter`);

* latency histogram (`Histogram`).

## Observability

* **Metrics:** Prometheus collects application metrics (total requests, latency, errors) and system metrics via Node Exporter (CPU, memory, disk).

* **Logs:** Structured JSON logs collected via Promtail are stored in Loki.

* **Visualization:** Grafana dashboard (JSON export) with panels:
* Requests/sec graphs;

* Latency percentage;
* CPU/memory usage;

* Application logs;

* Error/warning counter.

* **Alerts:** Prometheus rule for high latency (>1 sec).

## Running locally via Docker Compose

### Prerequisites

* Docker;

* Docker Compose;

* Git (for cloning the repository).

### Steps to get started

1. Clone the repository:

```bash

git clone https://github.com/Aleks2317/task_from_A_H.git

cd task_from_A_H