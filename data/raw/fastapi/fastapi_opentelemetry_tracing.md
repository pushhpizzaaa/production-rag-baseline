# Distributed Tracing with OpenTelemetry

**Doc ID:** `fastapi_opentelemetry_tracing`  
**Category:** `FastAPI`  
**Domain:** `Web APIs & Python Asynchronous Services`  
**Summary:** Propagate W3C trace contexts and instrument spans across distributed microservices.

---

## OpenTelemetry Tracing
```python
from fastapi import FastAPI
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider

provider = TracerProvider()
trace.set_tracer_provider(provider)

app = FastAPI()
FastAPIInstrumentor.instrument_app(app)
```
Every incoming HTTP request automatically receives a trace ID and span ID logged in telemetry backends like Jaeger or Datadog.

