import time  # to simulate a real time data, time loop

import numpy as np  # np mean, np random
import pandas as pd  # read csv, df manipulation
import plotly.express as px  # interactive charts
import streamlit as st  # 🎈 data web app development
from streamlit_lottie import st_lottie

import pandas as pd
import json
import glob
import matplotlib.pyplot as plt
from utils import create_df

# set up dashboard page
st.set_page_config(
    page_title="Facebook Messages Wrapped",
    page_icon="✅",
)

#######################################
# get data from uploaded files

placeholder = st.empty()

with placeholder.container():
    uploaded_files = st.file_uploader("Choose the messages file(s)", accept_multiple_files=True, type=['json'])
    if uploaded_files is not None:
        df, participants = create_df(uploaded_files)

        # calculate fun values
        frst_date = df.sort_values(by='date').iloc[0].date
        last_date = df.sort_values(by='date').iloc[-1].date
        no_messages = len(df)
        most_active = df.groupby(by='sender_name').count().sort_values(by='content',ascending=False).reset_index().iloc[0].sender_name
        most_active_no_messages = df.groupby(by='sender_name').count().sort_values(by='content',ascending=False).reset_index().iloc[0].content
        least_active = df.groupby(by='sender_name').count().sort_values(by='content',ascending=False).reset_index().iloc[-1].sender_name
        most_pictures = df.groupby(by='sender_name').count().sort_values(by='photos',ascending=False).reset_index().iloc[0].sender_name
        most_gifs = df.groupby(by='sender_name').count().sort_values(by='gifs',ascending=False).reset_index().iloc[0].sender_name


placeholder.empty()
time.sleep(2)

###################################
# get fun animations
path = "animation_lnmxxffi.json"
with open(path,"r") as file: 
    animation_messages = json.load(file)


####################################
# create the facebook messages wrapped!

placeholder = st.empty()

with placeholder.container():
    st.title(f'Since {frst_date} there has been communication between...')
    # set header
    for participant in participants:
        time.sleep(1.1)
        st.header(participant)

    time.sleep(1.5)

    clicked = st.button('Click me')

if clicked:
    # clear whole page
    placeholder.empty()

    st.session_state.clicked = False

    # create new placeholder
    placeholder = st.empty()

    with placeholder.container():
        st_lottie(animation_messages, 
            reverse=True, 
            height=250, 
            width=250, 
            speed=1, 
            loop=True, 
            quality='high', 
            key='messages'
        )

        st.title(f'In these {(last_date-frst_date).days} days, you have been writing {no_messages} messages to each other.')

        time.sleep(1.5)
        # set header
        st.header('Wow! :open_mouth:')

        time.sleep(1.5)

# clear whole page
placeholder.empty()

st.session_state.clicked = False
# create new placeholder
placeholder = st.empty()
with placeholder.container():
    st.header('The most activate person was...')
    time.sleep(1.5)
    st.title(most_active)
    st.balloons()
    time.sleep(0.8)
    st.header(f'making contact a total of {most_active_no_messages} times')


# show dataframe

#st.markdown("### Dataframe")
#st.dataframe(df)
