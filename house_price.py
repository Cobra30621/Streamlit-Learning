import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk


st.title('台灣房價預測網站')

st.header("一、請輸入房屋資料")

st.subheader("1.房屋面積")
area_col1, area_col2, area_col3 = st.columns(3)

with area_col1:
    Transfer_Total_Ping = st.number_input('轉移坪數', step=1)
with area_col2:
    main_area = st.number_input('主建物面積', step=1)
with area_col3:
    area_ping = st.number_input('土地轉移面積', step=1)

st.subheader("2.房廳衛")
hrb_col1, hrb_col2, hrb_col3 = st.columns(3)

with hrb_col1:
    room = st.slider('房', 0, 5, 2)
with hrb_col2:
    hall = st.slider('廳', 0, 5, 2)
with hrb_col3:
    bathroom = st.slider('衛', 0, 5, 2)

st.subheader("3.其他")

house_age = st.number_input('屋齡')

Total_price = '100,000,000'
unit_price = '1,000,000'
if st.button('預測房價'):
    st.subheader("二、房價預測")
    st.success('房價 : {}'.format(Total_price))
    st.success('每坪價格 : {}'.format(unit_price))
else:
    st.write('')


df = pd.DataFrame(
    np.random.randn(1000, 2) / [25, 25] + [22.7, 120.4],
    columns=['lat', 'lon'])

st.header("三、地圖區間")
st.write("可以使用pydeck顯示地圖資料，不過需要經緯度")

st.pydeck_chart(pdk.Deck(
     map_style='mapbox://styles/mapbox/light-v9',
     initial_view_state=pdk.ViewState(
         latitude=22.6,
         longitude=120.4,
         zoom=10,
         pitch=50,
     ),
     layers=[
         pdk.Layer(
            'HexagonLayer',
            data=df,
            get_position='[lon, lat]',
            radius=200,
            elevation_scale=4,
            elevation_range=[0, 1000],
            pickable=True,
            extruded=True,
         ),
         pdk.Layer(
             'ScatterplotLayer',
             data=df,
             get_position='[lon, lat]',
             get_color='[200, 30, 0, 160]',
             get_radius=200,
         ),
     ],
 ))