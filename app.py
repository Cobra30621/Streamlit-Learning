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

        area_col1, area_col2, area_col3, age_col = st.columns([1, 1, 1, 1])

        with area_col1:
            Transfer_Total_Ping = st.number_input('轉移坪數', value=20.0 )
        with area_col2:
            main_area = st.number_input('主建物面積', value=10.0 )
        with area_col3:
            area_ping = st.number_input('土地轉移面積', value=5.0 )
        with age_col:
            house_age = st.number_input('屋齡', value=10)
        

        hrb_col1, hrb_col2, hrb_col3, build_col1, build_col2 = st.columns([ 2, 2, 2, 2,2])

        with hrb_col1:
            room = st.number_input('房', step=1, value=1 ) 
        with hrb_col2:
            hall = st.number_input('廳', step=1, value=1 )
        with hrb_col3:
            bathroom = st.number_input('衛', step=1, value=1 )         
        with build_col1:
            building_total_floors = st.number_input('總樓層數', step=1, value=1 )
        with build_col2:
            min_floors_height = st.number_input('交易樓層', step=1, value=1 )

        submited = st.form_submit_button("修改房屋基本資料")

    city_col, district_col, color_col = st.columns([3, 3, 3])

    with city_col:
        city_list = st.multiselect(
        '縣市',
        dp.get_city_list(), ['臺北市']) # on_change
        

    with district_col:

        place = st.selectbox(
        '市區',
        dp.get_place_list_by_city_list(city_list))

    with color_col:
        palettes = cm.list_colormaps()
        palette = st.selectbox("圖表顏色", palettes, index=palettes.index("Blues"))

    geo_col, label_col, price_col, = st.columns([6,1,3])

    kwargs = { "Transfer_Total_Ping" : Transfer_Total_Ping, "main_area": main_area,
        "area_ping" : area_ping,
        "room" : room, "hall" : hall, "bathroom" : bathroom,
        "building_total_floors" : building_total_floors, "min_floors_height": min_floors_height,
        "house_age": house_age}

    # 繪圖
    if(len(city_list) != 0):
        with geo_col:
            # 地圖繪製
            selected_col = "price"
            gdf = dp.get_gdf_by_city(city_list)
            gdf = model.predict_by_place(gdf, **kwargs)

            gdf[selected_col] =  gdf[selected_col]
            gdf = gdf.sort_values(by=[selected_col], ascending=True)

            min_price = gdf['price_wan'].min()
            max_price = gdf['price_wan'].max()

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
                price = gdf['price_wan'][ind]
                index = int(((price - min_price) / (max_price - min_price) ) * len(colors))
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
                    # label=selected_col.title(),
                    # label="萬",
                    width=0.2,
                    height=3,
                    orientation="vertical",
                    vmin=min_price,
                    vmax=max_price,
                    font_size=10,
                )
            )
        
        with price_col:
            house_price = gdf[gdf['place'] == place].reset_index()['price_wan'][0]

            unit_price = 0
            if(Transfer_Total_Ping != 0):
                unit_price = round(house_price / Transfer_Total_Ping)

            st.subheader("{}".format(place))
            
            st.write("- 總房價　 : {}萬".format(house_price))
            st.write("- 單位房價 : {}萬".format(unit_price))

            st.subheader("房價比較")

            citys = city_list[0]
            for i in range(1, len(city_list)):
                citys +=  ", {}".format(city_list[i])

            st.write("{}".format(citys))
            
            st.write("- 最高房價 :{}萬".format(max_price))
            st.write("- 最低房價 :{}萬".format(min_price))

            # 感覺可以多用圖表

app()