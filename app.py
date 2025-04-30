import pickle
import streamlit as st
import requests

# Set Streamlit page configuration - must be FIRST Streamlit command
st.set_page_config(page_title="Movie Recommender", page_icon="🍿", layout="wide")

# Apply custom CSS with background image
page_bg_img = '''
<style>
body {
background-image: url("https://img.freepik.com/free-photo/3d-cinema-theatre-room-with-seating_23-2151005451.jpg?t=st=1746025320~exp=1746028920~hmac=398453dea2c2d5ac85daa1995609f2b881e81ef7faf8975c97eeb4f5ad48c73b&w=1380");
background-size: cover;
background-repeat: no-repeat;
background-attachment: fixed;
background-position: center;
}
.stApp {
    background-color: rgba(0, 0, 0, 0.7);  /* optional dark overlay */
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
    color: #fff;
    font-size: 14px;
}
h1, h2, h3, h4, h5, h6, p, div {
    color: #fff !important;
}
</style>
'''
st.markdown(page_bg_img, unsafe_allow_html=True)

# ---------------------------------
# Helper Functions
# ---------------------------------

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    data = requests.get(url).json()
    poster_path = data.get('poster_path')
    rating = data.get('vote_average', 'N/A')
    if poster_path:
        return "https://image.tmdb.org/t/p/w500/" + poster_path, rating
    else:
        return "https://via.placeholder.com/500x750?text=No+Image", rating

def recommend(movie):
    available_movies = movies[movies['title'] != movie]
    recommended_movies = available_movies.sample(5)
    names, posters, ratings = [], [], []
    for _, row in recommended_movies.iterrows():
        poster, rating = fetch_poster(row['movie_id'])
        names.append(row['title'])
        posters.append(poster)
        ratings.append(rating)
    return names, posters, ratings

def random_recommend():
    random_movies = movies.sample(5)
    names, posters, ratings = [], [], []
    for _, row in random_movies.iterrows():
        poster, rating = fetch_poster(row['movie_id'])
        names.append(row['title'])
        posters.append(poster)
        ratings.append(rating)
    return names, posters, ratings

# ---------------------------------
# Load Data
# ---------------------------------

try:
    movies = pickle.load(open('movies.pkl', 'rb'))
except Exception as e:
    st.error(f"Error loading movie data: {e}")
    st.stop()

# ---------------------------------
# ---------------------------------
# ---------------------------------
# Login System (simple centered design)
# ---------------------------------
USER_CREDENTIALS = {"admin":"1234","user":"password"}
def login(u,p): return USER_CREDENTIALS.get(u)==p

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    # CSS for centering and card style
    st.markdown("""
    <style>
      .login-wrapper {
        position: fixed;
        top: 0; left: 0; right: 0; bottom: 0;
        display: flex;
        justify-content: center;
        align-items: center;
        background: rgba(0,0,0,0.5);
        z-index: 1;
      }
      .login-card {
        background: rgba(255,255,255,0.15);
        backdrop-filter: blur(10px);
        padding: 2.5rem;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        width: 320px;
      }
      .login-card h2 {
        color: #fff;
        text-align: center;
        margin-bottom: 1.5rem;
        font-weight: bold;
      }
      .login-card .stTextInput > div > input {
        background: rgba(255,255,255,0.2) !important;
        color: #fff !important;
        border: none !important;
        border-radius: 4px !important;
        padding: 0.5rem !important;
        margin-bottom: 1rem !important;
        font-weight: bold !important;
      }
      .login-card .stTextInput > div > input::placeholder {
        color: #eee !important;
      }
      .login-card .stButton > button {
        width: 100%;
        background: #ff4b4b !important;
        color: #fff !important;
        border: none !important;
        padding: 0.6rem;
        font-weight: bold;
        border-radius: 4px;
      }
    </style>
    <div class="login-wrapper">
      <div class="login-card">
        <h2>🔒 Sign In</h2>
    """, unsafe_allow_html=True)

    with st.form("login_form"):
        username = st.text_input("Username", placeholder="Your username")
        password = st.text_input("Password", type="password", placeholder="Your password")
        submitted = st.form_submit_button("Login")

    if submitted:
        if login(username, password):
            st.session_state.logged_in = True
            st.session_state.username = username
            st.experimental_rerun()
        else:
            st.error("Invalid credentials", icon="⚠️")

    st.markdown("</div></div>", unsafe_allow_html=True)
    st.stop()
    # Logout button
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
    selected_movie = st.selectbox("Type or select a movie from the dropdown", movie_list)

    cols_action = st.columns(2)

    with cols_action[0]:
        if st.button('Show Recommendation 🎯'):
            with st.spinner('Fetching recommendations... 🎥'):
                names, posters, ratings = recommend(selected_movie)

            st.markdown("### Recommended Movies:")
            cols = st.columns(5)
            for idx, col in enumerate(cols):
                with col:
                    st.image(posters[idx], use_container_width=True)
                    st.markdown(f"<div class='movie-title'>{names[idx]}</div>", unsafe_allow_html=True)
                    st.markdown(f"<div class='rating'>⭐ {ratings[idx]}</div>", unsafe_allow_html=True)

    with cols_action[1]:
        if st.button('Surprise Me! 🎲'):
            with st.spinner('Fetching random picks... 🎥'):
                names, posters, ratings = random_recommend()

            st.markdown("### Random Movie Picks:")
            cols = st.columns(5)
            for idx, col in enumerate(cols):
                with col:
                    st.image(posters[idx], use_container_width=True)
                    st.markdown(f"<div class='movie-title'>{names[idx]}</div>", unsafe_allow_html=True)
                    st.markdown(f"<div class='rating'>⭐ {ratings[idx]}</div>", unsafe_allow_html=True)
