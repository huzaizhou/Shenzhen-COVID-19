# -*- coding: utf-8 -*-
#从爬到的段落中提取出确诊病例数和无症状感染者数

import re
import pandas as pd
import datetime

szdata = pd.read_excel('szdata.xlsx',index_col=0)#读取数据

szdata["确诊"] = 0
szdata["无症状"] = 0

for p in szdata.index:
    cont2 = szdata.at[p,"content"]
    e1 = r"([0-9][0-9]|[0-9])例诊断为新冠肺炎确诊病例|([0-9][0-9]|[0-9])例新冠肺炎确诊病例|新冠肺炎确诊病例([0-9][0-9]|[0-9])例|([0-9][0-9]|[0-9])例本土确诊病例|本土确诊病例([0-9][0-9]|[0-9])例|新增([0-9][0-9]|[0-9])例确诊病例"
    c1 = re.compile(e1)
    f1 = c1.findall(cont2)
    e2 = r"([0-9][0-9]|[0-9])例诊断为新冠病毒无症状感染者|([0-9][0-9]|[0-9])例新冠病毒无症状感染者|新冠病毒无症状感染者([0-9][0-9]|[0-9])例|([0-9][0-9]|[0-9])例本土无症状感染者|本土无症状感染者([0-9][0-9]|[0-9])例|新增([0-9][0-9]|[0-9])例无症状感染者([0-9][0-9]|[0-9])例"
    c2 = re.compile(e2)
    f2 = c2.findall(cont2)
    
    if len(f1) > 0:
        f1 = int(max(f1[0]))
    else:
        f1 = 0
    if len(f2) > 0:
        f2 = int(max(f2[0]))
    else:
        f2 = 0
    
    e3 = r"([0-9][0-9]|[0-9])例为无症状感染者转确诊"
    c3 = re.compile(e3)
    f3 = c3.findall(cont2)
    
    if len(f3) > 0:
        f3 = int(f3[0])
        f1 = f1 - f3
    
    if "均无症状感染者转确诊" in cont2:
        f2 = 0
    
    szdata.at[p,"确诊"] = f1
    szdata.at[p,"无症状"] = f2
    
    e4 = r"(\w\w\w\w)年(\w\w|\w)月(\w\w|\w)日"
    c4 = re.compile(e4)
    date_o = szdata.at[p,"date"]
    date_l = list(map(int, c4.findall(date_o)[0]))
    date_f = (datetime.date(date_l[0],date_l[1],date_l[2])+datetime.timedelta(days=-1)).strftime("%Y%m%d")
    szdata.at[p,"date"] = date_f

#补全缺失数据
szdata.at[11,"确诊"] = 21
szdata.at[11,"无症状"] = 11

szdata.to_excel('szdata2.xlsx')#保存为szdata2.xlsx