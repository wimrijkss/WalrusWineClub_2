from functions import * 
from login import login, logout, is_authenticated
from firebase_admin import storage, firestore
import io

# Login Module
if not is_authenticated():
    login()  
else:
    st.sidebar.write(f"**Logged in as:** {st.session_state['user']['email']}")
    if st.sidebar.button("Logout"):
        logout()

    customeCss()
    firebase_initialized = initialize_firebase()
    db = get_firestore_client() if firebase_initialized else None

    if firebase_initialized:
        # Streamlit form to add wine data
        with st.form("wine_form"):
            name = st.text_input("Name", "Kamptal")
            winery = st.text_input("Winery", "Domæne Gobelsburg")
            country = st.text_input("Country", "Austria")
            region = st.text_input("Region", "Niederösterreich")
            grape = st.text_input("Grape", "Riesling")
            year = st.text_input("Year", "2023")
            type_ = st.selectbox("Type", ["Red", "White", "Rosé", "Sparkling"], index=1)
            season = st.text_input("Season", "3")
            alc_per = st.text_input("Alcohol Percentage", "12.5")

            rating_avg = st.text_input("Rating Average", "4.2")
            rating_size = st.number_input("Number of Ratings", min_value=1, step=1, value=3)
            drinkability_avg = st.text_input("Drinkability Avg", "4.5")
            drysweet_avg = st.text_input("Dry/Sweet Avg", "2.3")
            fruitiness_avg = st.text_input("Fruitiness Avg", "2.0")

            # Image uploader
            uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])
            who = st.session_state['user']['email']

            submitted = st.form_submit_button("Add Wine")

            if submitted:
                # Prepare wine data to be added
                wine_data = {
                    "name": name,
                    "winery": winery,
                    "country": country,
                    "region": region,
                    "grape": grape,
                    "year": year,
                    "type": type_,
                    "season": season,
                    "alcPer": alc_per,
                    "ratingAvg": rating_avg,
                    "ratingSize": rating_size,
                    "drinkabilityAvg": drinkability_avg,
                    "drysweetAvg": drysweet_avg,
                    "fruitinessAvg": fruitiness_avg,
                    "who": who,
                    "createdAt": firestore.SERVER_TIMESTAMP  # Firebase timestamp
                }

                # Add wine data to Firestore
                try:
                    wine_doc_ref = db.collection("wines").add(wine_data)  # Add wine data to Firestore
                    wine_doc_id = wine_doc_ref[1].id  # Get the document ID

                    st.success(f"Wine '{name}' added successfully! 🍷")

                    # Now handle the image upload if file is uploaded
                    if uploaded_file is not None:
                        # Convert the uploaded file to a byte stream
                        byte_data = uploaded_file.read()

                        # Initialize Firebase Storage
                        bucket = storage.bucket('wineclub-12231.appspot.com')  # Specify your bucket
                        blob = bucket.blob(f'images/{wine_doc_id}.jpg')  # Save using the wine document ID as the name

                        # Upload the byte data to Firebase Storage
                        blob.upload_from_file(io.BytesIO(byte_data), content_type=uploaded_file.type)

                        # Get the public URL of the uploaded image
                        image_url = blob.public_url
                        st.success(f"Image uploaded successfully! URL: {image_url}")

                        # Update the wine document with the image URL
                        db.collection("wines").document(wine_doc_id).update({"url": image_url})
                        st.success(f"Wine document updated with image URL.")
                    else:
                        st.error("Please upload an image for the wine.")
                except Exception as e:
                    st.error(f"Error adding wine: {e}")
    else:
        st.write("Firestore client is not available. Please check initialization.")

# "https://firebasestorage.googleapis.com/v0/b/wineclub-12231.appspot.com/o/1NTZoNyMd7KkQGaS4sKx?alt=media&token=20375944-bae6-4240-adc1-84e6dcfba8b7"
# "https://storage.googleapis.com/wineclub-12231.appspot.com/images/JB6uosNrzruWkZ3XlT4H.jpg"

# This XML file does not appear to have any style information associated with it. The document tree is shown below.
# <Error>
# <Code>AccessDenied</Code>
# <Message>Access denied.</Message>
# <Details>Anonymous caller does not have storage.objects.get access to the Google Cloud Storage object. Permission 'storage.objects.get' denied on resource (or it may not exist).</Details>
# </Error>