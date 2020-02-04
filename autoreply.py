#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys

from werobot.client import Client

reload(sys) 
sys.setdefaultencoding('utf8')
import datetime
import json
import time
import random
import requests
import re
import urllib2
import werobot
# 下面进入你的测试公众号后台查找对应信息
robot=werobot.WeRoBot(token='#此处输入你自定义的token')
robot.config['APP_SECRET'] = '#此处输入你的APP_SECRET'
robot.config['APP_ID'] = '#此处输入你的APP_ID'
client = robot.client

@robot.filter('明天天气')
def test(message,session):
    session['last'] = True
    return '请发送要查询的位置'


@robot.filter('微博')
def weibo():
    # 将url的地址进行更改即可查找其他用户的微博
    url = "https://m.weibo.cn/api/container/getIndex?uid=2015316631&t=0&luicode=10000011&lfid=100103type%3D1%26q%3D%E5%B9%BF%E4%B8%9C%E5%A4%A9%E6%B0%94&type=uid&value=2015316631&containerid=1076032015316631"
    data = requests.get(url)
    data_text = data.text
    data_num = re.findall(r'\"mid\"\:\"(\d{16})\"', data_text)
    url_0 = "https://m.weibo.cn/detail/" + data_num[0]
    url_1 = "https://m.weibo.cn/detail/" + data_num[1]
    print(url_0)
    send_data = "广东天气最近发布的两条微博为：\n" + url_0 + "\n" + url_1
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
    send_data="今天是"+str(date)+" 星期"+str(week)+"\n农历"+str(lunar)+"\n宜："+str(suit)+"\n忌："+str(avoid)
    return send_data

@robot.location
def place(message,session):
    # 请确保你有能用的彩云天气令牌以及心知天气的令牌(可以去对应官网申请)
    place=message.location
    place_1 = ":".join([str(i) for i in place])
    place_2 = str(place[1]) + "," + str(place[0])
    print (place_2)
    if session['last'] == True:
        session['last'] = False
        # 记得更改此处的彩云天气令牌
        data = json.loads(
            requests.get(
                str.format("https://api.caiyunapp.com/v2/#此处输入你的彩云天气令牌/" + place_2 + "/weather.json")).content)
        status = data['status']
        print(status)
        if status == 'ok':
            hours = data['result']['hourly'][u'description']
            daily_temp_max = data['result']['daily']['temperature'][1][u'max']
            daily_temp_avg = data['result']['daily']['temperature'][1][u'avg']
            daily_temp_min = data['result']['daily']['temperature'][1][u'min']
            wea = data['result']['daily']['skycon'][1]['value']
            if wea == 'CLEAR_DAY' or wea == 'CLEAR_NIGHT':
                wea = "晴"
            elif wea == 'PARTLY_CLOUDY_DAY' or wea == 'PARTLY_CLOUDY_NIGHT':
                wea = "多云"
            elif wea == 'CLOUDY':
                wea = "阴"
            elif wea == 'WIND':
                wea = "大风"
            elif wea == 'HAZE':
                wea = "雾霾"
            elif wea == 'RAIN':
                wea = "雨"
            elif wea == 'SNOW':
                wea = "雪"
            print(wea)
            r_data = "经纬度：[" + str(place_2) +"]\n小时降雨预报：" + str(hours) + "\n明天天气：" + str(wea) + "\n最高 " +  str(daily_temp_max) + "℃ \n最低 " + str(daily_temp_min) + "℃ \n平均 " + str(daily_temp_avg) +"℃ \n数据来源：彩云科技"
            return r_data
        else:
            return "获取天气失败，可能服务器出问题了，请稍后再试"
    else:
        # 记得更改此处的彩云天气令牌
        json_text = requests.get(
            str.format("https://api.caiyunapp.com/v2/#此处输入你的彩云天气令牌/" + place_2 + "/realtime.json")).content
        data = json.loads(json_text)
        status = data['status']
        if status == 'failed':
            # 记得更改此处的心知天气令牌
            json_text = requests.get(str.format(
                "https://api.seniverse.com/v3/weather/now.json?key=#输入你的心知天气令牌&location=" + place_1 + "&language=zh-Hans&unit=c")).content
            r_data = json.loads(json_text)
            data = r_data['results'][0]
            wea = data['now']['text']
            tem = data['now']['temperature']
            location = data['location']['name']
            utime = data['last_update']
            send_data = location + "，" + wea + "，" + tem + "℃ \n更新时间：" + utime + "\n数据来源：心知天气" + "\n若想查看您所在地的天气，可访问www.caiyunapp.com/map"
            return send_data
        else:
            # 记得更改此处的彩云天气令牌
            json_text_1 = requests.get(
                str.format("https://api.caiyunapp.com/v2/#此处输入你的彩云天气令牌/" + place_2 + "/minutely.json")).content
            self_realtime_data = json.loads(json_text_1)
            now_data = self_realtime_data['result']['forecast_keypoint']
            a_place = "".join(str(data['location']))
            tem = data['result']['temperature']
            pm25 = data['result']['pm25']
            source = data['result']['precipitation']['local']['datasource']
            wea = data['result']['skycon']
            if wea == 'CLEAR_DAY' or wea == 'CLEAR_NIGHT':
                wea = "晴"
            elif wea == 'PARTLY_CLOUDY_DAY' or wea == 'PARTLY_CLOUDY_NIGHT':
                wea = "多云"
            elif wea == 'CLOUDY':
                wea = "阴"
            elif wea == 'WIND':
                wea = "大风"
            elif wea == 'HAZE':
                wea = "雾霾"
            elif wea == 'RAIN':
                wea = "雨"
            elif wea == 'SNOW':
                wea = "雪"
            send_data = "经纬度：" + a_place + "\n天气：" + wea + "\n降雨预报：" + now_data + "\n温度：" + str(
                tem) + " ℃\npm2.5：" + str(pm25) + "\n数据来源：彩云科技(" + source + ")"
            return send_data

@robot.handler
def echo(message):
    in_message = message.content
    # 此处转换会报错，本人水平不高暂时无法解决，不影响正常使用
    if  re.compile("群发*?").match(in_message.encode('utf8')):
        print message.source
        # 下面判断用于指定只有一个用户允许群发信息（如不需要可以去掉）
        if message.source == '#用户ID可以在公众号后台查看':
            users = json.dumps(client.get_followers())
            users_text = json.loads(users)
            u_openid = (users_text[u'data'])[u'openid']
            # 群发消息实例：群发 这是一条群发消息 这里是网址
            # 注意：默认设定以空格作为分割符，可在下一条语句进行修改
            send_message = in_message.encode('utf8').split(" ", 2)
            print(send_message[1])
            send_data = {"data": {"value": send_message[1]}}
            for x in u_openid:
                client.send_template_message(x, '#输入设定好的模板ID，模板内数据为data', send_data,
                                             send_message[2])
            return '已群发消息'
        else:
            return '您不能群发消息'
    else:
        return '这个并没有对应功能，但还是回复一下以免尴尬'

robot.config['HOST']='0.0.0.0'
# 这里的监听端口可自定义，前提是在服务器做好端口映射或使用反向代理，详情参考werobot API文档。微信默认监听为80
robot.config['PORT']=80
robot.run()
