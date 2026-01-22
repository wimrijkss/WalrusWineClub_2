from functions import *

# Function to display basic wine info
def display_basic_info(wine):
    st.markdown(f"""
        <div class="wine-details-header wine-card">
            <h2>{wine['name']} ({wine['year']})</h2>
            <div class="title-rating">
                <p>Gennemsnit</p>
                <p>{wine["ratingAvg"]} / 5.0</p>
            </div>
            <h3>Generel Information</h3>
            <div class="wine-card-info">
                <p><strong>Vingård</strong>: {wine['winery']}</p>
                <p><strong></strong>{wine['year']}</p>
                <p><strong>Region</strong>: {wine['region']}</p>
                <p><strong>Land</strong>: {wine['country']}</p>
                <p><strong>Type</strong>: {wine['type']}</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

# Function to display rating and characteristics of the wine
def display_characteristics(wine):
    data = {
        "Characteristic": ["Drinkability", "Sweetness", "Fruitiness"],
        # "Characteristic": ["Average Rating", "Drinkability", "Sweetness", "Fruitiness"],
        "Score": [
                # float(wine["ratingAvg"]), 
                float(wine["drinkabilityAvg"]), 
                float(wine["drysweetAvg"]), 
                float(wine["fruitinessAvg"])
            ]
    }
        
    df = pd.DataFrame(data)

    # Create Horizontal Bar Chart using Altair
    chart = alt.Chart(df).mark_bar(color="#2CB577").encode(
        x=alt.X("Score:Q"),
        y=alt.Y("Characteristic:N", sort="-x"),
        tooltip=["Characteristic", "Score"]
    ).properties(
        width=700,  # Adjust width
        height=250  # Adjust height
    )

    # Display header and chart
    st.markdown("<div class='wine-card'><h3>Vinens egenskaber</h3></div>", unsafe_allow_html=True)
    st.altair_chart(chart, use_container_width=True)

# Function to display grape and alcohol info
def display_grape_info(wine):
    st.markdown(f"""
        <div class="wine-grape-info wine-card">
            <h3>Druer & Alkohol</h3>
            <div class="wine-card-info">
                <p><strong>Druesorter</strong>: {wine['grape']}</p>
                <p><strong>Alkoholprocent</strong>: {wine['alcPer']}%</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

# Function to display the wine image
def display_wine_image(wine):
    st.markdown(f"""
        <div class="wine-image">
            <img src="{wine['url']}" alt="{wine['name']} - {wine['year']}"/>
        </div>
    """, unsafe_allow_html=True)

# Function to display additional information about the wine
def display_additional_info(wine):
    st.markdown(f"""
        <div class="wine-additional-info wine-card">
            <h3>Ekstra Information</h3>
            <div class="wine-card-info">
                <p><strong>Sæson</strong>: {wine['season']}</p>
                <p><strong>Antal ratings</strong>: {wine['ratingSize']} ratings</p>
                <p><strong>Indkrevet den</strong>: {format_timestamp(wine['createdAt'])}</p>
                <p><strong>Indskrevet af</strong>: {wine['who']}</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

# Helper function to format the timestamp
def format_timestamp(timestamp):
    if isinstance(timestamp, str):
        timestamp = datetime.strptime(timestamp, "%b %d, %Y at %I:%M:%S %p UTC%z")
    # If it's already a datetime object, no need to use strptime
    return timestamp.strftime("%B %d, %Y, %H:%M:%S")

# Main function to showcase the wine data
def display_wine(wine):
    col1, col3 = st.columns([2,3])
    with col1:
        display_wine_image(wine)
    with col3:
        # Display content using custom HTML structure
        display_basic_info(wine)
        display_characteristics(wine)
        display_grape_info(wine)
        display_additional_info(wine)

@st.dialog(" ", width="large")
def see_details(wine):
    display_wine(wine)




# Show the wine details