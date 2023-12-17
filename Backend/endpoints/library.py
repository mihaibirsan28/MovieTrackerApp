# library_routes.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import database.deps as deps
from models import User
from endpoints.auth import get_current_user, get_forbidden_exception
from services.library_service import LibraryService
from utils.movie_utils import load_library

router = APIRouter()

@router.post("/library/{imdb_movie_id}")
def create_library_item(imdb_movie_id: str, db: Session = Depends(deps.get_db), current_user: User = Depends(get_current_user)):
    service = LibraryService(db)
    return service.create_library_item(current_user.id, imdb_movie_id)

@router.get("/library/{library_id}")
def read_library_item(library_id: int, db: Session = Depends(deps.get_db), current_user: User = Depends(get_current_user)):
    service = LibraryService(db)
    library_item = service.get_library_item(library_id, current_user.id)
    if not service.is_owner_of_library(current_user, library_item):
        raise get_forbidden_exception()
    return library_item

@router.patch("/library/{library_id}/{imdb_movie_id}")
def update_library_item(library_id: int, imdb_movie_id: str, db: Session = Depends(deps.get_db), current_user: User = Depends(get_current_user)):
    service = LibraryService(db)
    return service.update_library_item(library_id, current_user.id, imdb_movie_id)

@router.delete("/library/{library_id}")
def delete_library_item(library_id: int, db: Session = Depends(deps.get_db), current_user: User = Depends(get_current_user)):
    service = LibraryService(db)
    return service.delete_library_item(library_id, current_user.id)

@router.get("/my-library")
def get_all_libraries(db: Session = Depends(deps.get_db), current_user: User = Depends(get_current_user)):
    service = LibraryService(db)
    libraries = service.get_all_libraries(current_user.id)
    return load_library(movie_list=libraries)
