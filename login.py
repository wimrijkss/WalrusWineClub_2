import streamlit as st
import firebase_admin
from firebase_admin import credentials, auth
import json

# Load Firebase credentials from Streamlit secrets
if "firebase" not in st.session_state:
    firebase_json = st.secrets["firebase"]["service_account"]
    firebase_cred = json.loads(firebase_json)
    cred = credentials.Certificate(firebase_cred)

    if not firebase_admin._apps:
        firebase_admin.initialize_app(cred)

def is_authenticated():
    """Check if a user is logged in (session-based persistence)."""
    return "user" in st.session_state

def login():
    """Login Form UI"""
    st.title("Log ind")
    st.subheader("Velkommen til Walrus Wine Club")

    email = st.text_input("Email", key="login_email")
    password = st.text_input("Password", type="password", key="login_password")

    if st.button("Log ind", key="login_button"):
        if not email or not password:
            st.error("Email and password are required.")
            return

        try:
            # Authenticate with Firebase Admin SDK
            user = auth.get_user_by_email(email)

            user_info = {
                "uid": user.uid,
                "email": user.email
            }

            # Store login info in session state
            st.session_state["user"] = user_info
            st.success(f"Login successful! Welcome, {user.email}")
            st.rerun()
        except Exception as e:
            st.error(f"Login failed: {e}")

def logout():
    """Log the user out"""
    if "user" in st.session_state:
        del st.session_state["user"]  # Remove from session
    st.success("Logged out successfully!")
    st.rerun()
