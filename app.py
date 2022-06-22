import pandas as pd
import pydeck as pdk
import geopandas as gpd
import streamlit as st
import leafmap.colormaps as cm
from leafmap.common import hex_to_rgb
from model import DataPreprocessor, ModelManager
import components as cp



def app():

    cp.create_sidebar()

    st.title("台灣房價地圖")
    st.markdown(
        """**介紹:** OWO
    """
    )

    dp = DataPreprocessor()
    model = ModelManager()

    with st.form("my_form"):

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
            dp.get_city_list()) # on_change
            print(dp.get_city_list())

        with district_col:

            district_option = st.selectbox(
            '區',
            dp.get_district_list(city_option))
            
        with build_col1:
            building_total_floors = st.number_input('總樓層數', step=1, value=1 )
        with build_col2:
            min_floors_height = st.number_input('交易樓層', step=1, value=1 )

        with age_col:
            house_age = st.number_input('屋齡', value=10)
    
        submited = st.form_submit_button("預測房價")
        # submited = st.button("預測房價")

    palettes = cm.list_colormaps()
    palette = st.selectbox("圖表顏色", palettes, index=palettes.index("Blues"))

    geo_col, label_col, price_col, = st.columns([6,1,3])

    place_id = dp.get_place_id(city_option + district_option)

    kwargs = { "Transfer_Total_Ping" : Transfer_Total_Ping, "main_area": main_area,
        "area_ping" : area_ping,
        "room" : room, "hall" : hall, "bathroom" : bathroom,
        "building_total_floors" : building_total_floors, "min_floors_height": min_floors_height,
        "house_age": house_age}

    # 繪圖
    with geo_col:
        # 地圖繪製
        selected_col = "price"
        # gdf = dp.get_gdf()
        gdf = dp.get_gdf_by_city(city_option)
        gdf = model.predict_by_place(gdf, **kwargs)

        gdf[selected_col] =  gdf[selected_col]
        gdf = gdf.sort_values(by=[selected_col], ascending=True)

        min_value = gdf['price_wan'].min()
        max_value = gdf['price_wan'].max()

        initial_view_state = pdk.ViewState(
            latitude=23.5,
            longitude=121,
            zoom=7,
            max_zoom=20,
            pitch=0,
            bearing=0,
            height=700,
            width=None,
        )

        
        # 顏色參數
        
        n_colors = 10
        color_exp = f"[R, G, B]"

        colors = cm.get_palette(palette, n_colors)
        colors = [hex_to_rgb(c) for c in colors]

        for i, ind in enumerate( gdf.index):
            index = int(i / (len( gdf) / len(colors)))
            if index >= len(colors):
                index = len(colors) - 1
            gdf.loc[ind, "R"] = colors[index][0]
            gdf.loc[ind, "G"] = colors[index][1]
            gdf.loc[ind, "B"] = colors[index][2]

        geojson = pdk.Layer(
            "GeoJsonLayer",
            gdf,
            pickable=True,
            opacity=0.5,
            stroked=True,
            filled=True,
            extruded=False,
            wireframe=True,
            get_elevation=selected_col,
            elevation_scale=1,
            get_fill_color=color_exp,
            get_line_color=[0, 0, 0],
            get_line_width=2,
            line_width_min_pixels=1,
        )

        tooltip = {
            "html": "<b>地區:</b> {"+ 'place' + "}<br><b>價格:</b> {"
            +  'price_wan'
            + "}萬",
            "style": {"backgroundColor": "steelblue", "color": "white"},
        }

        layers = [geojson]

        r = pdk.Deck(
            layers=layers,
            initial_view_state=initial_view_state,
            map_style="light",
            tooltip=tooltip,
        )

        
        st.pydeck_chart(r)

    with label_col:
        st.write(
            cm.create_colormap(
                palette,
                label=selected_col.title(),
                # label="萬",
                width=0.2,
                height=3,
                orientation="vertical",
                vmin=min_value,
                vmax=max_value,
                font_size=10,
            )
        )
    
    with price_col:
        house_price = gdf[gdf['place_id'] == place_id].reset_index()['price_wan'][0]

        unit_price = 0
        if(Transfer_Total_Ping != 0):
            unit_price = round(house_price / Transfer_Total_Ping)

        st.subheader("{}{}".format(city_option, district_option))
        
        st.write("- 總房價　 : {}萬".format(house_price))
        st.write("- 單位房價 : {}萬".format(unit_price))

        st.subheader("{}房價".format(city_option))
        
        max_house_price = gdf['price_wan'][gdf['COUNTYNAME'] == city_option].max()
        min_house_price = gdf['price_wan'][gdf['COUNTYNAME'] == city_option].min()

        st.write("- 最高房價 :{}萬".format(max_house_price))
        st.write("- 最低房價 :{}萬".format(min_house_price))

        # 感覺可以多用圖表

app()