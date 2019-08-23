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
    json_text = requests.get(str.format("https://api.caiyunapp.com/v2/输入你的彩云api_token/输入经纬度/minutely.json")).content
    self_realtime_data = json.loads(json_text)
    status=self_realtime_data['status']
    if status!='failed':
        now_data=self_realtime_data['result']['forecast_keypoint']
        nowTime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        send_data="降雨预报："+now_data+"\n更新于："+nowTime+"\n数据来源：彩云科技\n详情请访问www.caiyunapp.com/map"
    else:
        send_data="彩云API已经到配额上限，无法查询。\n可访问www.caiyunapp.com/map查看天气。"
    return send_data

@robot.filter('今天')
def today():
    nowTime=datetime.datetime.now().strftime('%Y%m%d')
    json_text = requests.get(str.format("http://www.mxnzp.com/api/holiday/single/"+nowTime)).content
    data = json.loads(json_text)
    date=data['data']['date']
    week=str(data['data']['weekDay'])
    lunar=data['data']['lunarCalendar']
    avoid=data['data']['avoid']
    suit=data['data']['suit']
    dayofyear=data['data']['dayOfYear']
    weekofyear=data['data']['weekOfYear']
    send_data="今天是"+date+" 星期"+week+"\n农历"+lunar+"\n宜："+suit+"\n忌："+avoid
    return send_data

@robot.location
def place(message,location):
    place=message.location
    place_1=":".join([str(i) for i in place])
    place_2=str(place[1])+","+str(place[0])
    print (place_2)
    json_text = requests.get(str.format("https://api.caiyunapp.com/v2/输入你的彩云api_token/"+place_2+"/realtime.json")).content
    data = json.loads(json_text)
    status=data['status']
    if status=='failed':
        json_text = requests.get(str.format("https://api.seniverse.com/v3/weather/now.json?key=输入你的心知api_token&location="+place_1+"&language=zh-Hans&unit=c")).content
        r_data = json.loads(json_text)
        data=r_data['results'][0]
        wea=data['now']['text']
        tem=data['now']['temperature']
        location=data['location']['name']
        utime=data['last_update']
        send_data=location+"，"+wea+"，"+tem+"℃ \n更新时间："+utime+"\n数据来源：心知天气"+"\n若想查看您所在地的天气，可访问www.caiyunapp.com/map"
        return send_data
    else:
        json_text_1 = requests.get(str.format("https://api.caiyunapp.com/v2/输入你的彩云api_token/"+place_2+"/minutely.json")).content
        self_realtime_data = json.loads(json_text_1)
        now_data=self_realtime_data['result']['forecast_keypoint']
        a_place="".join(str(data['location']))
        tem=data['result']['temperature']
        pm25=data['result']['pm25']
        source=data['result']['precipitation']['local']['datasource']
        wea=data['result']['skycon']
        if wea=='CLEAR_DAY' or wea=='CLEAR_NIGHT':
            wea="晴"
        elif wea=='PARTLY_CLOUDY_DAY' or wea=='PARTLY_CLOUDY_NIGHT':
            wea="多云"
        elif wea=='CLOUDY':
            wea="阴"
        elif wea=='WIND':
            wea="大风"
        elif wea=='HAZE':
            wea="雾霾"
        elif wea=='RAIN':
            wea="雨"
        elif wea=='SNOW':
            wea="雪"
        send_data="经纬度："+a_place+"\n天气："+wea+"\n降雨预报："+now_data+"\n温度："+str(tem)+" ℃\npm2.5："+str(pm25)+"\n数据来源：彩云科技("+source+")"
        return send_data

robot.config['HOST']='0.0.0.0'
robot.config['PORT']=80
robot.run()
