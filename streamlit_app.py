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

from geopy.distance import great_circle
 
def 중심위경도찾기(위경도리스트):

    위도들 = [loc[0] for loc in 위경도리스트]
    경도들 = [loc[1] for loc in 위경도리스트]

    중심위도 = np.mean(위도들)
    중심경도 = np.mean(경도들)

    가장먼거리 = 0

    for 위도, 경도 in 위경도리스트:
        거리 = great_circle((중심위도, 중심경도),(위도, 경도)).meters

        if 거리 > 가장먼거리:
            가장먼거리 = 거리

    return f'중심위경도={중심위도,중심경도},중심과가장먼거리={round(가장먼거리)}m'

def 모든경로구하기(출발지, 경유지, 도착지):
    """
    출발지, 경유지 리스트, 도착지를 입력받아 모든 가능한 경로를 반환합니다.
    경유지의 순서만 다르게 하여 경우의 수를 계산합니다.

    Args:
        출발지 (str): 출발 지점
        경유지 (list): 경유지 리스트 (문자열)
        도착지 (str): 도착 지점

    Returns:
        list: 가능한 모든 경로를 담은 리스트. 각 경로는 리스트 형태로 표현됩니다.
    """
    모든경로 = []

    # 경유지들의 모든 순열(permutation)을 생성합니다.
    # 예를 들어, waypoints = ['A', 'B', 'C'] 일 경우,
    # ('A', 'B', 'C'), ('A', 'C', 'B'), ('B', 'A', 'C'), ... 와 같이 모든 순서가 생성됩니다.
    for p in itertools.permutations(경유지):
        # 각 순열에 출발지와 도착지를 추가하여 하나의 완전한 경로를 만듭니다.
        # list()로 p를 변환하는 이유는, permutations가 튜플을 반환하므로 리스트에 요소를 추가하기 위함입니다.
        현재경로 = [출발지] + list(p) + [도착지]
        모든경로.append(현재경로)

    return 모든경로

df_주소 = pd.DataFrame(
    [('두레팜',35.108001,127.941070),
    ('판다스',35.176365,128.144800),
    ('사천공항',35.092968,128.087211),
    ('진양호동물원',35.177215,128.036574),
    ('촉석루',35.189732,128.081857)]
, columns=['주소','위도','경도'])

주소들 = [(i[1]['위도'],i[1]['경도']) for i in df_주소.iterrows()]

중심위도 = 35.1488562
중심경도 = 128.0583024

중심과가장먼거리 = 11589

G = ox.graph.graph_from_point(
    (35.1488562, 128.0583024),
    dist=12589,
    network_type="drive"
)

중심노드 = ox.distance.nearest_nodes(G, 중심경도, 중심위도)
각노드들 = [ox.distance.nearest_nodes(G, lon, lat) for lat, lon in 주소들]

중심노드데이터 = G.nodes[중심노드]
각노드들데이터 = [G.nodes[i] for i in 각노드들]

모든경로 = 모든경로구하기(9858096125,[6538290849, 12098363819, 4691821861],9797631491)

모든노드경로 = []

for i in 모든경로:
    모든노드경로.append([[i[j],i[j+1]] for j in range(len(i)-1)])

# 최단거리후보들 구하기
최단경로후보들 = []

for i in 모든노드경로:
    경로후보 = []
    for s, e in i:
        경로후보.append([ox.routing.shortest_path(G, s, e, weight="length"), nx.path_weight(G, ox.routing.shortest_path(G, s, e, weight="length"), 'length')])
    최단경로후보들.append(경로후보)

# 최단거리 구하기
최단거리경로 = []
최단거리 = 99999999999999999

for i in 최단경로후보들:
    if 최단거리 > sum([j[1] for j in i]):
        최단거리경로 = [j[0] for j in i]
        최단거리 = sum([j[1] for j in i])

최단거리경로 = 최단거리경로[0]+list(itertools.chain(*[i[1:] for i in 최단거리경로[1:]]))

route_gdf = ox.routing.route_to_gdf(G, 최단거리경로, weight='length')

lats = []
lons = []
for geom in route_gdf['geometry']:
    if geom.geom_type == 'LineString':
        x, y = geom.xy
        lons.extend(x)
        lats.extend(y)
        lons.append(None) # 다음 세그먼트와 연결되지 않도록 None 추가
        lats.append(None)

# Plotly Scattermapbox 트레이스 생성
# 경로를 나타내는 선을 그립니다.
trace_route = go.Scattermapbox(
    mode="lines",
    lon=lons,
    lat=lats,
    line=dict(width=5, color='red'), # 경로 선 색상 및 두께 설정
    name="Shortest Route"
)

# 배경 지도를 그리기 위해 전체 그래프의 노드와 엣지를 GeoDataFrame으로 변환
nodes_gdf, edges_gdf = ox.graph_to_gdfs(G)

# Plotly Scattermapbox 트레이스 생성 (도로 네트워크)
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

trace_network = go.Scattermapbox(
    mode="lines",
    lon=network_lons,
    lat=network_lats,
    line=dict(width=1, color='gray'),
    name="Street Network"
)

# Plotly 레이아웃 설정
fig = go.Figure(data=[trace_network, trace_route]) # 네트워크 먼저, 경로 나중에 그려서 경로가 위에 보이도록

fig.update_layout(
    mapbox_style="open-street-map", # OpenStreetMap 스타일 사용
    mapbox_zoom=12,
    mapbox_center={"lat": 중심위도, "lon": 중심경도}, # 시작 노드를 중심으로 지도 이동
    margin={"r":0,"t":0,"l":0,"b":0} # 여백 제거
)

fig.show()