import streamlit as st
import pickle
import pandas as pd
import requests

# === API-Based Movie Details Fetching ===
def fetch_movie_details_from_omdb(title):
    api_key = "55212a5c"
    url = f"http://www.omdbapi.com/?t={title}&apikey={api_key}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        if data.get('Response', 'False') == 'False':
            return {
                "title": title,
                "poster": "https://via.placeholder.com/500x750?text=No+Poster",
                "plot": "No plot available.",
                "cast": "Unknown",
                "director": "Unknown",
                "genre": "N/A",
                "year": "N/A",
                "imdb_rating": "N/A"
            }
        poster_url = data.get('Poster')
        if not poster_url or poster_url == "N/A":
            poster_url = "https://via.placeholder.com/500x750?text=No+Poster"
        return {
            "title": data.get('Title', title),
            "poster": poster_url,
            "plot": data.get('Plot', 'No plot available.'),
            "cast": data.get('Actors', 'Unknown'),
            "director": data.get('Director', 'Unknown'),
            "genre": data.get('Genre', 'N/A'),
            "year": data.get('Year', 'N/A'),
            "imdb_rating": data.get('imdbRating', 'N/A')
        }
    except requests.exceptions.RequestException:
        return {
            "title": title,
            "poster": "https://via.placeholder.com/500x750?text=No+Poster",
            "plot": "No plot available due to connection error.",
            "cast": "Unknown",
            "director": "Unknown",
            "genre": "N/A",
            "year": "N/A",
            "imdb_rating": "N/A"
        }

# === Load Pickle Data ===
movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# === Recommendation Logic ===
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended = []
    for i in movie_list:
        recommended.append(fetch_movie_details_from_omdb(movies.iloc[i[0]]['title']))
    return recommended

# === Streamlit Page Configuration ===
st.set_page_config(page_title="🎬 Movie Recommender", layout="wide")

# === Custom CSS for Aesthetic ===
st.markdown("""
<style>
h1, h2, h3, h4, h5, h6 { color: #00FFAB; }
.stButton>button { background: linear-gradient(90deg, #00FFAB, #006E7F); color: black; font-weight: bold; border-radius: 8px; }
.stButton>button:hover { background: linear-gradient(90deg, #006E7F, #00FFAB); color: white; }
hr { border: 1px solid #00FFAB; }

.recommend-card {
    background-color: #1C1C1C;
    border-radius: 10px;
    padding: 8px;
    text-align: center;
    box-shadow: 0 0 10px rgba(0,255,171,0.2);
}

/* --- NEW POSTER GRID STYLING --- */
.poster-container {
    text-align: center;
    margin-bottom: 20px;
}
.poster-container img {
    width: 100%;
    height: 280px;   /* equal height for all posters */
    object-fit: cover;
    border-radius: 10px;
    box-shadow: 0 0 10px rgba(0,255,171,0.2);
}
.poster-caption {
    font-weight: bold;
    color: white;
    margin-top: 8px;
    font-size: 14px;
    height: 40px;   /* keeps all captions same height */
    overflow: hidden;
}
</style>
""", unsafe_allow_html=True)

# === Title ===
st.markdown("<h1 style='text-align:center;'>🎥 Movie Recommender System</h1>", unsafe_allow_html=True)

# === Top 10 Highest-Grossing Movies Till 2024 ===
st.subheader("🔥 Top 10 Highest-Grossing Movies Till 2024")

highest_grossing = [
    {"title": "Avatar", "poster": "https://tse2.mm.bing.net/th/id/OIP.np71vouQvwOfrsCgHM7qkAHaJQ?pid=Api&P=0&h=180.jpg"},
    {"title": "Avengers: Endgame", "poster": "https://upload.wikimedia.org/wikipedia/en/0/0d/Avengers_Endgame_poster.jpg"},
    {"title": "Avatar: The Way of Water", "poster": "https://tse1.mm.bing.net/th/id/OIP.RnGcu6u_zsdpXNniyPtAnAHaJQ?pid=Api&P=0&h=180.jpg"},
    {"title": "Titanic", "poster": "https://tse4.mm.bing.net/th/id/OIP.oYxhZo6EoxN_kWGeuRs0CwHaKu?pid=Api&P=0&h=180.jpg"},
    {"title": "Star Wars: The Force Awakens", "poster": "https://tse4.mm.bing.net/th/id/OIP.UaXcPMAAr-wynZC5c1XVEQHaKl?pid=Api&P=0&h=180.jpg"},
    {"title": "Avengers: Infinity War", "poster": "https://upload.wikimedia.org/wikipedia/en/4/4d/Avengers_Infinity_War_poster.jpg"},
    {"title": "Spider-Man: No Way Home", "poster": "https://upload.wikimedia.org/wikipedia/en/0/00/Spider-Man_No_Way_Home_poster.jpg"},
    {"title": "Jurassic World", "poster": "https://upload.wikimedia.org/wikipedia/en/6/6e/Jurassic_World_poster.jpg"},
    {"title": "The Lion King (2019)", "poster": "https://tse3.mm.bing.net/th/id/OIP.zXMiqAPvtN_oBq6bMR-nmgHaK-?pid=Api&P=0&h=180.jpg"},
    {"title": "The Avengers", "poster": "https://tse4.mm.bing.net/th/id/OIP.zNDZbJ1vd_HW_D_3F1zaYgHaLH?pid=Api&P=0&h=180.jpg"},
]

