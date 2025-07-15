import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from controllers.chat_controller import router as chat_router
from controllers.ingest_controller import router as ingest_router


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(chat_router, prefix="/api")
app.include_router(ingest_router, prefix="/api") 


static_dir = "/app/static"
app.mount("/static", StaticFiles(directory=static_dir, html=True), name="static")
