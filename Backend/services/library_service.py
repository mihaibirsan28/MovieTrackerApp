# library_service.py
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from models import Library, User

class LibraryService:
    def __init__(self, db: Session):
        self.db = db

    def create_library_item(self, user_id: int, imdb_movie_id: str) -> Library:
        try:
            library = Library(user_id=user_id, imdb_movie_id=imdb_movie_id)
            self.db.add(library)
            self.db.commit()
            self.db.refresh(library)
            return library
        except IntegrityError:
            raise HTTPException(status_code=400, detail="Duplicate library item")

    def get_library_item(self, library_id: int, user_id: int) -> Library:
        library_item = self.db.query(Library).filter(Library.id == library_id).first()
        if library_item is None or library_item.user_id != user_id:
            raise HTTPException(status_code=404, detail="Library item not found")
        return library_item

    def update_library_item(self, library_id: int, user_id: int, imdb_movie_id: str) -> Library:
        library_item = self.db.query(Library).filter(Library.id == library_id).first()
        if library_item is None or library_item.user_id != user_id:
            raise HTTPException(status_code=404, detail="Library item not found")
        library_item.imdb_movie_id = imdb_movie_id
        self.db.commit()
        self.db.refresh(library_item)
        return library_item

    def delete_library_item(self, library_id: int, user_id: int) -> Library:
        library_item = self.db.query(Library).filter(Library.id == library_id).first()
        if library_item is None or library_item.user_id != user_id:
            raise HTTPException(status_code=404, detail="Library item not found")
        self.db.delete(library_item)
        self.db.commit()
        return library_item

    def get_all_libraries(self, user_id: int) -> list:
        libraries = self.db.query(Library).filter(Library.user_id == user_id).all()
        return libraries

    @staticmethod
    def is_owner_of_library(user: User, library: Library) -> bool:
        return library.user_id == user.id
