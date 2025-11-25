import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("TMDB_API_KEY")
BASE_URL = "https://api.themoviedb.org/3"

def search_movie(title):
    """
    Search TMDB for movies matching the given title.
    """
    url = f"{BASE_URL}/search/movie"
    params = {"api_key": API_KEY, "query": title}
    res = requests.get(url, params=params).json()
    return res.get("results", [])

def get_movie_details(movie_id):
    """
    Get detailed info for a movie including credits.
    """
    url = f"{BASE_URL}/movie/{movie_id}"
    params = {"api_key": API_KEY, "append_to_response": "credits"}
    res = requests.get(url, params=params).json()
    return res

def get_genres():
    """
    Return a dictionary of genre ID -> name.
    """
    url = f"{BASE_URL}/genre/movie/list"
    params = {"api_key": API_KEY}
    res = requests.get(url, params=params).json()
    return {g["id"]: g["name"] for g in res.get("genres", [])}

def get_trending():
    """
    Return top 10 trending movies this week.
    """
    url = f"{BASE_URL}/trending/movie/week"
    params = {"api_key": API_KEY}
    res = requests.get(url, params=params).json()
    return [m["title"] for m in res.get("results", [])[:10]]

def filter_movie(details, min_year=1900, max_year=2100,
                 min_rating=0, runtime_min=0, runtime_max=500,
                 genres_selected=None):
    """
    Returns True if movie passes filters.
    """
    release_date = details.get("release_date", "")
    release_year = int(release_date[:4]) if release_date else 0
    rating = details.get("vote_average", 0)
    runtime = details.get("runtime", 0)
    genres = [g["name"] for g in details.get("genres", [])]

    if not (min_year <= release_year <= max_year):
        return False
    if rating < min_rating:
        return False
    if not (runtime_min <= runtime <= runtime_max):
        return False
    if genres_selected and not any(g in genres for g in genres_selected):
        return False
    return True
