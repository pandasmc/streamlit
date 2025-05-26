from pygwalker.api.streamlit import StreamlitRenderer
import pandas as pd
import streamlit as st
 
# Adjust the width of the Streamlit page
st.set_page_config(
    page_title="Use Pygwalker In Streamlit",
    layout="wide"
)
# Import your data
df = pd.read_csv("https://github.com/pandasmc/streamlit/raw/refs/heads/main/data/%ED%99%98%EA%B2%BD%EB%B6%80%20%EA%B5%AD%EA%B0%80%EB%AF%B8%EC%84%B8%EB%A8%BC%EC%A7%80%EC%A0%95%EB%B3%B4%EC%84%BC%ED%84%B0_%EA%B5%AD%EA%B0%80%20%EB%8C%80%EA%B8%B0%EC%98%A4%EC%97%BC%EB%AC%BC%EC%A7%88%20%EB%B0%B0%EC%B6%9C%EB%9F%89%20%ED%86%B5%EA%B3%84_20221231.csv")
 
pyg_app = StreamlitRenderer(df)
 
pyg_app.explorer()