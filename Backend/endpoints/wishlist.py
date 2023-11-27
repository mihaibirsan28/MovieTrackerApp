# wishlist_routes.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import database.deps as deps
from models import User
from endpoints.auth import get_current_user
from services.wishlist_service import WishlistService

router = APIRouter()


@router.post("/wishlist/{imdb_movie_id}")
def create_wishlist_item(imdb_movie_id: str, db: Session = Depends(deps.get_db), current_user: User = Depends(get_current_user)):
    service = WishlistService(db)
    return service.create_wishlist_item(current_user.id, imdb_movie_id)


@router.get("/wishlist/{wishlist_id}")
def read_wishlist_item(wishlist_id: int, db: Session = Depends(deps.get_db), current_user: User = Depends(get_current_user)):
    service = WishlistService(db)
    return service.get_wishlist_item(wishlist_id, current_user.id)


@router.patch("/wishlist/{wishlist_id}/{imdb_movie_id}")
def update_wishlist_item(wishlist_id: int, imdb_movie_id: str, db: Session = Depends(deps.get_db), current_user: User = Depends(get_current_user)):
    service = WishlistService(db)
    return service.update_wishlist_item(wishlist_id, current_user.id, imdb_movie_id)


@router.delete("/wishlist/{wishlist_id}")
def delete_wishlist_item(wishlist_id: int, db: Session = Depends(deps.get_db), current_user: User = Depends(get_current_user)):
    service = WishlistService(db)
    return service.delete_wishlist_item(wishlist_id, current_user.id)


@router.get("/my-wishlist")
def get_all_wishlists(db: Session = Depends(deps.get_db), current_user: User = Depends(get_current_user)):
    service = WishlistService(db)
    return service.get_all_wishlists(current_user.id)
