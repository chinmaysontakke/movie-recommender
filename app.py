import pickle
import streamlit as st
import requests
import time
import json
import os
from streamlit_extras.switch_page_button import switch_page

# ---------------------------------
# Helper functions
# ---------------------------------

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    data = requests.get(url).json()
    poster_path = data.get('poster_path')
    if poster_path:
        full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
        return full_path
    else:
        return "https://via.placeholder.com/500x750?text=No+Image"

def recommend(movie):
    available_movies = movies[movies['title'] != movie]
    recommended_movies = available_movies.sample(5)
    recommended_movie_names = []
    recommended_movie_posters = []
    for idx, row in recommended_movies.iterrows():
        movie_id = row['movie_id']
        recommended_movie_names.append(row['title'])
        recommended_movie_posters.append(fetch_poster(movie_id))
    return recommended_movie_names, recommended_movie_posters

# ---------------------------------
# Load Data
# ---------------------------------

movies = pickle.load(open('model/movie_list.pkl', 'rb'))

# ---------------------------------
# User Management
# ---------------------------------

USERS_FILE = "users.json"

def load_users():
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, "w") as f:
            json.dump({}, f)
    with open(USERS_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)

users = load_users()

# ---------------------------------
# Session states
# ---------------------------------

if 'page' not in st.session_state:
    st.session_state.page = 'login'

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# ---------------------------------
# Toast Notifications
# ---------------------------------

def toast(msg, state="success"):
    colors = {
        "success": "#4BB543",
        "error": "#FF3333",
        "info": "#3498db"
    }
    color = colors.get(state, "#4BB543")
    st.markdown(f"""
        <div style="background-color: {color}; padding:10px; border-radius:5px; margin-bottom:10px; color: white;">
            {msg}
        </div>
        """, unsafe_allow_html=True)

# ---------------------------------
# Fancy Navbar
# ---------------------------------

def navbar():
    st.markdown("""
        <style>
        .navbar {
            background: linear-gradient(90deg, rgba(0,212,255,1) 0%, rgba(9,9,121,1) 50%, rgba(2,0,36,1) 100%);
            padding: 10px;
            border-radius: 12px;
            margin-bottom: 20px;
        }
        .navbar a {
            color: white;
            padding: 14px 20px;
            text-decoration: none;
            font-weight: bold;
            font-size: 18px;
        }
        .navbar a:hover {
            background-color: #ddd;
            color: black;
            border-radius: 5px;
        }
        </style>

        <div class="navbar">
            <a href="#home">🏠 Home</a>
            <a href="#login">🔐 Login</a>
            <a href="#signup">📝 Sign Up</a>
            <a href="#forgot">🔑 Forgot Password</a>
        </div>
    """, unsafe_allow_html=True)

# ---------------------------------
# Pages
# ---------------------------------

def login_page():
    navbar()
    st.title("🔐 Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username in users and users[username] == password:
            toast("Login Successful ✅", "success")
            st.session_state.logged_in = True
            st.session_state.page = 'home'
            time.sleep(1)
            st.experimental_rerun()
        else:
            toast("Invalid username or password ❌", "error")

    st.info("Don't have an account?")
    if st.button("Sign Up Here"):
        st.session_state.page = 'signup'
        st.experimental_rerun()

    st.info("Forgot Password?")
    if st.button("Reset Password"):
        st.session_state.page = 'forgot'
        st.experimental_rerun()

def signup_page():
    navbar()
    st.title("📝 Sign Up")

    new_username = st.text_input("New Username")
    new_password = st.text_input("New Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    if st.button("Sign Up"):
        if new_username in users:
            toast("Username already exists ❌", "error")
        elif new_password != confirm_password:
            toast("Passwords do not match ❌", "error")
        else:
            users[new_username] = new_password
            save_users(users)
            toast("Account created successfully 🎉", "success")
            st.session_state.page = 'login'
            time.sleep(1)
            st.experimental_rerun()

    if st.button("Back to Login"):
        st.session_state.page = 'login'
        st.experimental_rerun()

def forgot_password_page():
    navbar()
    st.title("🔑 Forgot Password")

    username = st.text_input("Enter your Username")

    if st.button("Recover Password"):
        if username in users:
            toast(f"Your password is: {users[username]}", "info")
        else:
            toast("Username not found ❌", "error")

    if st.button("Back to Login"):
        st.session_state.page = 'login'
        st.experimental_rerun()

def home_page():
    navbar()
    st.title("🎬 Movie Recommender 🍿")

    movie_list = movies['title'].values
    selected_movie = st.selectbox(
        "Choose a Movie you like",
        movie_list
    )

    if st.button('Show Recommendations'):
        recommended_movie_names, recommended_movie_posters = recommend(selected_movie)

        cols = st.columns(5)
        for idx, col in enumerate(cols):
            with col:
                st.image(recommended_movie_posters[idx], use_column_width=True)
                st.caption(recommended_movie_names[idx])

    if st.button('Logout'):
        st.session_state.logged_in = False
        st.session_state.page = 'login'
        toast("Logged out Successfully ✅", "success")
        time.sleep(1)
        st.experimental_rerun()

# ---------------------------------
# Main
# ---------------------------------

if st.session_state.page == 'login':
    login_page()
elif st.session_state.page == 'signup':
    signup_page()
elif st.session_state.page == 'forgot':
    forgot_password_page()
elif st.session_state.page == 'home':
    if st.session_state.logged_in:
        home_page()
    else:
        st.session_state.page = 'login'
        st.experimental_rerun()
