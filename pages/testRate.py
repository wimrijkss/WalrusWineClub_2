from functions import * 
from login import login, logout, is_authenticated
import plotly.express as px

# Login Module
if not is_authenticated():
    login()  

else:
        
    st.sidebar.write(f"**Logget ind som:** {st.session_state['user']['email']}")    
    if st.sidebar.button("Log ud"):
        logout()

    customeCss()
    firebase_initialized = initialize_firebase()
    db = get_firestore_client() if firebase_initialized else None

    # Set page config
    # st.set_page_config(page_title="MyFinances Dashboard", layout="wide")

    # Custom CSS for styling
    st.markdown(
        """
        <style>
            .css-18e3th9 {
                background-color: #F8F9FD;
            }
            .main-title {
                font-size: 24px;
                font-weight: bold;
                color: #333;
            }
            .profile-card {
                background: white;
                margin: 20px;
                padding: 20px;
                border-radius: 10px;
                text-align: center;
                box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
            }
            .balance-card {
                background: var(--main-color);
                color: white;
                padding: 15px;
                border-radius: 10px;
                text-align: center;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Sidebar menu



    # Dashboard layout
    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown('<div class="main-title">Overview</div>', unsafe_allow_html=True)
        
        # Sample data for bar chart
        df = pd.DataFrame({
            "Month": ["January", "February", "March", "April", "May", "June"],
            "Income": [3000, 4500, 5000, 5200, 6000, 7500],
            "Expenses": [2500, 4000, 4600, 4700, 5100, 6900]
        })
        
        fig = px.bar(df, x="Month", y=["Income", "Expenses"], barmode='group',
                    title="Income vs Expenses", color_discrete_map={"Income": "#3b82f6", "Expenses": "#ff6384"})
        st.plotly_chart(fig, use_container_width=True)
        
        # Pie Chart
        pie_data = pd.DataFrame({
            "Category": ["Income", "Expenses"],
            "Value": [sum(df["Income"]), sum(df["Expenses"])]
        })
        fig_pie = px.pie(pie_data, names='Category', values='Value', title="Income vs Expenses Breakdown",
                        color_discrete_map={"Income": "#3b82f6", "Expenses": "#ff6384"})
        st.plotly_chart(fig_pie, use_container_width=True)

    with col2:
        # Profile Card

        users_df = pd.DataFrame(get_collection("users"))
        ratings_df = pd.DataFrame(get_collection("ratings"))
        wines_df = pd.DataFrame(get_collection("wines"))

        # Get current user details
        current_user = users_df[users_df["userID"] == st.session_state['user']['email']].iloc[0]
        current_user_name = current_user["firstName"]
        current_user_email = current_user["userID"]

        # Filter ratings for the current user
        user_ratings = ratings_df[ratings_df["userID"] == current_user_email]

        # Find the highest-rated wine for the user
        highest_rating = user_ratings['rating'].max()
        highest_rated_wine_id = user_ratings[user_ratings['rating'] == highest_rating]["wineID"].values[0]

        # Fetch the wine details based on the highest-rated wine ID
        highest_rated_wine = wines_df[wines_df["id"] == highest_rated_wine_id].iloc[0]

        # Display user and wine details
        st.markdown(
            f'<div class="balance-card">'
            f'<h2>{current_user_name}</h2>'
            f"<p>Yndingsdrue: {highest_rated_wine['grape']}</p>"
            f'</div>',
            unsafe_allow_html=True
        )
        
        # # Recent Transactions
        # st.markdown("### Recent Activities")
        # st.write("✔️ Car Insurance -$810.50 (Sent)")
        # st.write("✔️ From Linda Hamilton +$1,274.94 (Received)")
        # st.write("✔️ Apple Store -$3,215.50 (Sent)")
