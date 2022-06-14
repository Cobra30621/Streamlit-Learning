import mlflow
#SERVER_HOST = os.environ.get('MLFLOW_HOST')
SERVER_HOST = 'https://www.dsml-research.com'
EXPRIMENT_NAME = 'house_project'
mlflow.set_tracking_uri(SERVER_HOST)
mlflow.set_experiment(EXPRIMENT_NAME)

import joblib
import pandas as pd
import numpy as np


adress = ''

# TEST_DATA_PATH = adress + 'output_feature/clean_data_all_test.csv'
TEST_DATA_PATH = adress + 'output_feature/clean_data_test.csv'
## 欄位型態確認
str_columns = ['Place_id','Type','compartment','manager','including_basement','including_arcade',
               'City_Land_Usage','Main_Usage_Walk','Main_Usage_Living','Main_Usage_Selling',
               'Main_Usage_Manufacturing','Main_Usage_Business','Main_Usage_Parking','Main_Usage_SnE',
               'Main_Usage_Farm','Building_Material_S','Building_Material_R','Building_Material_C',
               'Building_Material_steel','Building_Material_stone','Building_Material_B','Building_Material_W',
               'Building_Material_iron','Building_Material_tile','Building_Material_clay','Building_Material_RC_reinforce',
               'Elevator','Non_City_Land_Code','Note_Null','Note_Additions','Note_Presold','Note_Relationships',
               'Note_Balcony','Note_PublicUtilities','Note_PartRegister','Note_Negotiate','Note_Parking',
               'Note_OnlyParking','Note_Gov','Note_Overbuild','Note_Decoration','Note_Furniture','Note_Layer',
               'Note_BuildWithLandholder','Note_BlankHouse','Note_Defect','Note_Debt','Note_Elevator',
               'Note_Renewal','Note_DistressSale ','Note_OverdueInherit','Note_DeformedLand','Non_City_Land_Usage',
               'Parking_Space_Types','Building_Types',]
float_columns = ['area_m2','area_ping','house_age','room','hall','bathroom','Total_price',
                 'parking_price','main_area','ancillary_building_area','balcony_area','trading_floors_count',
                 'min_floors_height','building_total_floors','Parking_Area','Transaction_Land','Transaction_Building',
                 'Transaction_Parking','Unit_Price_Ping','Transfer_Total_Ping','CPI','CPI_rate','unemployment rate',
                 'Pain_index_3month','ppen_price','high_price','low_price','close_price','qmatch','amt_millon',
                 'return_rate_month','Turnover_rate_month','outstanding_share_thousand','Capitalization_million',
                 'excess total _ million_usdollars','import_price_index_usdollars','export_price_index_usdollars',
                 'export_million_usdollars','import_million_usdollars','survival_mobility_rate','live_deposit_mobility_interest_rate',
                 'CCI_3month','construction_engineering_index']
time_columns = ['TDATE','Month','Finish_Date','Finish_Month','Month_raw']
ID_columns = ['編號','address']

raw_data_test = pd.read_csv(TEST_DATA_PATH ,dtype = 'str')

str_columns = pd.Series(str_columns)[pd.Series(str_columns).isin(raw_data_test.columns)].tolist()
float_columns = pd.Series(float_columns)[pd.Series(float_columns).isin(raw_data_test.columns)].tolist()


def clean_data(raw_data):
        
    
    raw_data[str_columns] = raw_data[str_columns].astype('str')
    raw_data[float_columns] = raw_data[float_columns].astype('float')
    raw_data.TDATE = pd.to_datetime(raw_data.TDATE)
    raw_data.Finish_Date = pd.to_datetime(raw_data.Finish_Date)
    raw_data[['Month','Finish_Month','Month_raw']] = raw_data[['Month','Finish_Month','Month_raw']].astype("int")
    raw_data.Month = raw_data.Month.astype('int')
    
    raw_data = raw_data.drop(['編號','address','TDATE','Finish_Date','Finish_Month','Month_raw','parking_price'],axis = 1)
    
    return raw_data

