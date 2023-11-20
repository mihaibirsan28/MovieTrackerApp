from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import models
import logging
from database.database import engine
from endpoints.api import api_router

app = FastAPI(debug=True)
logging.basicConfig(level=logging.INFO)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)
models.Base.metadata.create_all(bind=engine)
