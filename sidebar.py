from functions import *
from login import logout

def sidebar():
    st.logo("images/logo.svg", size="large", icon_image="images/logo.svg")

    st.sidebar.write(f"**Logget ind som:** {st.session_state['user']['email']}")

    if st.sidebar.button("Log ud"):
        logout()