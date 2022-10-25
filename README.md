# 深圳市新冠疫情数据与可视化

## 程序文件说明
1_data_fetch.py - 从深圳市卫健委网站抓取每日疫情信息发布网页，并从中提取出包含新增病例数的段落。

2_data_processing.py - 从上一步提取的段落中提取出每日本土新增确诊病例数和无症状感染者数。

3_risk_region.py.py - 从全国每日中高风险区名单中提取深圳每日中高风险区名单，并提取每日中高风险区所在街道

4_szmap.py - 获取深圳各街道、各区地理边界数据

5_draw_picture.py - 绘制深圳每日中高风险区街道分布图和每日新增病例变化曲线

6_pic_to_vedio.py - 用上一步的图片生成视频

## 数据来源
[深圳市卫健委网站](http://wjw.sz.gov.cn/) 

[全国疫情中高风险地区查询](https://covid.risk-region.ml/)

[深圳市道路交通运行指数系统](http://tocc.jtys.sz.gov.cn/#/rt/street)

