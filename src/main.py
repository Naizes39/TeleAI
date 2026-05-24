from fastapi import FastAPI, HTTPException
from src.schemas import TelemetryData
import uvicorn
from contextlib import asynccontextmanager
from src.engine.rag_core import PyTorchRAGDatabase


models = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    models["rag_model"] = PyTorchRAGDatabase()
    models["rag_model"].load_and_chunk_text(filepath="data/nokia_5g_core_manual.txt", chunk_size=100, overlap=25)
    models["rag_model"].get_embeddings()
    yield
    models.clear()


app = FastAPI(title="TeleAI", lifespan=lifespan)



@app.post("/analyze")
async def analyze_telemetry(data: TelemetryData):
    if (
        data.cpu_usage > 95.0 
        or data.latency_ms > 150 
        or data.packet_loss_percent > 5.0 
        or data.radio_link_failures > 10
    ):
        status = "CRITICAL"
    elif (
        data.cpu_usage > 80.0 
        or data.latency_ms > 100 
        or data.jitter_ms > 30
    ):
        status = "WARNING"
    else:
        status = "HEALTHY"
    

    output = {
            "server_id": data.server_id,
            "status": status,
            "metrics_processed": {
                "cpu": data.cpu_usage,
                "latency": data.latency_ms
            },
            "diagnostics": None,
        }
    
    if status != "HEALTHY":
        text = "\n".join(f"{k}: {v}" for k, v in data.model_dump().items()) + status
        diagnose = models['rag_model'].search(text)
        output['diagnostics'] = diagnose

    return output


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8765,
        log_level="debug",
        reload=True,
    )