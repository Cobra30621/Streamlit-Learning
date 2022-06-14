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
        

    # @st.cache
    def loadModel(self):
         return joblib.load('model/model.pkl')


    def predict(self, **kwargs):
        for key, value in kwargs.items():
            # print ("%s : %s" %(key, value))
            
            self.test_data[key][0] = value
            # print (self.test_data[key][0])


        y_pred_test = self.gbm_Flag_weight.predict(self.test_data, num_iteration=self.gbm_Flag_weight.best_iteration)
        
        return y_pred_test[0]



