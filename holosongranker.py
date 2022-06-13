import streamlit as st
import pandas as pd
import numpy as np


st.title('HoloSongRanker')

DATE_COLUMN = 'date/time'
DATA_URL = 'vtubers_bar.csv'

@st.cache
def load_data():
    data = pd.read_csv(DATA_URL)
    return data

data_load_state = st.text('Loading data...')
data = load_data()
data_load_state.text("Done! (using st.cache)")

if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)

st.subheader('VTubers View')
chart_data = pd.DataFrame(
     np.random.randn(20, 3),
     columns=['a', 'b', 'c'])

line_data = data[['2022-05-08','2022-05-15','2022-05-22','2022-05-29','2022-06-05']]
line_data.index = data[['title']]
line_data_t = line_data.T

print(line_data_t)
print(chart_data)
st.line_chart(line_data_t)
