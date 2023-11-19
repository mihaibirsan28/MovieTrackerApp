from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
import database.deps as deps
from models import Library

router = APIRouter()


@router.post("/library/{user_id}/{imdb_movie_id}")
def create_library_item(user_id: int, imdb_movie_id: str, db: Session = Depends(deps.get_db)):
    try:
        library = Library(user_id=user_id, imdb_movie_id=imdb_movie_id)
        db.add(library)
        db.commit()
        db.refresh(library)
        return library
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Duplicate library item")


@router.get("/library/{library_id}")
def read_library_item(library_id: int, db: Session = Depends(deps.get_db)):
    library_item = db.query(Library).filter(Library.id == library_id).first()
    if library_item is None:
        raise HTTPException(status_code=404, detail="Library item not found")
    return library_item


@router.patch("/library/{library_id}/{user_id}/{imdb_movie_id}")
def update_library_item(library_id: int, user_id: int, imdb_movie_id: str, db: Session = Depends(deps.get_db)):
    library_item = db.query(Library).filter(Library.id == library_id).first()
    if library_item is None:
        raise HTTPException(status_code=404, detail="Library item not found")

    if user_id is not None:
        library_item.user_id = user_id
    if imdb_movie_id is not None:
        library_item.imdb_movie_id = imdb_movie_id

    db.commit()
    db.refresh(library_item)
    return library_item


@router.delete("/library/{library_id}")
def delete_library_item(library_id: int, db: Session = Depends(deps.get_db)):
    library_item = db.query(Library).filter(Library.id == library_id).first()
    if library_item is None:
        raise HTTPException(status_code=404, detail="Library item not found")

    db.delete(library_item)
    db.commit()
    return library_item


@router.get("/library/all/{user_id}")
def get_all_libraries(user_id: int, db: Session = Depends(deps.get_db)):
    libraries = db.query(Library).filter(Library.user_id == user_id).all()
    return libraries