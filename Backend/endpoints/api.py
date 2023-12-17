from fastapi import APIRouter
import endpoints.auth as auth
import endpoints.library as library
import endpoints.wishlist as wishlist
from endpoints import search


api_router = APIRouter()
api_router.include_router(auth.router, tags=['auth'])
api_router.include_router(wishlist.router, tags=['wishlist'])
api_router.include_router(library.router, tags=['library'])
api_router.include_router(search.router, tags=['search'])
