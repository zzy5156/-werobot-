#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys 
reload(sys) 
sys.setdefaultencoding('utf8')
import datetime
import json
import time
import random
import requests
import werobot
robot=werobot.WeRoBot(token='ziyun')

@robot.filter('天气')
def weather():
    json_text = requests.get(str.format("https://api.caiyunapp.com/v2/输入你的彩云天气api_token/输入经纬度/minutely.json")).content
    self_realtime_data = json.loads(json_text)
    status=self_realtime_data['status']
    if status!='failed':
        now_data=self_realtime_data['result']['forecast_keypoint']
        nowTime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        send_data="降雨预报："+now_data+"\n更新于："+nowTime+"\n详情请访问www.caiyunapp.com/map"
    else:
        send_data="彩云API已经到配额上限，无法查询。\n可访问www.caiyunapp.com/map查看天气。"
    return send_data

@robot.location
def place(message,location):
    place=message.location
    n_place=":".join([str(i) for i in place])
    print (n_place)
    json_text = requests.get(str.format("https://api.seniverse.com/v3/weather/now.json?key=输入你的心知天气api_token&location="+n_place+"&language=zh-Hans&unit=c")).content
    r_data = json.loads(json_text)
    data=r_data['results'][0]
    wea=data['now']['text']
    tem=data['now']['temperature']
    location=data['location']['name']
    utime=data['last_update']
    send_data=location+"，"+wea+"，"+tem+"℃ \n更新时间："+utime+"\n数据来源：心知天气"+"\n若想查看您所在地的天气，可访问www.caiyunapp.com/map"
    return send_data

robot.config['HOST']='0.0.0.0'
robot.config['PORT']=80
robot.run()
