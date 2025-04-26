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
# Load data
# ---------------------------------

movies = pickle.load(open('model/movie_dict.pkl', 'rb'))

# ---------------------------------
# Login System
# ---------------------------------

# Simple hardcoded username-password (you can expand later)
USER_CREDENTIALS = {
    "admin": "1234",
    "user": "password"
}

def login(username, password):
    return USER_CREDENTIALS.get(username) == password

# Session state to keep track of login
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# ---------------------------------
# Streamlit App
# ---------------------------------

if not st.session_state.logged_in:
    st.title("Login to Movie Recommender 🎬")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if login(username, password):
            st.success("Login Successful ✅")
            st.session_state.logged_in = True
        else:
            st.error("Invalid Credentials ❌")
else:
    st.title('Movie Recommender System 🍿')

    movie_list = movies['title'].values
    selected_movie = st.selectbox(
        "Type or select a movie from the dropdown",
        movie_list
    )

    if st.button('Show Recommendation'):
        recommended_movie_names, recommended_movie_posters = recommend(selected_movie)

        cols = st.columns(5)
        for idx, col in enumerate(cols):
            with col:
                st.text(recommended_movie_names[idx])
                st.image(recommended_movie_posters[idx], use_column_width=True)

    if st.button('Logout'):
        st.session_state.logged_in = False
        st.experimental_rerun()
