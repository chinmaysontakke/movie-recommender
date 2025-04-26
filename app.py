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
    background-color: #E3F2FD;
}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# Load Movie Data
movies = pickle.load(open('movies.pkl', 'rb'))

# Session Control
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""
if "current_page" not in st.session_state:
    st.session_state.current_page = "login"

# Top Right Corner Buttons
col1, col2 = st.columns([8, 1])

with col2:
    if st.session_state.logged_in:
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.session_state.current_page = "login"
            st.experimental_rerun()
    else:
        if st.button("Login"):
            st.session_state.current_page = "login"
            st.experimental_rerun()

# Navigation based on current page
if st.session_state.current_page == "login" and not st.session_state.logged_in:
    st.title("Login Page")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Login Now"):
        if login(username, password):
            st.success(f"Welcome {username}!")
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.current_page = "home"
            st.experimental_rerun()
        else:
            st.error("Invalid username or password!")

    st.info("Don't have an account? Go to Sign Up Page ➡️")
    if st.button("Go to Sign Up"):
        st.session_state.current_page = "signup"
        st.experimental_rerun()

    st.info("Forgot your password? ➡️")
    if st.button("Go to Forgot Password"):
        st.session_state.current_page = "forgot"
        st.experimental_rerun()

elif st.session_state.current_page == "signup" and not st.session_state.logged_in:
    st.title("Sign Up Page")
    new_username = st.text_input("Choose Username")
    new_password = st.text_input("Choose Password", type="password")

    if st.button("Create Account"):
        if signup(new_username, new_password):
            st.success("Account created successfully! Please login now.")
            st.session_state.current_page = "login"
            st.experimental_rerun()
        else:
            st.error("Username already exists!")

    if st.button("Back to Login"):
        st.session_state.current_page = "login"
        st.experimental_rerun()

elif st.session_state.current_page == "forgot" and not st.session_state.logged_in:
    st.title("Forgot Password Page")
    reset_username = st.text_input("Enter your Username")
    reset_password = st.text_input("Enter New Password", type="password")

    if st.button("Reset Password"):
        if forgot_password(reset_username, reset_password):
            st.success("Password Reset successful! Please login.")
            st.session_state.current_page = "login"
            st.experimental_rerun()
        else:
            st.error("Username not found!")

    if st.button("Back to Login"):
        st.session_state.current_page = "login"
        st.experimental_rerun()

elif st.session_state.logged_in:
    st.title(f"🎬 Welcome {st.session_state.username} to Movie Recommender System 🍿")

    movie_list = movies['title'].values
    selected_movie = st.selectbox("Type or select a movie", movie_list)

    if st.button('Show Recommendations'):
        with st.spinner('Fetching Recommendations...'):
            recommended_movie_names, recommended_movie_posters = recommend(selected_movie)

            cols = st.columns(5)
            for idx in range(5):
                with cols[idx]:
                    st.image(recommended_movie_posters[idx], width=150)
                    st.caption(recommended_movie_names[idx])
else:
    st.warning("Please login first!")

