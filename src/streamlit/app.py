import os
import sys
import yaml
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth
import streamlit as st

# @TODO: Only start auth on production, because it interferes with unittests.

credentials_filepath = "./credentials.yml"
with open(credentials_filepath, encoding="utf-8") as file:
    config = yaml.load(file, Loader=SafeLoader)


# Pre-hashing all plain text passwords once
stauth.Hasher.hash_passwords(config["credentials"])

authenticator = stauth.Authenticate(
    config["credentials"],
    config["cookie"]["name"],
    config["cookie"]["key"],
    config["cookie"]["expiry_days"],
    config["pre-authorized"],
)
authenticator.login()


if st.session_state["authentication_status"]:
    nav = st.navigation(
        [
            st.Page(
                "./menu/home.py",
                title="Home",
                icon=":material/dashboard:",
            ),
            st.Page(
                "./menu/page1.py",
                title="Page1",
                icon=":material/robot:",
            ),
        ]
    )

    # Only start auth on production
    authenticator.logout(location="sidebar")

    nav.run()
else:
    # Users only end up here if they are not authenticated and in prod.
    if st.session_state["authentication_status"] is False:
        st.error("Username/password is incorrect")
    elif st.session_state["authentication_status"] is None:
        st.warning("Please enter your username and password")
