# -*- coding: utf-8 -*-
import urllib.request
import re
import pandas as pd
import time

#打开深圳市卫健委网站“疫情信息”中的每一个页面，提取出文章标题和链接
url_list0 = ["http://wjw.sz.gov.cn/yqxx/index.html"]
for i in range(2,101):
    url_list0.append("http://wjw.sz.gov.cn/yqxx/index_{}.html".format(i))

titleList, linkList = [], []
for j in url_list0:
    #读取网页
    res = urllib.request.urlopen(j)
    page = res.read().decode("utf-8")
    page_s = str(page)
    #用正则表达式提取每一个标题所在的grid
    expr0 = r'<li>(.*?)</li>'
    grid = re.compile(expr0,re.S)
    gridList = grid.findall(page_s)
    #设定标题和链接的提取规则
    expr1 = r'title="(.*?)"'
    title0 = re.compile(expr1,re.S)
    
    expr2 = r'href="(.*?)"'
    link0 = re.compile(expr2,re.S)
    #在包含"深圳市新冠肺炎疫情情况"的grid中提取标题和链接
    for k in gridList:
        if "深圳市新冠肺炎疫情情况" in k:
            titleList.append(title0.findall(k)[0])
            linkList.append(link0.findall(k)[0])

date = list(map(lambda x: x[:-11], titleList))#只保留标题中的日期
szdata = pd.DataFrame({"date":date,"link":linkList})#放入一个DataFrame

def content(url):
    #读取每一个疫情信息网页
    response = urllib.request.urlopen(url)
    data = response.read().decode("utf-8")
    HTML = str(data)
    #提取出其中包含新增病例人数的段落
    expr3 = r'<div class="news_cont_d_wrap">(.*?)</p>'
    cont0 = re.compile(expr3,re.S)
    divsList2 = cont0.findall(HTML)
    cont1 = divsList2[0]
    cont1 = cont1.replace('</strong>',"")
    cont1 = cont1.replace('<strong>',"")
    cont1 = cont1.replace('<strong style="text-align: justify;">',"")
    cont1 = cont1.replace('<span style="text-align: justify;">',"")
    cont1 = cont1.replace('</span>',"")
    cont1 = cont1.replace('<span>',"")
    return cont1

#用content函数提取后存入szdata
szdata["content"] = ""
for n in szdata.index:
    szdata.at[n,"content"] = content(szdata.at[n,"link"])
    time.sleep(0.1)
    
szdata.to_excel('szdata.xlsx')#保存