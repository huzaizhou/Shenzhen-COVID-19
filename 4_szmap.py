# -*- coding: utf-8 -*-
#从深圳道路交通运行指数系统获取深圳分街道边界数据

import requests
import json
import pandas as pd
import geopandas as gpd
from shapely import geometry

#提取分街道数据，保存为gdf
url = "http://tocc.jtys.sz.gov.cn/static/geojson/sz_block_mars.json"
text = requests.get(url).text
data = json.loads(text)
poly,district,street = [],[],[]
for i in range(74):
    coord = data["features"][i]["geometry"]["coordinates"]
    if len(coord) > 1:
        mpoly = []
        for j in coord:
            single = list(map(tuple,j[0]))
            mpoly.append(geometry.Polygon(single))
        poly.append(geometry.MultiPolygon(mpoly))
    else:
        poly.append(geometry.Polygon(list(map(tuple,coord[0]))))
    district.append(data["features"][i]["properties"]["DISTRICT"])
    street.append(data["features"][i]["properties"]["NAME"])

df = pd.DataFrame({"name":street,"geometry":poly,"district":district})
gdf = gpd.GeoDataFrame(df)
gdf.crs = 'EPSG:4326'

#将街道数据整合成各区数据gdf2
def union(poly):
    x = poly[0]
    for y in poly[1:]:
        print(x)
        x = x.union(y)
    return x.boundary

dist_name = list(set(df["district"]))
dist_poly = []
for k in dist_name:
    mp = list(gdf[gdf["district"]==k]["geometry"])
    dist_poly.append(union(mp))
df2 = pd.DataFrame({"name":dist_name,"geometry":dist_poly})
gdf2 = gpd.GeoDataFrame(df2)
gdf2.crs = 'EPSG:4326'

#保存文件
gdf.to_file(r"szstreet.gpkg", driver="GPKG")
gdf2.to_file("szdistrict.gpkg", driver="GPKG")