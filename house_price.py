import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
from model import DataPreprocessor, ModelManager
import time
import geopandas as gpd
import pandas as pd

import geopandas

# df = pd.DataFrame(
#     {'City': ['Buenos Aires', 'Brasilia', 'Santiago', 'Bogota', 'Caracas'],
#      'Country': ['Argentina', 'Brazil', 'Chile', 'Colombia', 'Venezuela'],
#      'Latitude': [-34.58, -15.78, -33.45, 4.60, 10.48],
#      'Longitude': [-58.66, -47.91, -70.66, -74.08, -66.86]})
# gdf = geopandas.GeoDataFrame(
#     df, geometry=geopandas.points_from_xy(df.Longitude, df.Latitude))
# st.write(gdf.head())
# world = geopandas.read_file(geopandas.datasets.get_path('naturalearth_lowres'))
# ax = world[world.continent == 'South America'].plot(
#     color='white', edgecolor='black')
# gdf.plot(ax=ax, color='red')
# st.pyplot()


# town_shp = gpd.read_file('mapdata202203151020/TOWN_MOI_1100415.shp', encoding='utf-8')
# print(town_shp['COUNTYNAME'] )
# print(town_shp[town_shp['COUNTYNAME'] == '臺北市'])

# ax = town_shp[town_shp['TOWNNAME'] != '旗津區'].plot(
#     cmap='RdBu')
# # st.set_option('deprecation.showPyplotGlobalUse', False)
# st.pyplot()

# print(town_shp.head())
# map = town_shp.plot(cmap='RdBu')

# st.write(map)

# 事前讀取
model = ModelManager()
dp = DataPreprocessor()

st.title('台灣房價預測網站')


with st.form("imput_form"):
    st.header("一、請輸入房屋資料")

    st.subheader("1.房屋面積")
    area_col1, area_col2, area_col3 = st.columns(3)

    with area_col1:
        Transfer_Total_Ping = st.number_input('轉移坪數', value=20.0 )
    with area_col2:
        main_area = st.number_input('主建物面積', value=10.0 )
    with area_col3:
        area_ping = st.number_input('土地轉移面積', value=5.0 )

    st.subheader("2.房廳衛")
    hrb_col1, hrb_col2, hrb_col3 = st.columns(3)

    with hrb_col1:
        room = st.number_input('房', step=1, value=1 ) 
    with hrb_col2:
        hall = st.number_input('廳', step=1, value=1 )
    with hrb_col3:
        bathroom = st.number_input('衛', step=1, value=1 ) 

    st.subheader("3.房子高度")


    build_col1, build_col2 = st.columns(2)
    with build_col1:
        building_total_floors = st.number_input('總樓層數', step=1, value=1 )
    with build_col2:
        min_floors_height = st.number_input('交易樓層', step=1, value=1 )


    st.subheader("4.其他")
    other_col1, other_col2 = st.columns(2)
    with other_col1:
        house_age = st.number_input('屋齡', value=10)
    with other_col2:
        option = st.selectbox(
        '市區',
        dp.get_place_list(), index = 1)
        place_id = dp.get_place_id(option)
        # print(option , place_id)

    # submited = st.button('預測')
    submited = st.form_submit_button("預測房價")



kwargs = { "Transfer_Total_Ping" : Transfer_Total_Ping, "main_area": main_area,
    "area_ping" : area_ping,
    "room" : room, "hall" : hall, "bathroom" : bathroom,
    "building_total_floors" : building_total_floors, "min_floors_height": min_floors_height,
    "house_age": house_age, "Place_id" : place_id}

if (submited):
    Total_price = model.predict(**kwargs)
    house_price = format(round(Total_price), ',d')

    # # 直後要加真的在跑
    # with st.spinner('模型預測中'):
    #     time.sleep(0.1)

    unit_price = 0
    if(Transfer_Total_Ping != 0):
        unit_price = format(round(Total_price / Transfer_Total_Ping), ',d')

    st.header("二、房價預測")
    st.markdown('#### 總房價 : {}'.format(house_price))
    st.markdown('#### 單價元平方公尺 : {}'.format(unit_price))
    st.info("計算方式: 總房價 / 轉移面積")


# df = model.predict_by_place(place_df, **kwargs)
# st.bar_chart(df["price"])

