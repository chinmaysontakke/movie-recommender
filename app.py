import pickle
import streamlit as st
import requests
import pandas as pd

# Set Streamlit page configuration
st.set_page_config(page_title="Netflix Recommender", page_icon="🍿", layout="wide")

# ---------------------------------
# Load Data
# ---------------------------------

try:
    movies = pickle.load(open('movies.pkl', 'rb'))
except Exception as e:
    st.error(f"Error loading movie data: {e}")
    st.stop()

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
# Styling
# ---------------------------------

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
    }

    .stApp {
        background-image: url("https://www.transparenttextures.com/patterns/asfalt-dark.png");
        background-color: #111 !important;
    }

    .navbar {
        position: fixed;
        top: 0;
        width: 100%;
        background-color: rgba(0,0,0,0.85);
        padding: 10px 30px;
        z-index: 999;
        display: flex;
        align-items: center;
        justify-content: space-between;
        box-shadow: 0 2px 10px rgba(0,0,0,0.3);
    }

    .navbar-title {
        color: #e50914;
        font-size: 24px;
        font-weight: 700;
    }

    .navbar-right {
        color: #ffffff;
        font-size: 14px;
    }

    .movie-title {
        font-weight: 600;
        font-size: 15px;
        text-align: center;
        color: #e1e1e1;
    }

    .rating {
        text-align: center;
        color: #ffcc00;
        font-size: 14px;
        margin-top: 4px;
    }

    .poster {
        border-radius: 12px;
        transition: transform 0.3s ease;
        box-shadow: 0 4px 12px rgba(0,0,0,0.4);
    }

    .poster:hover {
        transform: scale(1.05);
    }

    .stButton > button {
        background-color: #e50914;
        color: #ffffff;
        border: none;
        border-radius: 10px;
        padding: 10px 20px;
        font-weight: 500;
        font-size: 16px;
        transition: background-color 0.3s;
    }

    .stButton > button:hover {
        background-color: #ff1e1e;
    }

    .login-box {
        background-color: rgba(0, 0, 0, 0.75);
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.5);
        color: #ffffff !important;
    }

    .stTextInput > div > input {
        background-color: #1f1f1f;
        color: #fff;
        border: 1px solid #444;
        border-radius: 8px;
    }

    .stTextInput > div > input::placeholder {
        color: #999;
    }

    /* Enhanced dropdown styling */
    .stSelectbox > div > div {
        background-color: #1f1f1f !important;
        color: #ffffff !important;
        border-radius: 8px;
        border: 1px solid #666;
        font-size: 15px;
    }

    .stSelectbox div[role="combobox"] span {
        color: #ffffff !important;
    }

    /* Dropdown options styling */
    ul[data-baseweb="menu"] {
        background-color: #1f1f1f !important;
        color: #ffffff !important;
        font-size: 14px;
    }

    ul[data-baseweb="menu"] li {
        padding: 8px 12px;
    }

    ul[data-baseweb="menu"] li:hover {
        background-color: #333333 !important;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------
# User Authentication
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
# Main App Interface
# ---------------------------------

if not st.session_state.logged_in:
    st.markdown("<h2 style='text-align: center;'>Login to Movie Recommender 🎬</h2>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([3, 2, 3])
    with col2:
        st.markdown('<div class="login-box">', unsafe_allow_html=True)
        with st.form(key="login_form"):
            username = st.text_input("Username", placeholder="Enter your username")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            submit_button = st.form_submit_button(label="Login")
        st.markdown('</div>', unsafe_allow_html=True)

        if submit_button:
            if login(username, password):
                st.success("Login Successful ✅")
                st.session_state.logged_in = True
                st.session_state.username = username
            else:
                st.error("Invalid Credentials ❌")

        st.markdown("<br><hr>", unsafe_allow_html=True)
        if 'show_signup' not in st.session_state:
            st.session_state.show_signup = False

        if st.button("New user? Sign Up"):
            st.session_state.show_signup = not st.session_state.show_signup

        if st.session_state.show_signup:
            st.markdown("### Create a New Account")
            with st.form(key="signup_form"):
                new_username = st.text_input("New Username", key="signup_user", placeholder="Choose a username")
                new_password = st.text_input("New Password", type="password", key="signup_pass", placeholder="Choose a password")
                signup_btn = st.form_submit_button("Create Account")

            if signup_btn:
                if new_username in USER_CREDENTIALS:
                    st.warning("Username already exists. Choose a different one.")
                elif new_username == "" or new_password == "":
                    st.warning("Username and password cannot be empty.")
                else:
                    USER_CREDENTIALS[new_username] = new_password
                    st.success("Account created successfully! You can now log in.")
                    st.session_state.show_signup = False

else:
    # Navbar
    st.markdown(f"""
    <div class='navbar'>
        <div class='navbar-title'>Netflix Recommender</div>
        <div class='navbar-right'>👤 {st.session_state.username}</div>
    </div>
    <br><br><br>
    """, unsafe_allow_html=True)

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
                    st.image(posters[idx], use_container_width=True, caption="")
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
#::contentReference[oaicite:0]{index=0}
 
