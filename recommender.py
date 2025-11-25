from tmdb_client import search_movie, get_movie_details, filter_movie

# Simple in-memory cache to reduce repeated API calls
movie_cache = {}

def get_recommendations(movie_title, top_n=5,
                        min_year=1900, max_year=2100,
                        min_rating=0, runtime_min=0, runtime_max=500,
                        genres_selected=None):
    """
    Returns a list of recommended movie titles based on TMDB search.
    Applies filtering.
    """
    results = search_movie(movie_title)
    if not results:
        return ["No results found. Try another movie."]

    similar_movies = []
    for m in results[:50]:  # top 50 search results
        movie_id = m["id"]
        if movie_id in movie_cache:
            details = movie_cache[movie_id]
        else:
            details = get_movie_details(movie_id)
            movie_cache[movie_id] = details

        if filter_movie(details, min_year, max_year,
                        min_rating, runtime_min, runtime_max,
                        genres_selected):
            similar_movies.append(details.get("title", ""))

    return similar_movies[:top_n] if similar_movies else ["No movies match filters."]


def get_recommendations_with_reason(movie_title, top_n=5,
                                    min_year=1900, max_year=2100,
                                    min_rating=0, runtime_min=0, runtime_max=500,
                                    genres_selected=None):
    """
    Returns a list of recommended movies with a simple explanation for each.
    Explanation currently uses shared genres for demonstration.
    """
    recs = get_recommendations(movie_title, top_n=top_n,
                               min_year=min_year, max_year=max_year,
                               min_rating=min_rating,
                               runtime_min=runtime_min, runtime_max=runtime_max,
                               genres_selected=genres_selected)

    recs_with_reason = []
    for r in recs:
        # Check if it's an error message
        if "No" in r:
            recs_with_reason.append((r, ""))
            continue

        # Get movie details to build explanation
        search_results = search_movie(r)
        if not search_results:
            recs_with_reason.append((r, ""))
            continue

        movie_id = search_results[0]["id"]
        if movie_id in movie_cache:
            details = movie_cache[movie_id]
        else:
            details = get_movie_details(movie_id)
            movie_cache[movie_id] = details

        # Simple reason: show shared genres
        genres = [g["name"] for g in details.get("genres", [])]
        reason = f"Shared genres: {', '.join(genres)}" if genres else "Reason not available"
        recs_with_reason.append((r, reason))

    return recs_with_reason
