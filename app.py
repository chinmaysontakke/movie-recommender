import pickle
import streamlit as st
import requests

# ---------------------------------
# Helper functions
# ---------------------------------

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    data = requests.get(url)
    data = data.json()
    poster_path = data.get('poster_path')
    rating = data.get('vote_average', 'N/A')
    plot = data.get('overview', 'No plot available.')
    trailer_url = f"https://www.youtube.com/results?search_query={data['title']}+trailer"  # You can modify this to use actual trailer URL if API is available
    if poster_path:
        full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
        return full_path, rating, plot, trailer_url
    else:
        return "https://via.placeholder.com/500x750?text=No+Image", rating, plot, trailer_url

def recommend(movie, genre_filter=None, min_rating=0):
    available_movies = movies[movies['title'] != movie]
    if genre_filter:
        available_movies = available_movies[available_movies['genre'] == genre_filter]
    if min_rating > 0:
        available_movies = available_movies[available_movies['rating'] >= min_rating]
    
    recommended_movies = available_movies.sample(5)
    recommended_movie_names = []
    recommended_movie_posters = []
    recommended_movie_ratings = []
    recommended_movie_plots = []
    recommended_movie_trailers = []
    
    for idx, row in recommended_movies.iterrows():
        movie_id = row['movie_id']
        poster, rating, plot, trailer = fetch_poster(movie_id)
        recommended_movie_names.append(row['title'])
        recommended_movie_posters.append(poster)
        recommended_movie_ratings.append(rating)
        recommended_movie_plots.append(plot)
        recommended_movie_trailers.append(trailer)
    
    return recommended_movie_names, recommended_movie_posters, recommended_movie_ratings, recommended_movie_plots, recommended_movie_trailers

def random_recommend(genre_filter=None, min_rating=0):
    random_movies = movies.sample(5)
    if genre_filter:
        random_movies = random_movies[random_movies['genre'] == genre_filter]
    if min_rating > 0:
        random_movies = random_movies[random_movies['rating'] >= min_rating]
    
    random_movie_names = []
    random_movie_posters = []
    random_movie_ratings = []
    random_movie_plots = []
    random_movie_trailers = []
    
    for idx, row in random_movies.iterrows():
        movie_id = row['movie_id']
        poster, rating, plot, trailer = fetch_poster(movie_id)
        random_movie_names.append(row['title'])
        random_movie_posters.append(poster)
        random_movie_ratings.append(rating)
        random_movie_plots.append(plot)
        random_movie_trailers.append(trailer)
    
    return random_movie_names, random_movie_posters, random_movie_ratings, random_movie_plots, random_movie_trailers

# ---------------------------------
# Load data
# ---------------------------------

try:
    movies = pickle.load(open('movies.pkl', 'rb'))
except Exception as e:
    st.error(f"Error loading movie data: {e}")
    st.stop()

# ---------------------------------
# Login System
# ---------------------------------

USER_CREDENTIALS = {
    "admin": "1234",
    "user": "password"
}

def login(username, password):
    return USER_CREDENTIALS.get(username) == password

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# ---------------------------------
# Streamlit App
# ---------------------------------

st.set_page_config(page_title="Movie Recommender", page_icon="🍿", layout="wide")

# Apply custom CSS
st.markdown("""
    <style>
        .stApp {
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        }
        .poster {
            border-radius: 15px;
            transition: 0.3s;
        }
        .poster:hover {
            transform: scale(1.05);
        }
        .movie-title {
            font-weight: bold;
            font-size: 16px;
            text-align: center;
        }
        .rating {
            text-align: center;
            color: #666;
            font-size: 14px;
        }
        .logout-button {
            position: absolute;
            top: 10px;
            right: 10px;
        }
    </style>
""", unsafe_allow_html=True)

if not st.session_state.logged_in:
    st.markdown("<h2 style='text-align: center;'>Login to Movie Recommender 🎬</h2>", unsafe_allow_html=True)
    with st.form(key="login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit_button = st.form_submit_button(label="Login")

    if submit_button:
        if login(username, password):
            st.success("Login Successful ✅")
            st.session_state.logged_in = True
            st.session_state.username = username
        else:
            st.error("Invalid Credentials ❌")
else:
    # Top bar with logout
    with st.container():
        cols_top = st.columns([8, 1])
        with cols_top[1]:
            if st.button("Logout", key="logout", help="Logout", type="primary"):
                st.session_state.logged_in = False
                st.session_state.username = None
                st.experimental_rerun()

    st.markdown("<h1 style='text-align: center;'>Movie Recommender System 🍿</h1>", unsafe_allow_html=True)
    st.write(f"### Welcome, **{st.session_state.username}** 👋")

    movie_list = movies['title'].values
    selected_movie = st.selectbox(
        "Type or select a movie from the dropdown",
        movie_list
    )

    # Filter by Genre
    genres = movies['genre'].unique()
    selected_genre = st.selectbox("Select Genre", ['All'] + list(genres))

    # Filter by Rating
    min_rating = st.slider("Select Minimum Rating", 0, 10, 5)

    # Action Buttons
    cols_action = st.columns(2)
    with cols_action[0]:
        if st.button('Show Recommendation 🎯'):
            with st.spinner('Fetching recommendations... 🎥'):
                recommended_movie_names, recommended_movie_posters, recommended_movie_ratings, recommended_movie_plots, recommended_movie_trailers = recommend(
                    selected_movie, selected_genre if selected_genre != 'All' else None, min_rating)
            
            st.markdown("### Recommended Movies:")
            cols = st.columns(5)
            for idx, col in enumerate(cols):
                with col:
                    st.image(recommended_movie_posters[idx], use_column_width=True, caption="")
                    st.markdown(f"<div class='movie-title'>{recommended_movie_names[idx]}</div>", unsafe_allow_html=True)
                    st.markdown(f"<div class='rating'>⭐ {recommended_movie_ratings[idx]}</div>", unsafe_allow_html=True)
                    st.markdown(f"<p>{recommended_movie_plots[idx]}</p>", unsafe_allow_html=True)
                    st.markdown(f"[Watch Trailer]({recommended_movie_trailers[idx]})", unsafe_allow_html=True)

    with cols_action[1]:
        if st.button('Surprise Me! 🎲'):
            with st.spinner('Fetching random picks... 🎥'):
                random_movie_names, random_movie_posters, random_movie_ratings, random_movie_plots, random_movie_trailers = random_recommend(
                    selected_genre if selected_genre != 'All' else None, min_rating)

            st.markdown("### Random Movie Picks:")
            cols = st.columns(5)
            for idx, col in enumerate(cols):
                with col:
                    st.image(random_movie_posters[idx], use_container_width=True)
                    st.markdown(f"<div class='movie-title'>{random_movie_names[idx]}</div>", unsafe_allow_html=True)
                    st.markdown(f"<div class='rating'>⭐ {random_movie_ratings[idx]}</div>", unsafe_allow_html=True)
                    st.markdown(f"<p>{random_movie_plots[idx]}</p>", unsafe_allow_html=True)
                    st.markdown(f"[Watch Trailer]({random_movie_trailers[idx]})", unsafe_allow_html=True)
