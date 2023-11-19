from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
import database.deps as deps
from models import Wishlist

router = APIRouter()


@router.post("/wishlist/{user_id}/{imdb_movie_id}")
def create_wishlist_item(user_id: int, imdb_movie_id: str, db: Session = Depends(deps.get_db)):
    try:
        wishlist = Wishlist(user_id=user_id, imdb_movie_id=imdb_movie_id)
        db.add(wishlist)
        db.commit()
        db.refresh(wishlist)
        return wishlist
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Duplicate wishlist item")


@router.get("/wishlist/{wishlist_id}")
def read_wishlist_item(wishlist_id: int, db: Session = Depends(deps.get_db)):
    wishlist_item = db.query(Wishlist).filter(Wishlist.id == wishlist_id).first()
    if wishlist_item is None:
        raise HTTPException(status_code=404, detail="Wishlist item not found")
    return wishlist_item


@router.patch("/wishlist/{wishlist_id}/{user_id}")
def update_wishlist_item(wishlist_id: int, user_id: int, imdb_movie_id: str, db: Session = Depends(deps.get_db)):
    wishlist_item = db.query(Wishlist).filter(Wishlist.id == wishlist_id).first()
    if wishlist_item is None:
        raise HTTPException(status_code=404, detail="Wishlist item not found")

    if user_id is not None:
        wishlist_item.user_id = user_id
    if imdb_movie_id is not None:
        wishlist_item.imdb_movie_id = imdb_movie_id

    db.commit()
    db.refresh(wishlist_item)
    return wishlist_item


@router.delete("/wishlist/{wishlist_id}")
def delete_wishlist_item(wishlist_id: int, db: Session = Depends(deps.get_db)):
    wishlist_item = db.query(Wishlist).filter(Wishlist.id == wishlist_id).first()
    if wishlist_item is None:
        raise HTTPException(status_code=404, detail="Wishlist item not found")

    db.delete(wishlist_item)
    db.commit()
    return wishlist_item


@router.get("/wishlist/all/{user_id}")
def get_all_wishlists(user_id: int, db: Session = Depends(deps.get_db)):
    wishlists = db.query(Wishlist).filter(Wishlist.user_id == user_id).all()
    return wishlists
