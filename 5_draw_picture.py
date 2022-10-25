# -*- coding: utf-8 -*-
import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
from matplotlib.font_manager import FontProperties
import matplotlib as mpl
import os

#读取地图数据和疫情数据
street_gdf = gpd.read_file(r"szstreet.gpkg")
district_gdf = gpd.read_file(r"szdistrict.gpkg")
szdata = pd.read_excel(r'szdata3.xlsx',index_col=0)
os.mkdir("pic")

#字体
font = FontProperties(fname='C:/Windows/Fonts/simkai.ttf',size=20)
sfont = FontProperties(fname='C:/Windows/Fonts/simkai.ttf',size=15)

#颜色
cm = (mpl.colors.ListedColormap(['white', 'orange']))

#只保留有用的数据
data = szdata.iloc[:193,[0,3,4,5,6,7]]
data['date'] = data['date'] % 10000
data = data.sort_index(ascending=False)
data["total"] = data["确诊"]+data["无症状"]

#绘图程序
def draw(index):
    day = data.iat[index,0]
    
    street_gdf["level"] = 0
    for t in street_gdf.index:
        name = street_gdf.at[t,"name"]
        if name in eval(data[data["date"]==day].iat[0,5]):
            street_gdf.at[t,"level"] = 1
    
    a = day // 100
    b = day % 100
    c = data[data["date"]==day].iat[0,1]
    d = data[data["date"]==day].iat[0,2]
    e = data[data["date"]==day].iat[0,3]
    f = data[data["date"]==day].iat[0,4]
    
    date_x = list(map(str,data["date"]))
    date_xtick = ["4月15日","5月15日","6月15日","7月15日","8月15日","9月15日","10月15日"]
    counts = data["total"]
    
    date2 = date_x[:index+1]
    counts2 = counts[:index+1]
    
    fig = plt.figure(figsize=(10,5.625))
    ax1 = fig.add_subplot(4,1,(1,3))
    ax2 = fig.add_subplot(4,1,4)
    
    ax1.set_axis_off()
    ax1.set_title("深圳市新冠疫情每日变化（2022年4月15日-10月24日）",fontproperties=font)
    ax1.text(114.45,22.81,"   {:>2}月{:>2}日".format(a,b),fontproperties=sfont)
    ax1.text(114.45,22.78,"   高风险区 {}".format(e),fontproperties=sfont)
    ax1.text(114.45,22.75,"   中风险区 {}".format(f),fontproperties=sfont)
    ax1.text(114.45,22.71,"   新增确诊 {}".format(c),fontproperties=sfont)
    ax1.text(114.45,22.68," 新增无症状 {}".format(d),fontproperties=sfont)
    ax1.text(113.99,22.47,"注：橙色为中高风险区所在街道",fontproperties=sfont)
    street_gdf.plot(ax=ax1,k=2,cmap=cm,edgecolor='grey',linewidth=1,column="level")
    district_gdf.plot(ax=ax1,edgecolor='k',linewidth=2)
    
    ax2.plot(date_x, counts)
    ax2.spines["top"].set_visible(False)
    ax2.spines["right"].set_visible(False)
    ax2.spines["left"].set_visible(False)
    ax2.patch.set_alpha(0)
    ax2.set_xticks(["415","515","615","715","815","915","1015"],date_xtick)
    ax2.tick_params(direction="in")
    ax2.set_yticks([20,40,60,80])
    ax2.set_ylim(0,90)
    ax2.grid(axis="y")
    ax2.set_xlim(("415","1023"))
    plt.rcParams['font.family'] = ['sans-serif']
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.tick_params(labelsize=12)
    ax2.plot(date2,counts2,"-r")
    
    fig.subplots_adjust(hspace=-0.5)
    fig.savefig("pic/sz{:0>4}.png".format(day),dpi=300)
    #plt.show()

#draw(100)
    
for z in range(193):
    draw(z)