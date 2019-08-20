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
robot=werobot.WeRoBot(token='输入微信公众号的token')

@robot.filter('天气')
def weather():
    json_text = requests.get(str.format("https://api.caiyunapp.com/v2/输入彩云天气的token/输入经纬度/minutely.json")).content
    self_realtime_data = json.loads(json_text)
    now_data=self_realtime_data['result']['forecast_keypoint']
    nowTime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    send_data="降雨预报："+now_data+"\n更新于："+nowTime
    return send_data

robot.config['HOST']='0.0.0.0'
robot.config['PORT']=80
robot.run()
