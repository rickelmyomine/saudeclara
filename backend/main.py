import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

from routers import triagem  # noqa: E402

app = FastAPI(title="SaúdeClara API")

origins = [o.strip() for o in os.getenv("ALLOWED_ORIGINS", "http://localhost:8501").split(",")]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # lista explícita, sem "*"
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)
app.include_router(triagem.router)
