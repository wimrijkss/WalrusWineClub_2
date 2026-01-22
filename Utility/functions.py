import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import pandas as pd
import numpy as np
from PIL import Image, ImageOps
import requests
from io import BytesIO
from datetime import datetime
import altair as alt
import pytz
import plotly.express as px  # Example usage for plotly

def initialize_firebase():
    try:
        if not firebase_admin._apps:  # Check if Firebase is already initialized
            # cred = credentials.Certificate("serviceAccountKey.json")
            cred = st.secrets["firebase"]["service_account"]
            firebase_admin.initialize_app(cred)  # No name provided → uses default
    except Exception as e:
        st.write(f"Error initializing Firebase app: {e}")
        return False
    return True


def get_firestore_client():
    try:
        return firestore.client()  # Use default app
    except Exception as e:
        st.write(f"Error accessing Firestore client: {e}")
        return None

# CSS
def customeCss():
    with open("style.css", "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Image cropping
@st.cache_resource 
def load_image_from_url(image_url):
    response = requests.get(image_url)
    image = Image.open(BytesIO(response.content))
    image = ImageOps.exif_transpose(image)
    return image

def imgCrop(wine_url):
    image = load_image_from_url(wine_url)

    width, height = image.size
    new_size = min(width, height)

    left = (width - new_size) / 2
    top = (height - new_size) / 2
    right = (width + new_size) / 2
    bottom = (height + new_size) / 2
    image_cropped = image.crop((left, top, right, bottom))
    return image_cropped
    # st.image(wine_url, use_container_width=True)



def get_current_timestamp():
    """Returns the current timestamp in 'Month Day, Year at HH:MM:SS AM/PM UTC±X' format."""
    # Set your timezone (Example: 'Europe/Copenhagen' for UTC+2)
    tz = pytz.timezone('Europe/Copenhagen')
    
    # Get current time in the specified timezone
    now = datetime.now(tz)
    
    # Format the timestamp
    formatted_timestamp = now.strftime("%B %d, %Y at %I:%M:%S %p %Z%z")
    
    return formatted_timestamp

def get_db_initialized():
    firebase_initialized = initialize_firebase()
    db = get_firestore_client() if firebase_initialized else None
    return db

def get_collection(collection):
    db = get_db_initialized()
    if db is not None:

        collection_ref = db.collection(collection)
        docs = collection_ref.stream()
        data = []
        for doc in docs:
            doc_dict = doc.to_dict()
            doc_dict['id'] = doc.id
            data.append(doc_dict)
            
        return data
    else:
        return st.write("Firestore client is not available. Please check initialization.")

