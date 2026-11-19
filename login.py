import streamlit as st

if "page" not in st.session_state:
    st.session_state.page = "login"

if "show_login" not in st.session_state:
    st.session_state.show_login = False

def go_to(page):
    st.session_state.page = page
    st.rerun()

def submit_name():
    name = st.session_state.name_input.strip()
    if name == "":
        st.session_state.name_warning = True
    else:
        st.session_state.name_warning = False
        st.session_state.user_name = name
        st.session_state.is_new_user = False
        st.session_state.page = "profile"

def create_account():
    name = st.session_state.signup_name.strip()
    if name == "":
        st.session_state.signup_warning = True
    else:
        st.session_state.signup_warning = False
        st.session_state.user_name = name
        st.session_state.is_new_user = True
        st.session_state.page = "profile"

def login_page():
    st.title("Prescription Pilot 💊")
    st.subheader("Login")

    if not st.session_state.show_login:
        if st.button("Log in"):
            st.session_state.show_login = True
            st.rerun()
    else:
        st.text_input("Enter First Name", key="name_input", on_change=submit_name)
        if st.session_state.get("name_warning"):
            st.warning("Please enter your first name :)")

    if st.button("Create Account"):
        st.session_state.is_new_user = True
        go_to("signup")

def profile_page():
    st.title("My Profile")
    if st.session_state.is_new_user:
        st.write(f"Welcome, {st.session_state.user_name}!")
    else:
        st.write(f"Welcome back, {st.session_state.user_name}!")

def signup_page():
    st.title("Create Account")

    st.text_input("Sign up with your first name", key = "signup_name", on_change = create_account)
    if st.session_state.get("signup_warning"):
        st.warning("Please enter your first name :)")

    if st.button("Back to login"):
        st.session_state.show_login = False
        go_to("login")

if st.session_state.page == "login":
    login_page()
elif st.session_state.page == "profile":
    profile_page()
elif st.session_state.page == "signup":
    signup_page()