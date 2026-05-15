from fastapi import FastAPI
from responsible_ai_service.routes import router

app = FastAPI(title="FairEval Responsible AI Service", version="0.1.0")
app.include_router(router)
