# Project Atlas: TeleAI - Autonomous 5G Edge Network Agent

## Executive Summary
TeleAI is an asynchronous, AI-driven network management microservice designed to autonomously diagnose 5G edge node telemetry. Instead of relying on static rule-based alerts, it combines a high-performance FastAPI nervous system with an embedded PyTorch Vector Engine (RAG) to instantly map critical network degradation to operational resolution protocols.

## System Architecture

The architecture is divided into two operational layers:

### 1. The Nervous System (FastAPI)
An asynchronous telemetry ingestion engine that monitors network slices in real-time. 
* Evaluates dynamic thresholds for CPU exhaustion, latency spikes, buffer bloat, and Radio Link Failures (RLF).
* Implements the `lifespan` context manager pattern to safely load and persist heavy machine learning models in memory without race conditions or memory leaks during horizontal scaling.

### 2. The Brain (PyTorch Vector Database)
A custom-built Retrieval-Augmented Generation (RAG) core engineered from scratch, bypassing heavy abstractions like LangChain for raw performance.
* **Overlapping Sliding Windows:** Ingests unstructured operational manuals using an overlapping token window to preserve semantic context.
* **Tensor Broadcasting:** Utilises `SentenceTransformer` to encode network manuals into high-dimensional PyTorch tensors.
* **Matrix Similarity:** Dynamically embeds incoming telemetry alarms and executes `F.cosine_similarity` matrix multiplication against the knowledge graph to extract the exact mitigation protocol in milliseconds.

## Engineering Standards & Optimisations
* **Memory Management:** Zero-copy tensor dimensionality manipulation (`unsqueeze(0)`) for optimal GPU/CPU broadcasting.
* **Automated CI/CD Testing:** Full `pytest` integration with mocked FastAPI `TestClient` context managers to verify stateless threshold logic.
* **Enterprise Containerisation:** Built on a `python:3.11-slim` base image, utilising Astral's Rust-based `uv` package manager for sub-second dependency resolution and frozen lockfiles. Configured with a non-root `app` user for strict enterprise security compliance.

## Quickstart & Deployment

### 1. Build the Container
Utilising Docker and `uv` for deterministic, cached builds:
```bash
docker build -t teleai-agent .

### 2. Run the Microservice
```
docker run -p 8765:8765 teleai-agent
```

### 3. API Usage Example (cURL)
```
curl -X 'POST' \
  'http://localhost:8765/analyze' \
  -H 'Content-Type: application/json' \
  -d '{
  "server_id": "edge-node-04",
  "cpu_usage": 85.0,
  "memory_usage": 70.0,
  "latency_ms": 160,
  "packet_loss_percent": 6.0,
  "jitter_ms": 45,
  "active_network_slices": 3,
  "radio_link_failures": 12
}'
```
Expected JSON Response:
```
{
  "server_id": "edge-node-04",
  "status": "CRITICAL",
  "metrics_processed": {
    "cpu": 85.0,
    "latency": 160
  },
  "diagnostics": "Latency exceeding 150ms or jitter exceeding 30ms directly degrades... Engineers must flush the transport buffer and reset the QoS scheduler. Execute: `sysctl -w net.ipv4.tcp_congestion_control=bbr`"
}
```