cols = st.columns(5)
for idx, movie in enumerate(highest_grossing):
    with cols[idx % 5]:
        st.markdown(f"""
        <div class='poster-container'>
            <img src='{movie["poster"]}' alt='{movie["title"]}'>
            <div class='poster-caption'>{movie["title"]}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

# === Must-Watch Movies Till 2024 ===
st.subheader("🎬 Must-Watch Movies Till 2024")

must_watch_movies = [
    {"title": "Oppenheimer", "poster": "https://tse1.mm.bing.net/th/id/OIP.h1RWD6yY8Y_aWhgTuYFTMgHaK9?pid=Api&P=0&h=180.jpg"},
    {"title": "Everything Everywhere All At Once", "poster": "https://tse4.mm.bing.net/th/id/OIP.lzIT1UB6hdBccteLcSkO-AHaKe?pid=Api&P=0&h=180.jpg"},
    {"title": "Top Gun: Maverick", "poster": "https://tse1.mm.bing.net/th/id/OIP.wOWaRBDpEj3SGo4-sE-vFAHaK4?pid=Api&P=0&h=180.jpg"},
    {"title": "Spider-Man: Across the Spider-Verse", "poster": "https://tse4.mm.bing.net/th/id/OIP.V0ustTI4Xr26oBuCCEV7GAHaK8?pid=Api&P=0&h=180.jpg"},
    {"title": "Dune: Part One", "poster": "https://tse2.mm.bing.net/th/id/OIP.wzA1MQvkcKBBainecb6b7gHaLF?pid=Api&P=0&h=180.jpg"},
    {"title": "The Batman", "poster": "https://tse3.mm.bing.net/th/id/OIP.xmlpgQS10ZMkJMjii-3boQHaLE?pid=Api&P=0&h=180.jpg"},
    {"title": "The Whale", "poster": "https://tse1.mm.bing.net/th/id/OIP.VsgC-j6WlesdIEwZJHhPAQHaK6?pid=Api&P=0&h=180.jpg"},
    {"title": "Avatar: The Way of Water", "poster": "https://tse1.mm.bing.net/th/id/OIP.RnGcu6u_zsdpXNniyPtAnAHaJQ?pid=Api&P=0&h=180.jpg"},
    {"title": "Mission: Impossible – Dead Reckoning Part One", "poster": "https://www.mauvais-genres.com/41687-large_default/mission-impossible-dead-reckoning-part-1-movie-poster-47x63-in-2023-christopher-mcquarrie-tom-cruise.jpg"},
    {"title": "John Wick: Chapter 4", "poster": "https://tse2.mm.bing.net/th/id/OIP.F4demVHwIlsAHLgyHr5FbQHaJV?pid=Api&P=0&h=180.jpg"},
]

cols = st.columns(5)
for idx, movie in enumerate(must_watch_movies):
    with cols[idx % 5]:
        st.markdown(f"""
        <div class='poster-container'>
            <img src='{movie["poster"]}' alt='{movie["title"]}'>
            <div class='poster-caption'>{movie["title"]}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

# === Movie Recommendation Section ===
st.subheader("✨ Get Personalized Recommendations")
selected_movie = st.selectbox(
    "🎬 Select a Movie:",
    movies['title'].values,
    index=None,
    placeholder="Type or select a movie to get recommendations...",
)

if st.button("Get Recommendations 🎥"):
    if selected_movie:
        recommendations = recommend(selected_movie)
        rec_cols = st.columns(5)
        for idx, movie in enumerate(recommendations):
            with rec_cols[idx % 5]:
                st.markdown(f"<div class='recommend-card'>", unsafe_allow_html=True)
                st.image(movie["poster"], use_container_width=True)
                st.markdown(f"**{movie['title']} ({movie['year']})**")
                st.markdown(f"⭐ **IMDB Rating:** {movie['imdb_rating']}")
