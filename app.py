import streamlit as st
import json
import os

# --- Initialize users database ---
if not os.path.exists("users.json"):
    with open("users.json", "w") as f:
        json.dump({}, f)

def load_users():
    with open("users.json", "r") as f:
        return json.load(f)

def save_users(users):
    with open("users.json", "w") as f:
        json.dump(users, f)

# --- Authentication Logic ---
def login(username, password):
    users = load_users()
    if username in users and users[username]["password"] == password:
        return True
    return False

def signup(username, password):
    users = load_users()
    if username in users:
        return False
    users[username] = {"password": password}
    save_users(users)
    return True

def reset_password(username, new_password):
    users = load_users()
    if username in users:
        users[username]["password"] = new_password
        save_users(users)
        return True
    return False

# --- Streamlit Page Setup ---
st.set_page_config(page_title="Movie Recommender", page_icon="🎬")

# --- Background Color ---
st.markdown("""
    <style>
    .stApp {
        background-color: #f0f2f6;
    }
    .top-right-buttons {
        position: absolute;
        top: 10px;
        right: 10px;
        display: flex;
        gap: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Session States ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "page" not in st.session_state:
    st.session_state.page = "login"

# --- Top Right Buttons ---
def top_buttons():
    st.markdown('<div class="top-right-buttons">', unsafe_allow_html=True)
    if st.session_state.logged_in:
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.session_state.page = "login"
    else:
        if st.button("Login"):
            st.session_state.page = "login"
        if st.button("Sign Up"):
            st.session_state.page = "signup"
    st.markdown('</div>', unsafe_allow_html=True)

top_buttons()

# --- Pages ---
def login_page():
    st.title("Login 🔐")
    username = st.text_input("Username", key="login_username")
    password = st.text_input("Password", type="password", key="login_password")

    if st.button("Login Now"):
        if login(username, password):
            st.success("Login successful! 🎉")
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.page = "home"
        else:
            st.error("Invalid username or password.")

    if st.button("Forgot Password?"):
        st.session_state.page = "forgot"

def signup_page():
    st.title("Sign Up 📝")
    username = st.text_input("New Username", key="signup_username")
    password = st.text_input("New Password", type="password", key="signup_password")
    confirm_password = st.text_input("Confirm Password", type="password", key="signup_confirm_password")

    if st.button("Sign Up Now"):
        if password != confirm_password:
            st.error("Passwords do not match.")
        elif signup(username, password):
            st.success("Account created successfully! Please login.")
            st.session_state.page = "login"
        else:
            st.error("Username already exists.")

def forgot_page():
    st.title("Forgot Password 🔑")
    username = st.text_input("Enter Username", key="forgot_username")
    new_password = st.text_input("New Password", type="password", key="forgot_password")
    confirm_password = st.text_input("Confirm New Password", type="password", key="forgot_confirm_password")

    if st.button("Reset Password"):
        if new_password != confirm_password:
            st.error("Passwords do not match.")
        elif reset_password(username, new_password):
            st.success("Password reset successful! Please login.")
            st.session_state.page = "login"
        else:
            st.error("Username does not exist.")

def home_page():
    st.title(f"Welcome, {st.session_state.username} 🎬")
    st.write("This is your Movie Recommender System 🚀.")
    # Your main app code (movie recommendations) can come here.
    st.success("Start exploring movies now!")

# --- Routing Based on Page ---
if st.session_state.page == "login":
    login_page()
elif st.session_state.page == "signup":
    signup_page()
elif st.session_state.page == "forgot":
    forgot_page()
elif st.session_state.page == "home" and st.session_state.logged_in:
    home_page()
else:
    st.session_state.page = "login"
