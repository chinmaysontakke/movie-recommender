import pickle
import streamlit as st
import requests
import json
import os

# ----------------- Helper Functions -----------------

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    data = requests.get(url).json()
    poster_path = data.get('poster_path')
    if poster_path:
        full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
        return full_path
    else:
        return "https://via.placeholder.com/300x450?text=No+Image"

def recommend(movie):
    available_movies = movies[movies['title'] != movie]
    recommended_movies = available_movies.sample(5)
    recommended_movie_names = recommended_movies['title'].tolist()
    recommended_movie_ids = recommended_movies['movie_id'].tolist()
    recommended_movie_posters = [fetch_poster(mid) for mid in recommended_movie_ids]
    return recommended_movie_names, recommended_movie_posters

# User Authentication Functions
def load_users():
    if os.path.exists("users.json"):
        with open("users.json", "r") as f:
            return json.load(f)
    else:
        return {}

def save_users(users):
    with open("users.json", "w") as f:
        json.dump(users, f)

def signup(username, password):
    users = load_users()
    if username in users:
        return False
    users[username] = {"password": password}
    save_users(users)
    return True

def login(username, password):
    users = load_users()
    if username in users and users[username]['password'] == password:
        return True
    return False

def forgot_password(username, new_password):
    users = load_users()
    if username in users:
        users[username]['password'] = new_password
        save_users(users)
        return True
    return False

# ----------------- Main Streamlit App -----------------

# Set Background Color
page_bg = """
<style>
[data-testid="stAppViewContainer"] {
    background-color: #DCE3F2;
}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# Load Movie Data
movies = pickle.load(open('movies.pkl', 'rb'))

# Page Control
if "page" not in st.session_state:
    st.session_state.page = "login"

# ----------------- Pages -----------------

if st.session_state.page == "login":
    st.title("🎬 Movie Recommender System - Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if login(username, password):
            st.success("Login successful!")
            st.session_state.page = "home"
            st.session_state.username = username
            st.experimental_rerun()
        else:
            st.error("Invalid username or password!")

    st.info("Don't have an account? Sign up below.")
    if st.button("Sign Up"):
        st.session_state.page = "signup"

    st.info("Forgot Password?")
    if st.button("Reset Password"):
        st.session_state.page = "forgot"

elif st.session_state.page == "signup":
    st.title("Sign Up")
    new_username = st.text_input("Choose a username")
    new_password = st.text_input("Choose a password", type="password")

    if st.button("Create Account"):
        if signup(new_username, new_password):
            st.success("Account created successfully! Please login.")
            st.session_state.page = "login"
        else:
            st.error("Username already exists!")

    if st.button("Back to Login"):
        st.session_state.page = "login"

elif st.session_state.page == "forgot":
    st.title("Reset Password")
    reset_username = st.text_input("Enter your username")
    reset_password = st.text_input("Enter new password", type="password")

    if st.button("Reset"):
        if forgot_password(reset_username, reset_password):
            st.success("Password reset successful! Please login.")
            st.session_state.page = "login"
        else:
            st.error("Username not found!")

    if st.button("Back to Login"):
        st.session_state.page = "login"

elif st.session_state.page == "home":
    st.title(f"Welcome, {st.session_state.username}! 🎬🍿")

    movie_list = movies['title'].values
    selected_movie = st.selectbox(
        "Type or select a movie from the dropdown",
        movie_list
    )

    if st.button('Show Recommendation'):
        with st.spinner('Fetching awesome recommendations for you... 🍿🎬'):
            recommended_movie_names, recommended_movie_posters = recommend(selected_movie)

            cols = st.columns(5)
            for idx in range(5):
                with cols[idx]:
                    st.image(recommended_movie_posters[idx])
                    st.caption(recommended_movie_names[idx])

    if st.button("Logout"):
        st.session_state.page = "login"
        st.experimental_rerun()
