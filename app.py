import streamlit as st
import pickle
import requests

# ---------------------------------
# Helper functions for movie fetching
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
# Load movie data
# ---------------------------------

try:
    movies = pickle.load(open('movies.pkl', 'rb'))
except Exception as e:
    st.error(f"Error loading movie data: {e}")
    st.stop()

# ---------------------------------
# Streamlit App Layout
# ---------------------------------

st.set_page_config(page_title="Movie Recommender", page_icon="🍿", layout="wide")

# Apply custom CSS for the login page design
st.markdown("""
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Roboto', sans-serif;
        }
        body {
            background: #000;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }
        body::before {
            content: "";
            position: absolute;
            left: 0;
            top: 0;
            opacity: 0.5;
            width: 100%;
            height: 100%;
            background: url("images/hero-img.jpg");
            background-position: center;
            background-size: cover;
        }
        nav {
            position: fixed;
            padding: 25px 60px;
            z-index: 1;
        }
        nav a img {
            width: 167px;
        }
        .form-wrapper {
            position: relative;
            border-radius: 12px;
            padding: 40px;
            width: 400px;
            background: rgba(0, 0, 0, 0.8);
            box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.5);
        }
        .form-wrapper h2 {
            color: #fff;
            font-size: 2rem;
            text-align: center;
            margin-bottom: 20px;
        }
        .form-wrapper form {
            margin: 20px 0;
        }
        form .form-control {
            height: 50px;
            position: relative;
            margin-bottom: 20px;
        }
        .form-control input {
            height: 100%;
            width: 100%;
            background: #333;
            border: none;
            outline: none;
            border-radius: 4px;
            color: #fff;
            font-size: 1rem;
            padding: 0 20px;
        }
        .form-control label {
            position: absolute;
            left: 20px;
            top: 50%;
            transform: translateY(-50%);
            font-size: 1rem;
            pointer-events: none;
            color: #8c8c8c;
            transition: all 0.1s ease;
        }
        .form-control input:is(:focus, :valid)~label {
            font-size: 0.75rem;
            transform: translateY(-130%);
        }
        form button {
            width: 100%;
            padding: 16px 0;
            font-size: 1rem;
            background: #e50914;
            color: #fff;
            font-weight: 500;
            border-radius: 4px;
            border: none;
            outline: none;
            margin: 25px 0;
            cursor: pointer;
            transition: 0.1s ease;
        }
        form button:hover {
            background: #c40812;
        }
        .form-wrapper p a {
            color: #fff;
        }
        .form-wrapper small {
            display: block;
            margin-top: 15px;
            color: #b3b3b3;
        }
        .form-wrapper small a {
            color: #0071eb;
        }
        @media (max-width: 740px) {
            .form-wrapper {
                width: 90%;
                top: 50%;
                transform: translateY(-50%);
            }
        }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------
# Login System Logic
# ---------------------------------

USER_CREDENTIALS = {
    "admin": "1234",
    "user": "password"
}

def login(username, password):
    return USER_CREDENTIALS.get(username) == password

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.markdown("<h2 style='text-align: center;'>Sign In</h2>", unsafe_allow_html=True)
    with st.form(key="login_form"):
        username = st.text_input("Email or phone number")
        password = st.text_input("Password", type="password")
        submit_button = st.form_submit_button(label="Sign In")

    if submit_button:
        if login(username, password):
            st.success("Login Successful ✅")
            st.session_state.logged_in = True
            st.session_state.username = username
        else:
            st.error("Invalid Credentials ❌")
else:
    # After successful login, show the movie recommender system
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

    # Logout Button
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = None
        st.experimental_rerun()

