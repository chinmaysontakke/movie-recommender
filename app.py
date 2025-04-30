import pickle
import streamlit as st
import requests

# Set Streamlit page configuration - must be FIRST Streamlit command
st.set_page_config(page_title="Movie Recommender", page_icon="🍿", layout="wide")

# Apply custom CSS with background image
page_bg_img = '''
<style>
.stApp {
    background-image: url("https://www.filmmakersacademy.com/wp-content/uploads/2020/01/EOQ_t9SW4AEY0Uk.jpeg");
    background-size: cover;
    background-repeat: no-repeat;
    background-attachment: fixed;
    background-position: center;
    background-color: rgba(0, 0, 0, 0.7);
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
# Main App Interface
# ---------------------------------

if not st.session_state.logged_in:
    st.markdown("<h2 style='text-align: center;'>Login to Movie Recommender 🎬</h2>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([3, 2, 3])
    with col2:
        st.markdown("""
            <style>
            .login-box {
                background-color: rgba(0, 0, 0, 0.6);
                padding: 30px;
                border-radius: 15px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.4);
                backdrop-filter: blur(6px);
                color: white !important;
            }
            .login-box label {
                color: #ffffff !important;
                font-weight: 500;
            }
            .stTextInput > div > input {
                background-color: #1e1e1e;
                color: white;
                border: 1px solid #333;
            }
            .stTextInput > div > input::placeholder {
                color: #aaa;
            }
            </style>
        """, unsafe_allow_html=True)

        with st.container():
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

        # Sign-up section toggle
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
