import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
from model import DataPreprocessor, ModelManager
import time
import geopandas as gpd
import pandas as pd
import components as cp

import geopandas

def app():
    cp.create_sidebar()
    # 事前讀取
    model = ModelManager()
    dp = DataPreprocessor()

    st.title('台灣房價預測')
    st.markdown(
        """**介紹:** This interactive dashboard is designed for visualizing U.S. real estate data and market trends at multiple levels (i.e., national,
         state, county, and metro). The data sources include [Real Estate Data](https://www.realtor.com/research/data) from realtor.com and 
         [Cartographic Boundary Files](https://www.census.gov/geographies/mapping-files/time-series/geo/carto-boundary-file.html) from U.S. Census Bureau.
         Several open-source packages are used to process the data and generate the visualizations, e.g., [streamlit](https://streamlit.io),
          [geopandas](https://geopandas.org), [leafmap](https://leafmap.org), and [pydeck](https://deckgl.readthedocs.io).
    """
    )

    st.header("一、請輸入房屋資料")

    area_col1, area_col2, area_col3, \
    hrb_col1, hrb_col2, hrb_col3 = st.columns([2, 2, 2, 1, 1, 1])

    with area_col1:
        Transfer_Total_Ping = st.number_input('轉移坪數', value=20.0 )
    with area_col2:
        main_area = st.number_input('主建物面積', value=10.0 )
    with area_col3:
        area_ping = st.number_input('土地轉移面積', value=5.0 )

    with hrb_col1:
        room = st.number_input('房', step=1, value=1 ) 
    with hrb_col2:
        hall = st.number_input('廳', step=1, value=1 )
    with hrb_col3:
        bathroom = st.number_input('衛', step=1, value=1 ) 

    city_col, district_col, build_col1, build_col2, age_col = st.columns([3, 3, 2, 2, 2])

    with city_col:
        city_option = st.selectbox(
        '縣市',
        dp.get_city_list(), index = 1)

    with district_col:
        district_option = st.selectbox(
        '區',
        dp.get_district_list(city_option), index = 1)
        
    with build_col1:
        building_total_floors = st.number_input('總樓層數', step=1, value=1 )
    with build_col2:
        min_floors_height = st.number_input('交易樓層', step=1, value=1 )

    with age_col:
        house_age = st.number_input('屋齡', value=10)
    
    submited = st.button("預測房價")

    if (submited):
        place_id = dp.get_place_id(city_option + district_option)
        kwargs = { "Transfer_Total_Ping" : Transfer_Total_Ping, "main_area": main_area,
            "area_ping" : area_ping,
            "room" : room, "hall" : hall, "bathroom" : bathroom,
            "building_total_floors" : building_total_floors, "min_floors_height": min_floors_height,
            "house_age": house_age, "Place_id" : place_id}

        Total_price = model.predict(**kwargs)
        house_price = format(round(Total_price), ',d')

        unit_price = 0
        if(Transfer_Total_Ping != 0):
            unit_price = format(round(Total_price / Transfer_Total_Ping), ',d')

        st.header("二、房價預測")
        st.markdown('#### 總房價 : {}'.format(house_price))
        st.markdown('#### 單價元平方公尺 : {}'.format(unit_price))
        st.info("計算方式: 總房價 / 轉移面積")




app()

# df = model.predict_by_place(place_df, **kwargs)
# st.bar_chart(df["price"])

