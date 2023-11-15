from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from typing import Annotated
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
import auth

app = FastAPI()
app.include_router(auth.router)
models.Base.metadata.create_all(bind=engine)

