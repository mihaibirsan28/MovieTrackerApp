from typing import List
import requests

from models import Wishlist, Library
from secrets import X_RAPID_API_HOST, X_RAPID_API_KEY


def load_wish_list(movie_list: List[Wishlist]):
    results = []
    for movie in movie_list:
        result = load_movie(movie.imdb_movie_id)
        if result:
            results.append(result)
    return results


def load_library(movie_list: List[Library]):
    results = []
    for movie in movie_list:
        result = load_movie(movie.imdb_movie_id)
        if result:
            results.append(result)
    return results


def load_movie(imdb_movie_id: str):
    headers = {
        'X-RapidAPI-Host': X_RAPID_API_HOST,
        'X-RapidAPI-Key': X_RAPID_API_KEY
    }
    request_url = f'https://{X_RAPID_API_HOST}/titles/{imdb_movie_id}'
    request_response = requests.get(url=request_url, headers=headers)
    if request_response.status_code == 200:
        request_response_data = request_response.json().get('results')
        return request_response_data
    else:
        return None
