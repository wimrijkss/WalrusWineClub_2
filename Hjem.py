from functions import *
from login import login, logout, is_authenticated
from wine_details import see_details
from rate_wine import rateWine, get_collection
from sidebar import sidebar

# Login Module
if not is_authenticated():
    login()  

else:
    sidebar()
    customeCss()

    # Page
    st.title("Walrus Wine Club   Beta 2.1")

    df = pd.DataFrame(get_collection("wines"))
    
    st.header("Vine")
    col1, col2, col3 = st.columns(3)
    
    # Sorting wines
    sort_options = {
        "Navn (A-Z)": ("name", True),
        "Navn (Z-A)": ("name", False),
        "Årgang (Nyest først)": ("year", False),
        "Årgang (Ældst først)": ("year", True),
        "Rating gennemsnitligt (Høj til Lav)": ("ratingAvg", False),
        "Rating gennemsnitligt (Lav til Høj)": ("ratingAvg", True),
    }

    distinct_grapes = ['Alle'] + sorted(list(df['grape'].unique()))
    distinct_types = ['Alle'] + sorted(list(df['type'].unique()))
    
    with col1:
        selected_item = st.selectbox("Vælg en druesort", distinct_grapes)
    with col2:
        selected_type = st.selectbox("Vælg en vintype", distinct_types)

    # Filter by selected grape type
    if selected_item != 'Alle':
        df = df[df['grape'] == selected_item]

    if selected_type != 'Alle':
        df = df[df['type'] == selected_type]


    # Sort wines
    with col3:
        sort_choice = st.selectbox("Sortér efter:", list(sort_options.keys()))
    
    sort_column, sort_ascending = sort_options[sort_choice]
    df = df.sort_values(by=sort_column, ascending=sort_ascending)
    st.dataframe(df)
    # Columns
    num_cols = 2
    rows = [df.iloc[i:i+num_cols] for i in range(0, len(df), num_cols)] 

    progress_bar = st.progress(0)
    
    total_images = len(df)
    current_image = 0

    for row in rows:
        cols = st.columns(num_cols) 

        for col, (_, wine) in zip(cols, row.iterrows()):
            with col:
                with st.container(border=True):
                    img_col, text_col = st.columns([1, 2])  

                    with img_col:
                        st.image(wine["url"], use_container_width=True) #Faster but not cropped
                        # st.image(imgCrop(wine["url"]), use_container_width=True)
                        current_image += 1
                        progress_bar.progress(current_image / total_images)
                        if current_image / total_images == 1:
                            progress_bar.empty()
                        if st.button("Se info", key=wine["url"]):
                            see_details(wine)
                        if st.button("Rate wine", key=f'{wine["url"]}+2'):
                            rateWine(wine)

                    with text_col:
                        st.html(
                            f"<div class='card'>"
                            f"<h1>{wine['name']}</h1>"
                            f"<h3>{wine['year']}</h3>"
                            f"<p>{wine['winery']}</p>"
                            f"<p>{wine['grape']}</p>"
                            f"<p>{wine['type']}</p>"
                            f"<p>Average rating<p>"
                            f"<div class='card-rating'>"
                                f"<p class='ratingAvg'>{wine['ratingAvg']}</p>"
                                f"<p>{wine['ratingSize']} ratings</p>"
                                f"<p>{wine['type']}</p>"
                            f"</div>"
                            f"</div>"
                        )
                        # st.metric(label="Average rating", value=f"{wine['ratingAvg']}")
                        # st.write(f"{wine['ratingSize']} ratings")
