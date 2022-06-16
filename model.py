import joblib
import pandas as pd
import numpy as np
import streamlit as st

class ModelManager():
    

    def __init__(self):
        self.test_data = pd.read_csv('test.csv', index_col=False)
        # print(self.test_data)
        # self.test_data = self.test_data.drop(['Unnamed: 0'],axis =1)[0]
        
        self.gbm_Flag_weight = self.loadModel()
        

    @st.cache
    def loadModel(self):
         return joblib.load('model/model.pkl')


    def predict(self, **kwargs):
        for key, value in kwargs.items():
            # print ("%s : %s" %(key, value))
            
            self.test_data[key][0] = value
            # print (self.test_data[key][0])

        print (self.test_data["Place_id"][0])

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



