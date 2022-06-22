import joblib
import pandas as pd
import numpy as np
# from sqlalchemy import false
import streamlit as st
import geopandas as gpd

class ModelManager():
    def __init__(self):
        self.gbm_Flag_weight = self.loadModel('model/model.pkl')
        self.test_data = pd.read_csv('csv/test.csv')
        
    # @st.cache # 建立快取
    def loadModel(self, model_path):
        print("ModelManager load model:" + model_path)
        return joblib.load(model_path)


    def predict(self, **kwargs):
        for key, value in kwargs.items():
            self.test_data.loc[0, key] = value

        y_pred_test = self.gbm_Flag_weight.predict(self.test_data, num_iteration=self.gbm_Flag_weight.best_iteration)
        
        return y_pred_test[0]

    def predict_by_place(self, place_df, **kwargs):
        for key, value in kwargs.items():
            
            self.test_data[key][0] = value

        data = self.test_data[0:0]

        for place_id in place_df["place_id"]:
            self.test_data["Place_id"][0] = int(place_id)
            # print(self.test_data.iloc[[0]])
            data = data.append(self.test_data.iloc[[0]] , ignore_index=True)


        y_pred_test = self.gbm_Flag_weight.predict(data, num_iteration=self.gbm_Flag_weight.best_iteration)
        # print(y_pred_test)
        df = place_df
        df["price"] = y_pred_test.astype(int)
        df["price_"] = df.apply(lambda x : format(x["price"], ','), axis=1 )
        df["price_wan"] = df.apply(lambda x : round(x["price"] / 10000) , axis=1 )
        
        # print(df)
        return df

    def number_2_wan(self, number):
        return round(number / 1000)


# 將使用者輸入資料，轉成模型所需資料
class DataPreprocessor():
    def __init__(self):

        self.place_df = self.load_csv('csv/place_id.csv')
        self.gdf = gpd.read_file('mapdata202203151020/TOWN_MOI_1100415.shp', encoding='utf-8')
        self.gdf['place'] = self.gdf['COUNTYNAME'] + self.gdf['TOWNNAME']
        self.gdf = pd.merge(self.gdf, self.place_df, on ="place")
        self.city_list = ['臺北市', '新北市', '基隆市', '桃園市', '新竹縣', 
            '宜蘭縣', '苗栗縣', '臺中市', '彰化縣', '雲林縣', '嘉義縣', 
            '臺南市', '高雄市', '屏東縣', '臺東縣', '花蓮縣', '南投縣',    
            '澎湖縣', '連江縣', '金門縣' ]
               

    # @st.cache # 建立快取
    def load_csv(self, file_path):
        print("DataPreprocessor load csv:" + file_path)
        return pd.read_csv(file_path)

    def get_place_id(self, city, district):
        return self.place_df[self.place_df['place'] == city + district]\
            .reset_index()['place_id'][0]

    def get_place_id(self, palce):
        return self.place_df[self.place_df['place'] == palce].reset_index()['place_id'][0]

    def get_city_list(self):
        # return self.gdf['COUNTYNAME'].unique()
        return self.city_list

    def get_district_list(self, city):
        return self.gdf['TOWNNAME'][self.gdf['COUNTYNAME'] == city].unique()

    def get_place_list(self):
        return self.place_df['place']
    
    def get_gdf(self):
        return self.gdf

    def get_gdf_by_city(self, city):
        return self.gdf [self.gdf["COUNTYNAME"] == city]
    
    def get_economy_indicators(self, date):
        print(date)