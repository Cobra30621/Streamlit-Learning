import datetime
import os
import pathlib
import requests
import zipfile
import pandas as pd
import pydeck as pdk
import geopandas as gpd
from sqlalchemy import false
import streamlit as st
import leafmap.colormaps as cm
from leafmap.common import hex_to_rgb
from model import DataPreprocessor, ModelManager


def app():
    st.title("台灣房價地圖")


    selected_col = "price"

    dp = DataPreprocessor()
    gdf = dp.get_gdf()

    mm = ModelManager()
    gdf = mm.predict_by_place(gdf)

    gdf[selected_col] =  gdf[selected_col].astype(str).astype(float).astype(int)
    gdf = gdf.sort_values(by=[selected_col], ascending=True)

   

    min_value = gdf[selected_col].min()
    max_value = gdf[selected_col].max()

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
    palettes = cm.list_colormaps()
    palette = st.selectbox("Color palette", palettes, index=palettes.index("Blues"))
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
        "html": "<b>Name:</b> {"+ 'place' + "}<br><b>Value:</b> {"
        +  'price'
        + "}",
        "style": {"backgroundColor": "steelblue", "color": "white"},
    }

    layers = [geojson]

    r = pdk.Deck(
        layers=layers,
        initial_view_state=initial_view_state,
        map_style="light",
        tooltip=tooltip,
    )

    row3_col1, row3_col2 = st.columns([6, 1])

    with row3_col1:
        st.pydeck_chart(r)
    with row3_col2:
        st.write(
            cm.create_colormap(
                palette,
                label=selected_col.title(),
                width=0.2,
                height=3,
                orientation="vertical",
                vmin=min_value,
                vmax=max_value,
                font_size=10,
            )
        )
    
app()