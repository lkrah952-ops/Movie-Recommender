import streamlit as st
from recommender import get_recommendations_with_reason
from tmdb_client import get_genres, get_trending, search_movie, get_movie_details
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="TMDB Movie Recommender", layout="wide")
st.title("🎬 TMDB Movie Recommender System")

# --- Main movie input ---
movie_name = st.text_input("Enter a movie you like:")

# --- Sidebar filters ---
st.sidebar.header("Filters")
min_year = st.sidebar.number_input("Min Year", 1900, 2100, 2000)
max_year = st.sidebar.number_input("Max Year", 1900, 2100, 2025)
min_rating = st.sidebar.slider("Minimum Rating", 0.0, 10.0, 0.0, 0.1)
runtime_min = st.sidebar.number_input("Min Runtime (min)", 0, 500, 0)
runtime_max = st.sidebar.number_input("Max Runtime (min)", 0, 500, 300)
genres_list = list(get_genres().values())
selected_genres = st.sidebar.multiselect("Select Genres", genres_list)

# --- Trending movies visualization ---
st.sidebar.subheader("Trending Movies")
trending = get_trending()
for t in trending:
    st.sidebar.write("• " + t)

# Bar chart for trending
df = pd.DataFrame({"Movie": trending, "Popularity": range(len(trending), 0, -1)})
fig = px.bar(df, x="Movie", y="Popularity", color="Popularity",
             title="Trending Movies This Week")
st.plotly_chart(fig)

# --- Watchlist ---
if "watchlist" not in st.session_state:
    st.session_state.watchlist = []

st.sidebar.subheader("Your Watchlist")
new_movie = st.sidebar.text_input("Add a movie to your watchlist")
if st.sidebar.button("Add to Watchlist") and new_movie.strip():
    st.session_state.watchlist.append(new_movie)
    st.sidebar.success(f"Added {new_movie}!")

for m in st.session_state.watchlist:
    st.sidebar.write("• " + m)

# --- Get Recommendations ---
if st.button("Recommend"):
    if movie_name.strip():
        recs_with_reason = get_recommendations_with_reason(
            movie_name,
            top_n=10,
            min_year=min_year,
            max_year=max_year,
            min_rating=min_rating,
            runtime_min=runtime_min,
            runtime_max=runtime_max,
            genres_selected=selected_genres
        )
        st.subheader("Recommended Movies:")
        for r, reason in recs_with_reason:
            st.write(f"• {r} ({reason})")
    else:
        st.warning("Please enter a movie name.")
