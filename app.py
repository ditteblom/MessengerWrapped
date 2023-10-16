import time  # to simulate a real time data, time loop

import numpy as np  # np mean, np random
import pandas as pd  # read csv, df manipulation
import plotly.express as px  # interactive charts
import streamlit as st  # 🎈 data web app development
from streamlit_lottie import st_lottie
from PIL import Image
import os

import pandas as pd
import openai
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
    path_from_user = st.text_input('Please input path to directory for the chat.')

if path_from_user:
    placeholder.empty()

    df, participants = create_df(path_from_user)

    frst_date = df.sort_values(by='date').iloc[0].date
    last_date = df.sort_values(by='date').iloc[-1].date
    no_messages = len(df)
    most_active = df.groupby(by='sender_name').count().sort_values(by='content',ascending=False).reset_index().iloc[0].sender_name
    most_active_no_messages = df.groupby(by='sender_name').count().sort_values(by='content',ascending=False).reset_index().iloc[0].content
    least_active = df.groupby(by='sender_name').count().sort_values(by='content',ascending=False).reset_index().iloc[-1].sender_name
    least_active_no_messages = df.groupby(by='sender_name').count().sort_values(by='content',ascending=False).reset_index().iloc[-1].content
    most_pictures = df.groupby(by='sender_name').count().sort_values(by='photos',ascending=False).reset_index().iloc[0].sender_name
    most_gifs = df.groupby(by='sender_name').count().sort_values(by='gifs',ascending=False).reset_index().iloc[0].sender_name

time.sleep(2)

###################################
# get fun animations
path = "animation_lnmxxffi.json"
with open(path,"r") as file: 
    animation_messages = json.load(file)

path = "sad_animation.json"
with open(path,"r") as file: 
    sad_animation = json.load(file)


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


# clear whole page
placeholder.empty()

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

    time.sleep(1.2)

    st.title(f'In these {(last_date-frst_date).days} days, you have been writing {no_messages} messages to each other.')

    time.sleep(1.8)
    # set header
    st.header('Wow! :open_mouth:')

    time.sleep(3.9)

# clear whole page
placeholder.empty()

# create new placeholder
placeholder = st.empty()
with placeholder.container():
    st.header('The most activate person was...')
    time.sleep(2.1)
    st.title(most_active)
    st.balloons()
    time.sleep(2.1)
    st.header(f'making contact a total of {most_active_no_messages} times!')
    time.sleep(4.5)

# clear whole page
placeholder.empty()

# create new placeholder
placeholder = st.empty()
with placeholder.container():
    st.header(f'The coldest person only making contact {least_active_no_messages} times was...')
    time.sleep(2.1)
    st.title(least_active)
    st.snow()
    time.sleep(2.1)
    st.header(f':cold_face:')
    time.sleep(4.5)

placeholder.empty()

# create new placeholder
placeholder1 = st.empty()
placeholder2 = st.empty()

# show sad messages
df_sad = df[(df['type_reactions'].str.contains('crying', regex=True)) & (df['no_reactions'] > 3)]
idx_sad = df_sad[df_sad.no_reactions > 3].index.to_list()
if len(idx_sad) > 5:
    no_sad = 5
else:
    no_sad = len(idx_sad)
idx_sad_disp = np.random.choice(idx_sad, size = no_sad)

with placeholder1.container():
    st_lottie(sad_animation, 
        reverse=True, 
        height=250, 
        width=250, 
        speed=1, 
        loop=True, 
        quality='high', 
        key='sad'
    )
    st.title(f'You have been sad together...')
    time.sleep(2.1)


for val in idx_sad_disp:
    placeholder2.empty()
    placeholder2 = st.empty()
    with placeholder2.container():
        # calculate timestamp 10 min before and 10 min after
        low_ts = df.iloc[val].timestamp - pd.Timedelta(minutes=7)
        high_ts = df.iloc[val].timestamp + pd.Timedelta(minutes=7)
        df_sad_tmp = df[(df.timestamp > low_ts) & (df.timestamp < high_ts)]
        for index, row in df_sad_tmp.iterrows():
            if pd.isna(row.content):
                path = path_from_user + '/photos/' + row.photos[0]['uri'].split('/')[-1]
                string = row.sender_name +' at ' + str(row.timestamp) + ': '
                st.write(string)
                im = Image.open(path)
                st.image(im)
            else:
                string = row.sender_name +' at ' + str(row.timestamp) + ': ' + row.content
                st.write(string)
    time.sleep(10.1)

    

#st.markdown("### Dataframe")
#st.dataframe(df)
