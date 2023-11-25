from fastapi import Query, APIRouter, Depends
from typing import Any

from starlette import status

from models import User
from secrets import X_RAPID_API_KEY, X_RAPID_API_HOST
from endpoints.auth import get_current_user
import requests
import logging
import sys


router = APIRouter()
logging.basicConfig(level=logging.DEBUG)


@router.get("/search/{movie_title}", status_code=status.HTTP_200_OK, response_model=Any)
async def search_movie_title(
        movie_title: str,
        current_user: User = Depends(get_current_user),
        exact: bool = Query(False, description="Exact search for title"),
        year: int = Query(None, description="Filter by release year"),
        page: str = Query("1", description="Page number"),
        endYear: int = Query(None, description="Filter by max release year"),
        startYear: int = Query(None, description="Filter by min release year"),
        titleType: str = Query(None, description="Filter by movie type: movie or series"),
        limit: int = Query(10, description="Number of results per page")
):
    external_api_url = f"https://{X_RAPID_API_HOST}/titles/search/title/{movie_title}"
    headers = get_headers()
    query_params = {
        "exact": exact,
        "year": year,
        "page": page,
        "endYear": endYear,
        "startYear": startYear,
        "titleType": titleType,
        "limit": limit
    }
    external_api_response = requests.get(external_api_url, headers=headers, params=query_params)
    logging.debug("Status code " + str(external_api_response.status_code))
    print("Status code " + str(external_api_response.status_code))
    sys.stdout.flush()
    if external_api_response.status_code == 200:
        external_api_response_data = external_api_response.json()
        return external_api_response_data
    else:
        default_response = {
            "page": "1",
            "next": None,
            "entries": 0,
            "results": []
        }
        return default_response


@router.get("/details/{movie_id}")
async def get_movie_by_id(movie_id: str):
    headers = get_headers()
    external_api_url = f"https://{X_RAPID_API_HOST}/titles/{movie_id}"
    external_api_response = requests.get(external_api_url, headers=headers)
    if external_api_response.status_code == 200:
        external_api_response_data = external_api_response.json()
        return external_api_response_data
    else:
        return {
            "message": "The id was not found!"
        }


@router.get("/random-movies")
async def get_random_movies(
        startYear: int = Query(None, description="Start year"),
        genre: str = Query(None, description="movie genres"),
        titleType: str = Query(None, description="Type of movie: series or movie"),
        limit: int = Query(10, description="Number of random movies, max 10"),
        endYear: int = Query(None, description="Max release year"),
        year: int = Query(None, description="Release year of movie"),
        listOfMovies: str = Query("most_pop_series", description="Where to get random movies from")):
    headers = get_headers()
    query_params = {
        "genre": genre,
        "year": year,
        "endYear": endYear,
        "startYear": startYear,
        "titleType": titleType,
        "limit": limit,
        "list": listOfMovies
    }
    external_api_url = f"https://{X_RAPID_API_HOST}/titles/random"
    external_api_response = requests.get(external_api_url, headers=headers, params=query_params)
    if external_api_response.status_code == 200:
        external_api_response_data = external_api_response.json()
        return external_api_response_data
    else:
        return {
            "message": "There was an error fetching the movies"
        }


def get_headers():
    headers = {
        "X-RapidAPI-Host": X_RAPID_API_HOST,
        "X-RapidAPI-Key": X_RAPID_API_KEY
    }
    return headers
