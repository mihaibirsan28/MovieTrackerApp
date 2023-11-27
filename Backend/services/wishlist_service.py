# wishlist_service.py
from typing import List  # Add this line
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from models import Wishlist


class WishlistService:
    def __init__(self, db: Session):
        self.db = db

    def create_wishlist_item(self, user_id: int, imdb_movie_id: str) -> Wishlist:
        try:
            wishlist = Wishlist(user_id=user_id, imdb_movie_id=imdb_movie_id)
            self.db.add(wishlist)
            self.db.commit()
            self.db.refresh(wishlist)
            return wishlist
        except IntegrityError:
            raise HTTPException(status_code=400, detail="Duplicate wishlist item")

    def get_wishlist_item(self, wishlist_id: int, user_id: int) -> Wishlist:
        wishlist_item = self.db.query(Wishlist).filter(Wishlist.id == wishlist_id).first()
        if wishlist_item is None or wishlist_item.user_id != user_id:
            raise HTTPException(status_code=404, detail="Wishlist item not found")
        return wishlist_item

    def update_wishlist_item(self, wishlist_id: int, user_id: int, imdb_movie_id: str) -> Wishlist:
        wishlist_item = self.db.query(Wishlist).filter(Wishlist.id == wishlist_id).first()
        if wishlist_item is None or wishlist_item.user_id != user_id:
            raise HTTPException(status_code=404, detail="Wishlist item not found")
        wishlist_item.imdb_movie_id = imdb_movie_id
        self.db.commit()
        self.db.refresh(wishlist_item)
        return wishlist_item

    def delete_wishlist_item(self, wishlist_id: int, user_id: int) -> Wishlist:
        wishlist_item = self.db.query(Wishlist).filter(Wishlist.id == wishlist_id).first()
        if wishlist_item is None or wishlist_item.user_id != user_id:
            raise HTTPException(status_code=404, detail="Wishlist item not found")
        self.db.delete(wishlist_item)
        self.db.commit()
        return wishlist_item

    def get_all_wishlists(self, user_id: int) -> List[Wishlist]:
        wishlists = self.db.query(Wishlist).filter(Wishlist.user_id == user_id).all()
        return wishlists
