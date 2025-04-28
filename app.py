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
    if poster_path:
        full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
        return full_path, rating
    else:
        return "https://via.placeholder.com/500x750?text=No+Image", rating

def recommend(movie):
    available_movies = movies[movies['title'] != movie]
    recommended_movies = available_movies.sample(5)
    recommended_movie_names = []
    recommended_movie_posters = []
    recommended_movie_ratings = []
    for idx, row in recommended_movies.iterrows():
        movie_id = row['movie_id']
        poster, rating = fetch_poster(movie_id)
        recommended_movie_names.append(row['title'])
        recommended_movie_posters.append(poster)
        recommended_movie_ratings.append(rating)
    return recommended_movie_names, recommended_movie_posters, recommended_movie_ratings

def random_recommend():
    random_movies = movies.sample(5)
    random_movie_names = []
    random_movie_posters = []
    random_movie_ratings = []
    for idx, row in random_movies.iterrows():
        movie_id = row['movie_id']
        poster, rating = fetch_poster(movie_id)
        random_movie_names.append(row['title'])
        random_movie_posters.append(poster)
        random_movie_ratings.append(rating)
    return random_movie_names, random_movie_posters, random_movie_ratings

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
if not st.session_state.logged_in:
    # Apply dark theme background for login page
    st.markdown("""
        <style>
            .stApp {
                background-image: url('https://images.unsplash.com/photo-1526401485004-2a8c24b705f0?ixlib=rb-4.0.3&auto=format&fit=crop&w=1950&q=80');
                background-size: cover;
                background-repeat: no-repeat;
                background-attachment: fixed;
                background-position: center;
                color: white;
            }
            .login-container {
                background-color: rgba(0, 0, 0, 0.7);
                padding: 40px 30px;
                border-radius: 15px;
                max-width: 400px;
                margin: 0 auto;
                margin-top: 10%;
                box-shadow: 0px 0px 10px 2px rgba(255, 255, 255, 0.2);
            }
            input {
                background-color: #222 !important;
                color: white !important;
            }
            label {
                font-size: 18px !important;
                margin-bottom: 5px;
            }
            button {
                width: 100%;
            }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<h2 style='text-align: center; color: white;'>Login to Movie Recommender 🎬</h2>", unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        with st.form(key="login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submit_button = st.form_submit_button(label="Login")
        st.markdown('</div>', unsafe_allow_html=True)

    if submit_button:
        if login(username, password):
            st.success("Login Successful ✅")
            st.session_state.logged_in = True
            st.session_state.username = username
            st.experimental_rerun()
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

    cols_action = st.columns(2)
    with cols_action[0]:
        if st.button('Show Recommendation 🎯'):
            with st.spinner('Fetching recommendations... 🎥'):
                recommended_movie_names, recommended_movie_posters, recommended_movie_ratings = recommend(selected_movie)

            st.markdown("### Recommended Movies:")
            cols = st.columns(5)
            for idx, col in enumerate(cols):
                with col:
                    st.image(recommended_movie_posters[idx], use_container_width=True, caption="")
                    st.markdown(f"<div class='movie-title'>{recommended_movie_names[idx]}</div>", unsafe_allow_html=True)
                    st.markdown(f"<div class='rating'>⭐ {recommended_movie_ratings[idx]}</div>", unsafe_allow_html=True)

    with cols_action[1]:
        if st.button('Surprise Me! 🎲'):
            with st.spinner('Fetching random picks... 🎥'):
                random_movie_names, random_movie_posters, random_movie_ratings = random_recommend()

            st.markdown("### Random Movie Picks:")
            cols = st.columns(5)
            for idx, col in enumerate(cols):
                with col:
                    st.image(random_movie_posters[idx], use_container_width=True, caption="")
                    st.markdown(f"<div class='movie-title'>{random_movie_names[idx]}</div>", unsafe_allow_html=True)
                    st.markdown(f"<div class='rating'>⭐ {random_movie_ratings[idx]}</div>", unsafe_allow_html=True)
