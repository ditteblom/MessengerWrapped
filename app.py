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

from langchain.chat_models import ChatOpenAI
from langchain.schema import AIMessage, HumanMessage, SystemMessage

# set up dashboard page
st.set_page_config(
    page_title="Facebook Messages Wrapped",
    page_icon="✅",
)

f = open("openai_key.txt", "r")
openai_key = f.read()

###################################
# get fun animations
path = "animations/animation_lnmxxffi.json"
with open(path,"r") as file: 
    animation_messages = json.load(file)

path = "animations/sad_animation.json"
with open(path,"r") as file: 
    sad_animation = json.load(file)

path = "animations/cooking_animation.json"
with open(path,"r") as file: 
    cooking_animation = json.load(file)

#######################################
# get data from uploaded files

placeholder = st.empty()

with placeholder.container():
    openai_key = st.text_input('Please input your OpenAI key.')

if openai_key:
    placeholder.empty()

    placeholder = st.empty()

    with placeholder.container():
        path_from_user = st.text_input('Please input path to directory for the chat.')

    if path_from_user:
        placeholder.empty()

        df, participants = create_df(path_from_user)
        df.timestamp = pd.to_datetime(df.timestamp)
        df['time_formatted'] = df['timestamp'].dt.strftime('%H:%M')

        frst_date = df.sort_values(by='date').iloc[0].date
        last_date = df.sort_values(by='date').iloc[-1].date

        no_messages = df.count().content
        no_photos = df.count().photos
        no_gifs = df.count().gifs
        no_videos = df.count().videos
        no_files = df.count().files

        # most active person
        most_active = df.groupby(by='sender_name').count().sort_values(by='content',ascending=False).reset_index().iloc[0].sender_name
        most_active_messages = df.groupby(by='sender_name').count().sort_values(by='content',ascending=False).reset_index().iloc[0].content
        most_active_photos = df[df.sender_name == most_active].count().photos
        most_active_gifs = df[df.sender_name == most_active].count().gifs
        most_active_videos = df[df.sender_name == most_active].count().videos
        most_active_files = df[df.sender_name == most_active].count().files
        # least active
        least_active = df.groupby(by='sender_name').count().sort_values(by='content',ascending=False).reset_index().iloc[-1].sender_name
        least_active_no_messages = df.groupby(by='sender_name').count().sort_values(by='content',ascending=False).reset_index().iloc[-1].content
        most_pictures = df.groupby(by='sender_name').count().sort_values(by='photos',ascending=False).reset_index().iloc[0].sender_name
        most_gifs = df.groupby(by='sender_name').count().sort_values(by='gifs',ascending=False).reset_index().iloc[0].sender_name

        df_top = df[df.no_reactions >= 4]

        # insert loading animation
        placeholder = st.empty()
        with placeholder.container():
            st.title(f'Almost ready!')
            st_lottie(cooking_animation, 
                    reverse=False, 
                    height=500, 
                    width=500, 
                    speed=1, 
                    loop=True, 
                    quality='high', 
                    key='cooking'
                )


###################################
# use ChatGPT
# chat = ChatOpenAI(temperature=0, openai_api_key=openai_key, model = 'gpt-3.5-turbo')

# df_top = df[df.no_reactions >= 4]
# df_top = df_top.dropna(subset=['content'])
# df_top = df_top[df_top['content'].str.contains('sent an attachment')==False]
# np.random.seed(20)
# idx_ = np.random.choice(len(df_top), size = 20, replace = False)
# df_idx = df_top.iloc[idx_]

# # get sentiment scores
# scores = []
# message_in = ''

# for i in range(len(df_idx)):
#     message_in += df_idx.iloc[i].content + '\t'

# messages = [
#     SystemMessage(
#         content="You are a helpful assistant that gives each message a score on the sentiment of each of the messages \
#                 which are seperated by \t. Negative scores are angy/sad and positive scores are happy/funny. \
#                 Give messages involving Birthdays and/or Christmas a score of NaN. Only give one score per message,\
#                 there are 20 messages in total.\
#                 For each message return in this format: Message #no, Score: #score"
#     ),
#     HumanMessage(
#         content=message_in
#     ),
#             ]
# res = chat(messages).content
# sent_scores = res.split('\n')
# df_idx = df_idx.iloc[:len(sent_scores)]
# df_idx['sentiment_score'] = sent_scores
# df_idx['sentiment_score'] = df_idx['sentiment_score'].apply(lambda x: float(x.split(' ')[-1]))
# df_idx = df_idx.dropna(subset=['sentiment_score'])

# df_idx.to_csv('df_idx.csv')

df_idx = pd.read_csv('df_idx.csv', index_col = 0)

print_idx = []

if len(df_idx) < 3:
    len_print = len(df_idx)
else:
    len_print = 3

