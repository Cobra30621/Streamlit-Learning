import joblib
import pandas as pd
import numpy as np
from sqlalchemy import false
import streamlit as st

class ModelManager():
    def __init__(self):
        
        self.gbm_Flag_weight = self.loadModel('model/model.pkl')
        self.test_data = pd.read_csv('csv/test.csv')
        
    @st.cache # 建立快取
    def loadModel(self, model_path):
        print("ModelManager load model:" + model_path)
        return joblib.load(model_path)


    def predict(self, **kwargs):
        for key, value in kwargs.items():
            # print ("%s : %s" %(key, value))
            
            self.test_data.loc[0, key] = value
            # print (self.test_data[key][0])

        # print (self.test_data["Place_id"][0])

        y_pred_test = self.gbm_Flag_weight.predict(self.test_data, num_iteration=self.gbm_Flag_weight.best_iteration)
        
        return y_pred_test[0]

    def predict_by_place(self,place_df, **kwargs):
        for key, value in kwargs.items():
            
            self.test_data[key][0] = value

        data = self.test_data[0:0]

        for place_id in place_df["place_id"]:
            self.test_data["Place_id"][0] = int(place_id)
            # print(self.test_data.iloc[[0]])
            data = data.append(self.test_data.iloc[[0]] , ignore_index=True)


        y_pred_test = self.gbm_Flag_weight.predict(data, num_iteration=self.gbm_Flag_weight.best_iteration)
        print(y_pred_test)
        df = place_df[["place"]]
        df["price"] = y_pred_test
        print(df)


        return df


# 將使用者輸入資料，轉成模型所需資料
class DataPreprocessor():
    def __init__(self):

        self.place_df = self.load_csv('csv/place_id.csv')

    @st.cache # 建立快取
    def load_csv(self, file_path):
        print("DataPreprocessor load csv:" + file_path)
        return pd.read_csv(file_path)

    def get_place_id(self, palce):
        return self.place_df[self.place_df['place'] == palce].reset_index()['place_id'][0]

    def get_economy_indicators(self, date):
        print(date)

    def get_place_list(self):
        return self.place_df['place']