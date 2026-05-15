from fastapi import FastAPI
from responsible_ai_service.risk_routes import router as risk_router

app = FastAPI(title="FairEval Responsible AI Risk Evaluation Service", version="0.2.0")
app.include_router(risk_router)
