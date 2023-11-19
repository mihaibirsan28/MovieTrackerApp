from typing import Generator
from database.database import SessionLocal
from fastapi.security import OAuth2PasswordBearer


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/login')