for i in range(len_print):
    print_idx.append(df_idx.sort_values(by='sentiment_score').iloc[-i].name)

q_list = []
conv_list = []

time.sleep(10)

# for idx in print_idx:
#     idx_ts = pd.to_datetime(df.iloc[idx].timestamp)
#     tmp = df[(df.timestamp > idx_ts-pd.Timedelta(minutes=60)) & (df.timestamp < idx_ts+pd.Timedelta(minutes=60))]
#     # for nice formatting of timestamps
#     #tmp['time_formatted'] = tmp['timestamp'].dt.strftime('%H:%M')

#     string_message = str(df.iloc[idx].date) + ': '
#     conv_list_tmp = []
#     for i in range(len(tmp)):
#         string_message += str(tmp.iloc[i].content) + '\n'

#     if len(tmp) < 5:
#         for j in range(len(tmp)):
#             conv_list_tmp.append(tmp.iloc[j].sender_name.split(' ')[0] + ' at ' + tmp.iloc[j].time_formatted + ': ' + str(tmp.iloc[j].content))
#         conv_list.append(conv_list_tmp)
#     else:
#         j = -2
#         for _ in range(5):
#             conv_list_tmp.append(df.iloc[idx + j].sender_name.split(' ')[0] + ' at ' + df.iloc[idx + j].time_formatted + ': ' + str(df.iloc[idx + j].content))
#             j += 1
#         conv_list.append(conv_list_tmp)

#     messages = [
#     SystemMessage(
#         content="You are a helpful assistant that summarizes a conversation between friends.\
#                 You will summarize the content and sentiment of the conversation.\
#                 Start every returned message with: Do you remember on *insert date* when...\
#                 Only return one sentence. The date in stated in the beggining of the conversation."
#     ),
#     HumanMessage(
#         content=string_message
#     ),
#     ]
#     q_list.append(chat(messages).content)

# conv_list_df = pd.DataFrame(conv_list)
# conv_list_df.to_csv('conv_list')
# q_list_df = pd.DataFrame(q_list)
# q_list_df.to_csv('q_list')

conv_list_df = pd.read_csv('conv_list')
conv_list = []
q_list = []
q_list_df = pd.read_csv('q_list')
for i in range(len(conv_list_df)):
    conv_list.append(conv_list_df.iloc[i].to_list()[1:])
    q_list.append(q_list_df.iloc[i][1])


####################################
# create the facebook messages wrapped!

# clear whole page
placeholder.empty()

placeholder = st.empty()

with placeholder.container():
    st.title(f'Since {frst_date} there has been communication between...')
    col1, col2 = st.columns(2)
    # set header
    i = 1
    for participant in participants:
        time.sleep(1.1)
        if (i%2) == 0:
            col2.header(participant)
        else:
            col1.header(participant)
        i += 1
    time.sleep(1.5)

# clear whole page
placeholder.empty()

# create new placeholder
placeholder = st.empty()

with placeholder.container():
    col1, col2 = st.columns(2)
    with col1:
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
    string = f'In these {(last_date-frst_date).days} days, you have been writing {no_messages} messages to each other'
    if no_photos > 0:
        string += f', sending {no_photos} photos'
    if no_videos > 0:
        string += f', {no_videos} videos'
    if no_gifs > 0:
        string += f', {no_gifs} gifs'
    if no_files > 0:
        string += f', {no_files} files'
    col2.title(string)
    time.sleep(1.8)
    # set header
    col2.header('Wow! :open_mouth:')

    time.sleep(4.9)

# clear whole page
placeholder.empty()

# create new placeholder
placeholder = st.empty()
with placeholder.container():
    st.header('The most active person was...')
    time.sleep(2.1)
    st.title(most_active)
    st.balloons()
    time.sleep(2.1)
    string = f'writing {most_active_messages} messages'
    if most_active_photos > 0:
        string += f', sending {most_active_photos} photos'
    if most_active_videos > 0:
        string += f', {most_active_videos} videos'
    if most_active_gifs > 0:
        string += f', {most_active_gifs} gifs'
    if most_active_files > 0:
        string += f', {most_active_files} files'
    st.header(string)
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
placeholder = st.empty()

with placeholder.container():
    st.title(q_list[0])
    time.sleep(2.1)
    for string in conv_list[0]:
        st.write(string)
        time.sleep(0.9)
    time.sleep(8.7)

placeholder.empty()

# create new placeholder
placeholder = st.empty()

with placeholder.container():
    st.title(q_list[1])
    time.sleep(2.1)
    for string in conv_list[1]:
        st.write(string)
        time.sleep(0.9)
    time.sleep(8.7)

placeholder.empty()

# create new placeholder
placeholder = st.empty()

with placeholder.container():
    st.title(q_list[2])
    time.sleep(2.1)
    for string in conv_list[2]:
        st.write(string)
        time.sleep(0.9)
    time.sleep(8.7)
