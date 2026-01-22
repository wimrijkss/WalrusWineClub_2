from functions import *
from functions import get_collection

@st.dialog(" ", width="large")
def rateWine(wine):
    """Allows users to rate the wine and submits ratings to Firestore."""
    st.title(wine["name"])

    db = get_db_initialized()

    ratings = pd.DataFrame(get_collection("ratings"))

    currentRating = ratings[
        (ratings["wineID"] == wine["id"])  & 
        (ratings["userID"] == st.session_state["user"]["email"])
    ]
    
    # Rating sliders
    # user_rating = st.slider("Your Rating", 0.0, 5.0, 3.0, 0.1)
    # st.dataframe(currentRating)
    if not currentRating.empty:
        st.header("RatingID: " + currentRating["id"].values[0])
        st.header("WineID: " + currentRating["wineID"].values[0])
        # Ensure each rating is a scalar (not a list)
        rating_value = currentRating["rating"].values[0]
        drySweetRating_value = currentRating["drySweetRating"].values[0]
        drinkabilityRating_value = currentRating["drinkabilityRating"].values[0]
        fruitinessRating_value = currentRating["fruitinessRating"].values[0]
        
        # Display sliders with correct values
        rating = st.slider('Vurder vin:', min_value=0.0, max_value=5.0, value=float(rating_value), step=1.0)
        drySweetRating = st.slider('Dry / Sweet:', min_value=0.0, max_value=5.0, value=float(drySweetRating_value), step=1.0)
        drinkabilityRating = st.slider('Drinkability:', min_value=0.0, max_value=5.0, value=float(drinkabilityRating_value), step=1.0)
        fruitinessRating = st.slider('Frutiness:', min_value=0.0, max_value=5.0, value=float(fruitinessRating_value), step=1.0)
    else:
        st.header("Ikke vurderet endnu")
        # Default to zero when no rating is available
        rating = st.slider('Rate vin:', min_value=0.0, max_value=10.0, value=0.0, step=1.0)
        drySweetRating = st.slider('Dry / Sweet:', min_value=0.0, max_value=10.0, value=0.0, step=1.0)
        drinkabilityRating = st.slider('Drinkability:', min_value=0.0, max_value=10.0, value=0.0, step=1.0)
        fruitinessRating = st.slider('Frutiness:', min_value=0.0, max_value=10.0, value=0.0, step=1.0)

    if st.button("Send vurdering"):
        rating_data = {
            "wineID": wine["id"],
            "rating": rating,
            "userID": st.session_state["user"]["email"],
            "drySweetRating": drySweetRating,
            "drinkabilityRating": drinkabilityRating,
            "fruitinessRating": fruitinessRating,
            "ratedAt": get_current_timestamp()
        }
        try:
            db.collection("ratings").add(rating_data)
            st.success("Tak for at vurdere vinen! 🍷")
        except Exception as e:
            st.error(f"Error submitting rating: {e}")
