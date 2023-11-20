from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
import database.deps as deps
from models import Library, User
from endpoints.auth import get_current_user, get_forbidden_exception
from utils.movie_utils import load_library

router = APIRouter()


@router.post("/library/{imdb_movie_id}")
def create_library_item(
        imdb_movie_id: str, db: Session = Depends(deps.get_db), current_user: User = Depends(get_current_user)):
    try:
        library = Library(user_id=current_user.id, imdb_movie_id=imdb_movie_id)
        db.add(library)
        db.commit()
        db.refresh(library)
        return library
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Duplicate library item")


@router.get("/library/{library_id}")
def read_library_item(
        library_id: int, db: Session = Depends(deps.get_db), current_user: User = Depends(get_current_user)):
    library_item = db.query(Library).filter(Library.id == library_id).first()
    if library_item is None:
        raise HTTPException(status_code=404, detail="Library item not found")
    check_if_user_has_rights(user=current_user, library=library_item)
    return library_item


@router.patch("/library/{library_id}/{imdb_movie_id}")
def update_library_item(
        library_id: int, imdb_movie_id: str,
        db: Session = Depends(deps.get_db),
        current_user: User = Depends(get_current_user)):
    library_item = db.query(Library).filter(Library.id == library_id).first()
    if library_item is None:
        raise HTTPException(status_code=404, detail="Library item not found")
    check_if_user_has_rights(user=current_user, library=library_item)
    if imdb_movie_id is not None:
        library_item.imdb_movie_id = imdb_movie_id

    db.commit()
    db.refresh(library_item)
    return library_item


@router.delete("/library/{library_id}")
def delete_library_item(
        library_id: int,
        db: Session = Depends(deps.get_db),
        current_user: User = Depends(get_current_user)):
    library_item = db.query(Library).filter(Library.id == library_id).first()
    if library_item is None:
        raise HTTPException(status_code=404, detail="Library item not found")
    check_if_user_has_rights(user=current_user, library=library_item)
    db.delete(library_item)
    db.commit()
    return library_item


@router.get("/my-library")
def get_all_libraries(
        db: Session = Depends(deps.get_db),
        current_user: User = Depends(get_current_user)):
    libraries = db.query(Library).filter(Library.user_id == current_user.id).all()
    user_library_list = load_library(movie_list=libraries)
    return user_library_list


def is_owner_of_library(user: User, library: Library):
    return library.user_id == user.id


def check_if_user_has_rights(user: User, library: Library):
    if not is_owner_of_library(user, library):
        raise get_forbidden_exception()
