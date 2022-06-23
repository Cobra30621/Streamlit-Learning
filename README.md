# Streamlit-Learning

## 執行專案

### 本地端
```
streamlit run house_price.py       
```

## 套件

### GeaPandas 
- 下載
    - [Geopandas Installation— the easy way for Windows!](https://viml.nchc.org.tw/archive_blog_687/)
- 教學
    - [Python 練習: 以地圖顯示癌症死因資料(II)](https://viml.nchc.org.tw/archive_blog_687/)
    - [Simple thematic mapping of shapefile using Python?](https://gis.stackexchange.com/questions/61862/simple-thematic-mapping-of-shapefile-using-python)


## DEMO

[台灣房價預測網站](https://share.streamlit.io/cobra30621/streamlit-learning/main/uber_pickups.py)


## 教學

- [Streamlit是什麼?-Streamlit入門(1)](https://medium.com/@yt.chen/%E6%A9%9F%E5%99%A8%E5%AD%B8%E7%BF%92-%E8%B3%87%E6%96%99%E7%A7%91%E5%AD%B8%E6%A1%86%E6%9E%B6%E6%87%89%E7%94%A8-streamlit%E5%85%A5%E9%96%80-1-d07478cd4d8)
- [Streamlit官網教學](https://docs.streamlit.io/library/get-started) 


## 更新模型步驟
- 下載
    - 去mlflow下載模型
    - 去OneDrive下載資料集
- 用Sypder打開資料....

data_d = test.reset_index()[0:1]
data_d = data_d.drop(columns=['Unit_Price_Ping', 'Total_price'])
data_d.to_csv('Output_feature/test.csv')
