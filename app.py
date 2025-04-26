import streamlit as st
import json
import os

# ====== Setup Users Database ======
if not os.path.exists("users.json"):
    with open("users.json", "w") as f:
        json.dump({}, f)

def load_users():
    with open("users.json", "r") as f:
        return json.load(f)

def save_users(users):
    with open("users.json", "w") as f:
        json.dump(users, f)

# ====== Authentication Functions ======
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

# ====== Styling ======
st.markdown(
    """
    <style>
        .top-right-buttons {
            position: absolute;
            top: 10px;
            right: 10px;
            display: flex;
            gap: 10px;
        }
        .stApp {
            background-color: #f0f2f6;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# ====== Session State ======
if "page" not in st.session_state:
    st.session_state.page = "login"
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

# ====== Top Right Buttons ======
def top_right_buttons():
    with st.container():
        st.markdown('<div class="top-right-buttons">', unsafe_allow_html=True)
        if st.session_state.logged_in:
            if st.button("Logout"):
                st.session_state.logged_in = False
                st.session_state.page = "login"
        else:
            if st.button("Login"):
                st.session_state.page = "login"
            if st.button("Sign Up"):
                st.session_state.page = "signup"
        st.markdown('</div>', unsafe_allow_html=True)

top_right_buttons()

# ====== Pages ======

# Login Page
def login_page():
    st.subheader("Login 🔐")
    username = st.text_input("Username", key="login_user")
    password = st.text_input("Password", type="password", key="login_pass")

    if st.button("Login Now"):
        if login(username, password):
            st.success(f"Welcome {username} 🎉")
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.page = "home"
        else:
            st.error("Invalid username or password")

    if st.button("Forgot Password?"):
        st.session_state.page = "forgot"

# Sign Up Page
def signup_page():
    st.subheader("Create Account 📝")
    username = st.text_input("Choose a Username", key="signup_user")
    password = st.text_input("Choose a Password", type="password", key="signup_pass")
    confirm_password = st.text_input("Confirm Password", type="password", key="signup_conf_pass")

    if st.button("Create Account"):
        if password != confirm_password:
            st.error("Passwords do not match.")
        elif signup(username, password):
            st.success("Account created successfully! Please login.")
            # Wait briefly then switch page
            st.session_state.page = "login"
            st.experimental_set_query_params(page="login")   # Silent switch (no rerun)
        else:
            st.error("Username already exists. Please try a different one.")

# Forgot Password Page
def forgot_page():
    st.subheader("Reset Password 🔑")
    username = st.text_input("Enter your Username", key="forgot_user")
    new_password = st.text_input("Enter New Password", type="password", key="forgot_new_pass")
    confirm_password = st.text_input("Confirm New Password", type="password", key="forgot_conf_pass")

    if st.button("Reset Password"):
        if new_password != confirm_password:
            st.error("Passwords do not match.")
        elif reset_password(username, new_password):
            st.success("Password reset successfully! Please login.")
            st.session_state.page = "login"
        else:
            st.error("Username not found.")

# Home (after Login)
def home_page():
    st.title(f"Welcome, {st.session_state.username} 🎬")
    st.write("This is your Movie Recommender System. 🚀")
    # Put your main movie recommender UI here
    st.success("Enjoy Your Movie Journey!")

# ====== Routing ======
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
