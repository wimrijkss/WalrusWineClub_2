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

    # Page
    # -------------------- Fetch Data --------------------

    if db:
        # Fetch data
        collection_ref = db.collection('wines')
        docs = collection_ref.stream()
        data = [doc.to_dict() | {"id": doc.id} for doc in docs]
        df = pd.DataFrame(data)

        st.header("Charts")
        
        chart_df = df[["year", "type", "ratingAvg", "country", "grape"]]

        chart_df["ratingAvg"] = pd.to_numeric(chart_df["ratingAvg"], errors="coerce")

        chart_df["year"] = chart_df["year"].replace("N/V", np.nan)
        chart_df["year"] = pd.to_numeric(chart_df["year"], errors="coerce")
        chart_df = chart_df.dropna(subset=["year"])
        chart_df["year"] = chart_df["year"].astype(int)

        chart_df["country"] = chart_df["country"].replace({"Frankrig": "France"})

        df_grouped = chart_df.groupby("year")["ratingAvg"].mean().reset_index()
        df_grouped2 = chart_df.groupby("year").size().reset_index(name="count")
        
        st.bar_chart(df_grouped, x="year", y="ratingAvg", use_container_width=True)
        st.bar_chart(df_grouped2, x="year", y="count", use_container_width=True)
        st.bar_chart(chart_df, x="year", y="ratingAvg", color="country", horizontal=False)
        # st.bar_chart(chart_df.set_index(), x="grape", y="ratingAvg", horizontal=False)
        # st.bar_chart(chart_df.set_index('grape')['ratingAvg'])

        avg_ratings = chart_df.groupby('grape', as_index=False)['ratingAvg'].mean()

        # Sort the DataFrame by average rating (descending order)
        avg_ratings = avg_ratings.sort_values('ratingAvg', ascending=False)
        st.bar_chart(avg_ratings.set_index('grape'), horizontal=True)


        avg_ratings = avg_ratings.sort_values('ratingAvg', ascending=True)
        fig = px.bar(avg_ratings, x='ratingAvg', y='grape', title="Gennemsnitlig rating per drue",
                    labels={'ratingAvg': '', 'grape': ''}, hover_data={'ratingAvg': True})
        fig.update_layout(
            xaxis_tickangle=45,  # Rotate x-axis labels by 45 degrees to make them readable
            xaxis_tickmode='array',  # Ensure the tick labels do not overlap
        )
        st.plotly_chart(fig)


        avg_ratings = chart_df.groupby('year', as_index=False)['ratingAvg'].mean()

        # Sort the DataFrame by average rating (descending order)
        avg_ratings = avg_ratings.sort_values('year', ascending=False)

        avg_ratings = avg_ratings.sort_values('year', ascending=True)
        fig = px.bar(avg_ratings, x='year', y='ratingAvg', title="Gennemsnitlig rating per år",
                    labels={'year': '', 'grape': ''}, hover_data={'year': True})
        fig.update_layout(
            xaxis_tickangle=45,  # Rotate x-axis labels by 45 degrees to make them readable
            xaxis_tickmode='array',  # Ensure the tick labels do not overlap
        )
        st.plotly_chart(fig)




    else:
        st.write("Firestore client is not available. Please check initialization.")