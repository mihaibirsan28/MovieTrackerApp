from fastapi import FastAPI, Query, APIRouter
from typing import Any

from starlette import status
from secrets import X_RAPID_API_KEY, X_RAPID_API_HOST
import requests


router = APIRouter()


@router.get("/search/{movie_title}", status_code=status.HTTP_200_OK, response_model=Any)
async def search_movie_title(
        movie_title: str,
        exact: bool = Query(False, description="Exact search for title"),
        year: int = Query(None, description="Filter by release year"),
        page: str = Query("1", description="Page number"),
        endYear: int = Query(None, description="Filter by max release year"),
        startYear: int = Query(None, description="Filter by min release year"),
        titleType: str = Query(None, description="Filter by movie type: movie or series"),
        limit: int = Query(10, description="Number of results per page")
):
    external_api_url = f"https://{X_RAPID_API_HOST}/search/title/{movie_title}"
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
    print("Status code " + str(external_api_response.status_code))
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
async def get_movie_by_id(movie_id: int):
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


def get_headers():
    headers = {
        "X-RapidAPI-Host": X_RAPID_API_HOST,
        "X-RapidAPI-Key": X_RAPID_API_KEY
    }
    return headers
