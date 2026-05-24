from pydantic import BaseModel, Field

class TelemetryData(BaseModel):
    server_id: str = Field(..., description="Unique identifier of the 5G edge node")
    cpu_usage: float = Field(..., ge=0.0, le=100.0)
    memory_usage: float = Field(..., ge=0.0, le=100.0)
    latency_ms: int = Field(..., ge=0)
    packet_loss_percent: float = Field(..., ge=0.0, le=100.0)
    jitter_ms: int = Field(..., ge=0)
    active_network_slices: int = Field(..., ge=1)
    radio_link_failures: int = Field(..., ge=0)