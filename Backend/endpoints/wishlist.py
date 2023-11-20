from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
import database.deps as deps
from models import Wishlist, User
from endpoints.auth import get_current_user, get_forbidden_exception

router = APIRouter()


@router.post("/wishlist/{imdb_movie_id}")
def create_wishlist_item(
        imdb_movie_id: str,
        db: Session = Depends(deps.get_db),
        current_user: User = Depends(get_current_user)):
    try:
        wishlist = Wishlist(user_id=current_user.id, imdb_movie_id=imdb_movie_id)
        db.add(wishlist)
        db.commit()
        db.refresh(wishlist)
        return wishlist
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Duplicate wishlist item")


@router.get("/wishlist/{wishlist_id}")
def read_wishlist_item(
        wishlist_id: int,
        db: Session = Depends(deps.get_db),
        current_user: User = Depends(get_current_user)):
    wishlist_item = db.query(Wishlist).filter(Wishlist.id == wishlist_id).first()
    if wishlist_item is None:
        raise HTTPException(status_code=404, detail="Wishlist item not found")
    check_if_user_has_rights(user=current_user, wishlist=wishlist_item)
    return wishlist_item


@router.patch("/wishlist/{wishlist_id}/{imdb_movie_id}")
def update_wishlist_item(
        wishlist_id: int,
        imdb_movie_id: str,
        db: Session = Depends(deps.get_db),
        current_user: User = Depends(get_current_user)):
    wishlist_item = db.query(Wishlist).filter(Wishlist.id == wishlist_id).first()
    if wishlist_item is None:
        raise HTTPException(status_code=404, detail="Wishlist item not found")
    check_if_user_has_rights(user=current_user, wishlist=wishlist_item)
    if imdb_movie_id is not None:
        wishlist_item.imdb_movie_id = imdb_movie_id

    db.commit()
    db.refresh(wishlist_item)
    return wishlist_item


@router.delete("/wishlist/{wishlist_id}")
def delete_wishlist_item(
        wishlist_id: int,
        db: Session = Depends(deps.get_db),
        current_user: User = Depends(get_current_user)):
    wishlist_item = db.query(Wishlist).filter(Wishlist.id == wishlist_id).first()
    if wishlist_item is None:
        raise HTTPException(status_code=404, detail="Wishlist item not found")
    check_if_user_has_rights(user=current_user, wishlist=wishlist_item)
    db.delete(wishlist_item)
    db.commit()
    return wishlist_item


@router.get("/wishlist/all")
def get_all_wishlists(
        db: Session = Depends(deps.get_db),
        current_user: User = Depends(get_current_user)):
    wishlists = db.query(Wishlist).filter(Wishlist.user_id == current_user.id).all()
    return wishlists


def is_owner_of_wishlist(user: User, wishlist: Wishlist):
    return wishlist.user_id == user.id


def check_if_user_has_rights(user: User, wishlist: Wishlist):
    if not is_owner_of_wishlist(user, wishlist):
        raise get_forbidden_exception()
