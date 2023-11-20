from fastapi import APIRouter
import endpoints.auth as auth
import endpoints.library as library
import endpoints.wishlist as wishlist


api_router = APIRouter()
api_router.include_router(auth.router, prefix='/auth', tags=['auth'])
api_router.include_router(wishlist.router, prefix='/wishlist', tags=['wishlist'])
api_router.include_router(library.router, prefix='/library', tags=['library'])
