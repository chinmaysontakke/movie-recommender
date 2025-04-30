import pickle
import streamlit as st
import requests

# 1) Page config first
st.set_page_config(page_title="Movie Recommender", page_icon="🍿", layout="wide")

# 2) Global CSS: background + login-box styling
st.markdown("""
<style>
/* Full-page cinematic background */
body {
  background-image: url("https://img.freepik.com/free-photo/3d-cinema-theatre-room-with-seating_23-2151005451.jpg");
  background-size: cover;
  background-position: center;
  background-attachment: fixed;
}

/* Semi-opaque overlay so text stands out */
.stApp > .main {
  background-color: rgba(0,0,0,0.6);
}

/* LOGIN CONTAINER */
.login-container {
  width: 950px;
  height: 960px;
  margin: 50px auto;               /* vertical space + center horizontally */
  padding: 40px;
  background: rgba(255,255,255,0.1);
  border-radius: 12px;
  display: flex;
  flex-direction: column;
  justify-content: center;         /* vertical centering */
  align-items: center;             /* horizontal centering */
}

/* HEADINGS & LABELS */
.login-container h2,
.login-container label {
  color: #fff !important;
  font-weight: bold !important;
  text-align: center !important;
}

/* INPUT FIELDS */
.login-container input {
  color: #fff !important;
  background-color: rgba(0,0,0,0.4) !important;
  border: 1px solid #777 !important;
  font-weight: bold !important;
}

/* PLACEHOLDERS */
.login-container input::placeholder {
  color: #ddd !important;
}

/* BUTTON */
.login-container .stButton > button {
  color: #fff !important;
  background-color: rgba(255,255,255,0.2) !important;
  border: 1px solid #fff !important;
  font-weight: bold !important;
  padding: 0.6em 2em !important;
}
</style>
""", unsafe_allow_html=True)

# 3) Login logic & UI
USER_CREDENTIALS = {"admin":"1234","user":"password"}
def login(u,p): return USER_CREDENTIALS.get(u)==p

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    # Wrap everything in a div.login-container
    st.markdown("<div class='login-container'>", unsafe_allow_html=True)
    st.markdown("<h2>Login to Movie Recommender 🎬</h2>", unsafe_allow_html=True)
    with st.form("login_form"):
        username = st.text_input("Username", placeholder="Enter your username")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        submit = st.form_submit_button("Login")
    if submit:
        if login(username, password):
            st.session_state.logged_in = True
            st.success("Login Successful ✅")
        else:
            st.error("Invalid Credentials ❌")
    st.markdown("</div>", unsafe_allow_html=True)

else:
    # …rest of your logged-in app…
    st.write(f"Welcome, **{st.session_state.username}**")