## Eli clean data
def clean_and_drop(df):
    # 只篩選有包含 '住' 用途的交易案
    df = df.loc[df['Main_Usage_Living'] == 1]
    df = df.drop(columns=['Main_Usage_Living'])

    # 因為都是 0
    df = df.drop(columns=['Non_City_Land_Usage', 'Main_Usage_Walk',
                          'Main_Usage_Selling',
                          'Main_Usage_SnE'])

    # 只有 344 筆是包含工廠用途，且都不具住宅用途，故剔除
    df = df.loc[df['Main_Usage_Manufacturing'] == 0]
    df = df.drop(columns=['Main_Usage_Manufacturing'])

    # 只有 76 筆是包含停車用途，且都不具住宅用途，故剔除
    df = df.loc[df['Main_Usage_Parking'] == 0]
    df = df.drop(columns=['Main_Usage_Parking'])

    # 只有 78 筆有農業用途，且都不具住宅用途，故剔除
    df = df.loc[df['Main_Usage_Farm'] == 0]
    df = df.drop(columns=['Main_Usage_Farm'])

    # NOTICE: 我沒有錢，所以我先只買 6 房以下的
    df = df.loc[df['room'] < 6]

    df = df.loc[df['trading_floors_count'] == 1]

    # 雖然有 95 個樣本包含地下室，但是樣本太少，可能不足以推廣
    # 所以先剔除，剔除完後，都是 0 所以直接 drop
    df = df.loc[df['including_basement'] == 0]
    df = df.drop(columns=['including_basement'])

    # 所有的樣本都不包含人行道，所以直接去除這個 feature
    df = df.drop(columns=['including_arcade'])

    # 剔除交易樓層高度是 -1 (原本有一個樣本)
    df = df.loc[df['min_floors_height'] != -1]

    # 剔除交易建物是 0 個樓層的情況
    df = df.loc[df['building_total_floors'] != 0]

    # 因為車位交易 50 坪以上的資料只有 22 筆，所以先去除
    # 因為浮點數在硬體儲存會有小數點，故不能直接用 == 50.0 去比較
    df = df.loc[df['Parking_Area'] < 49.5]

    # 把農舍，廠辦踢掉
    df = df.loc[df['Building_Types'] < 8]

    # 把超大轉移坪數刪掉
    df = df.loc[df['Transfer_Total_Ping'] < 150]

    # 我先刪除 area_m2, 因為覺得跟 area_ping 的意義很類似，但是不確定會不會有些微差距。
    # 因為在 future data 中，manager 都是 0，所以也把這個欄位刪除
    # trading_floor_count 有 0 的情況，這樣應該不是房屋交易
    df = df.drop(columns=[ 'area_m2', 'manager', 'Building_Material_stone',
                           ]) #'address','TDATE',, '編號','Total_price'

    # Convert the categorical features' dtype to 'category'
    #category_columns = ['Type', 'Month', 'Month_raw',
    #                    'City_Land_Usage', 'Main_Usage_Business',
    #                    'Building_Material_S', 'Building_Material_R', 'Building_Material_C',
    #                    'Building_Material_steel', 'Building_Material_B',
    #                    'Building_Material_W', 'Building_Material_iron',
    #                    'Building_Material_tile', 'Building_Material_clay',
    #                    'Building_Material_RC_reinforce',
    #                    'Parking_Space_Types', 'Building_Types']
    #df.loc[:, category_columns] = df.loc[:,
    #                                     category_columns].astype('category')
    return df

##
y_name = ['Unit_Price_Ping','Total_price']


c_fiture = str_columns.copy()

del_column =['area_m2','manager','including_basement','including_arcade','Main_Usage_Walk','Main_Usage_Living','Main_Usage_Selling','Main_Usage_Manufacturing','Main_Usage_Parking',
 'Main_Usage_SnE','Main_Usage_Farm', 'Building_Material_stone','Non_City_Land_Usage']


c_fiture = pd.Series(c_fiture)[~pd.Series(c_fiture).isin(del_column)].tolist()


test = clean_data(raw_data_test)
test[str_columns] = test[str_columns].astype('int')
test = clean_and_drop(test)

test.dtypes.unique()


gbm_Flag_weight = joblib.load('model/model.pkl')


y_pred_test = gbm_Flag_weight.predict(test.drop(y_name,axis =1), num_iteration=gbm_Flag_weight.best_iteration)


test_0 = test.drop(y_name,axis =1).iloc[:10]


test_0.to_csv('test.csv')


data = test_data[0:0]

# 測試用

for place_id in place_df["place_id"]:
    test_data["Place_id"][0] = int(place_id)
    # print(self.test_data.iloc[[0]])
    data = data.append(test_data.iloc[[0]] , ignore_index=True)

y_pred_test = gbm_Flag_weight.predict(data, num_iteration=gbm_Flag_weight.best_iteration)
df = place_df[["place"]]
df["price"] = y_pred_test
print(df)

import matplotlib.pyplot as plt
fig = plt.figure()
ax = fig.add_axes([0,0,1,1])
langs = ['C', 'C++', 'Java', 'Python', 'PHP']
students = [23,17,35,29,12]
ax.bar(df["place"],df["price"])
plt.show()




