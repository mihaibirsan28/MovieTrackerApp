from fastapi import APIRouter
import auth
import library
import wishlist


api_router = APIRouter()
api_router.include_router(auth.router, prefix='/auth', tags=['auth'])
api_router.include_router(wishlist.router, prefix='/wishlist', tags=['wishlist'])
api_router.include_router(library.router, prefix='/library', tags=['library'])
