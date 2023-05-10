import streamlit as st
import pandas as pd
import numpy as np

from io import BytesIO
import requests
import plotly.express as px

class GoogleSheetsReader(object):
    
    def __init__(self, sheet_id):
        self.sheet_id = sheet_id
                
    def read_sheet(self, sheet_name, use_cache=False):
        filename = '.cache/%s.csv'%sheet_name # only used for cache
        if use_cache:
            if os.path.exists(filename):
                return pd.read_csv(filename)
                
        sheet_id = self.sheet_id
        url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
        df = pd.read_csv(url) #, on_bad_lines='skip'
        if use_cache:
            df.to_csv(filename)
        return df


def read_sheet():
    GOOGLE_SHEET_ID = '11V_hq6igSe-2y80GmlSewMl2aGfV5xftRcvEBvxTLlE'
    reader = GoogleSheetsReader(GOOGLE_SHEET_ID)
    df = reader.read_sheet("Sheet1")
    df = df[[c for c in df.columns if 'Unnamed' not in c]]
    df.dropna(subset=['Price', 'Year', 'Mileage'], inplace=True)
    
    for c in 'Price', 'Year', 'Mileage':
        df[c] = df[c].astype(str).str.replace(',','').replace('$', '').astype(float)
    
    df['Wear'] = 2023-df['Year'] + df['Mileage']/7500 - 15
    return df


df = read_sheet()
df['symbol'] = df['Accident'].apply(lambda a:'circle-x' if a=='x' else 'circle')
df['color'] = df['Status'].apply(lambda s: 'None' if pd.isna(s) else s).map({'None': 1, 'NO': 0, 'SOLD': 0.5})
fig = px.scatter(df, x='Wear', y='Price', trendline='ols', height=500, hover_name='CarNo', hover_data=['Notes', 'Price', 'Mileage', 'Year'], 
          text='CarNo', symbol='symbol', color='color', color_continuous_scale=px.colors.sequential.Bluered
) #,  , color='CarNo'
#color_discrete_map = {'None': 'blue', 'NO': 'red', 'SOLD': 'gray'}
fig.update_traces(textposition='top center')
           
           
#range_color=[1, ]
#dir(px.colors.sequential)


st.title('Brame Van Shopping')

st.plotly_chart(px_chart)

st.write("Add Vans in Google Sheets [Here](https://docs.google.com/spreadsheets/d/11V_hq6igSe-2y80GmlSewMl2aGfV5xftRcvEBvxTLlE/edit?usp=sharing)")




st.table(df)