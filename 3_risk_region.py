# -*- coding: utf-8 -*-
#从全国中高风险区名单中获取深圳中高风险区名单

import json
import pandas as pd

#读取深圳疫情数据和中高风险区数据
szdata = pd.read_excel('szdata2.xlsx',index_col=0)
info = open("RiskLevelAPI-api\info.json","r",encoding='utf-8')#每日名单文件目录
file_list = json.load(info)["file_list"]

#提取出深圳的中高风险区
regions = []
for i in file_list:
    file_name = i["file_name"]
    d = file_name[:8]
    f = open("RiskLevelAPI-api/{}".format(file_name),"r",encoding='utf-8')
    data = json.load(f)
    high = data["data"]["highlist"]
    middle = data["data"]["middlelist"]
    highdf = pd.DataFrame(high)
    middledf = pd.DataFrame(middle)
    szhigh = highdf[highdf["city"] == "深圳市"]
    szmiddle = middledf[middledf["city"] == "深圳市"]
    if len(szhigh) > 0:
        for p in szhigh["communitys"]:
            for q in p:
                regions.append({"day":d, "location":q, "level":"high"})
    if len(szmiddle) > 0:
        for p in szmiddle["communitys"]:
            for q in p:
                regions.append({"day":d, "location":q, "level":"middle"})

df = pd.DataFrame(regions)
regiondf = df.drop_duplicates()#删除每日重复数据

#计算中高风险区数，提取中高风险区所在街道名单
szdata["高风险区数"] = 0
szdata["中风险区数"] = 0
szdata["风险区街道"] = ""

for m in szdata.index:
    day = str(szdata.at[m,"date"])
    hdf = regiondf[(regiondf["day"]==day) & (regiondf["level"]=="high")]
    mdf = regiondf[(regiondf["day"]==day) & (regiondf["level"]=="middle")]
    hcount = len(hdf)
    mcount = len(mdf)
    szdata.at[m,"高风险区数"] = hcount
    szdata.at[m,"中风险区数"] = mcount
    
    riskregion = []
    for n in regiondf[regiondf["day"]==day]["location"]:
        if "街道" in n:
            k = n.split("街道")
            k0 = k[0]
            if "区" in k0:
                riskregion.append(k0.split("区")[1])
            else:
                riskregion.append(k0)
    
    szdata.at[m,"风险区街道"] = list(set(riskregion))
    
szdata.to_excel('szdata3.xlsx')#保存为szdata3，此为最终的疫情数据