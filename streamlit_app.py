import streamlit as st

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

import plotly.express as px
import plotly.graph_objects as go

import folium
import networkx as nx
import osmnx as ox
import geopandas as gpd

from geopy.distance import great_circle

import pickle

중심위도 = 35.1488562
중심경도 = 128.0583024

input_path_shp = "./gdf/cities.shp"
route_gdf = gpd.read_file(input_path_shp)

nodes_input_path_pkl = "./node_edge/nodes.pkl"
edges_input_path_pkl = "./node_edge/edges.pkl"

with open(nodes_input_path_pkl, 'rb') as f:
    loaded_nodes_gdf_pkl = pickle.load(f)

with open(edges_input_path_pkl, 'rb') as f:
    loaded_edges_gdf_pkl = pickle.load(f)

lats = []
lons = []
for geom in route_gdf['geometry']:
    if geom.geom_type == 'LineString':
        x, y = geom.xy
        lons.extend(x)
        lats.extend(y)
        lons.append(None) # 다음 세그먼트와 연결되지 않도록 None 추가
        lats.append(None)

# Plotly Scattermap 트레이스 생성
# 경로를 나타내는 선을 그립니다.
trace_route = go.Scattermap(
    mode="lines",
    lon=lons,
    lat=lats,
    line=dict(width=5, color='red'), # 경로 선 색상 및 두께 설정
    name="Shortest Route"
)

# 배경 지도를 그리기 위해 전체 그래프의 노드와 엣지를 GeoDataFrame으로 변환
nodes_gdf, edges_gdf = loaded_nodes_gdf_pkl, loaded_edges_gdf_pkl

# Plotly Scattermap 트레이스 생성 (도로 네트워크)
# 모든 도로를 회색으로 그립니다.
network_lats = []
network_lons = []
for geom in edges_gdf['geometry']:
    if geom.geom_type == 'LineString':
        x, y = geom.xy
        network_lons.extend(x)
        network_lats.extend(y)
        network_lons.append(None)
        network_lats.append(None)

trace_network = go.Scattermap(
    mode="lines",
    lon=network_lons,
    lat=network_lats,
    line=dict(width=1, color='gray'),
    name="Street Network"
)

# Plotly 레이아웃 설정
minx, miny, maxx, maxy = route_gdf.total_bounds
center_lat = (miny + maxy) / 2
center_lon = (minx + maxx) / 2

fig = go.Figure(data=[trace_network, trace_route]) # 네트워크 먼저, 경로 나중에 그려서 경로가 위에 보이도록

fig.update_layout(
    hovermode='closest',
    map=dict(
        bearing=0,
        center=go.layout.map.Center(
            lat=center_lat,
            lon=center_lon
        ),
        pitch=0,
        zoom=5
    )
)

st.plotly_chart(fig)