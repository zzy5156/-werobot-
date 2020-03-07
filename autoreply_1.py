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
import sqlite3
import thread
import urllib2
import werobot
from werobot.session.sqlitestorage import SQLiteStorage
# 这是设置werobot数据库文件名，如无特殊需求不用改
session_storage = SQLiteStorage(filename='werobot_session_1.sqlite3')
# token是自定义的，在微信公众号后台设置
robot = werobot.WeRoBot(token='这里输入你的token', enable_session=True, session_storage=session_storage)
# app_secret和app_id均可在微信公众号后台获得
robot.config['APP_SECRET'] = '这里输入你的app_secret'
robot.config['APP_ID'] = '这里输入你的app_id'
client = robot.client


@robot.unknown_event
def finished():
    return "unknow"


@robot.filter('关闭定时发送天气')
def disable_auto(message, session):
    if 'auto' in session and session['auto'] == True:
        session['auto'] = False
        return "已关闭定时发送天气"
    else:
        return "您尚未启用定时发送天气，无需执行此操作"


@robot.filter('帮助')
def help():
    return "这是新坑，还没填"


@robot.filter('测试')
def test(message, session):
    send_data = ""
    # 这里的文件名与最上面的一致（虽说也没用来着）
    conn = sqlite3.connect('./werobot_session_2.sqlite3')
    cur = conn.cursor()
    row_data = cur.execute("SELECT * FROM WeRoBot")
    for row in row_data:
        status = 'No'
        details = json.loads(row[1])
        if 'test' in details:
            status = 'yes'
        send_data += row[0] + " " + str(details['set']) + "\n" + str(status)
    return "恭喜你发现了测试后遗留关键词，不过这个关键词对应的只有这条回复而已"


@robot.filter('设置位置')
def set_location(message,session):
    session['set'] = True
    return '请发送用于接收定时推送的位置'


@robot.filter('明天天气')
def test(message,session):
    session['last'] = True
    return '请发送要查询的位置'


@robot.filter('启用定时发送天气')
def start_auto_send(message, session):
    if 'had_set_location' in session:
        if session['had_set_location'] == True:
            session['auto'] = True
            return "已启用定时发送，每小时推送一次实时天气"
        else:
            return "未设置默认位置，请先发送“设置位置”按指示设置默认位置再试"
    else:
        session['had_set_location'] = False
        return "未设置默认位置，请先发送“设置位置”按指示设置默认位置再试"


@robot.filter('微博')
def weibo():
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
    place=message.location
    place_1 = ":".join([str(i) for i in place])
    place_2 = str(place[1]) + "," + str(place[0])
    print (place_2)
    if 'last' in session:
        print "has last"
    else:
        session['last'] = False
    if 'set' in session:
        print "not set"
    else:
        session['set'] = False
        session['had_set_location'] = False
    if session['set'] == True:
        session['d_location_1'] = place_1
        session['d_location_2'] = place_2
        session['had_set_location'] = True
        session['set'] = False
        return '设置成功'
    if session['last'] == True:
        session['last'] = False
        send_data = get_tomorrow_weather(place_2)
        return send_data
    else:
        send_data = get_now_weather(place_1, place_2)
        return send_data


@robot.handler
def echo(message):
    in_message = message.content
    if re.compile("群发.*?").match(in_message.encode('utf8')):
        print message.source
        # 默认只允许一个用户拥有群发权限，用户id可以在公众号后台看到
        if message.source == '请输入管理员id':
            u_openid = get_u_openid()
            send_message = in_message.encode('utf8').split(" ", 2)
            print(send_message[1])
            send_data = {"data": {"value": send_message[1]}}
            for x in u_openid:
                # 模板id在公众号后台获取。记得模板内必须包含data.DATA
                client.send_template_message(x, '请输入模板id', send_data,
                                             send_message[2])
            return '已群发消息'
        else:
            return '您不能群发消息'
    else:
        return '这个并没有对应功能，但还是回复一下以免尴尬'


@robot.subscribe
def subscribe(message, session):
    send_message = '欢迎关注此公众号\n此公众号目前的功能有：\n查询指定位置的今天/明天天气\n定时发送实时天气'
    session['d_location_1'] = False
    session['d_location_2'] = False
    session['set'] = False
    session['last'] = False
    session['had_set_location'] = False
    session['auto'] = False
    return send_message


def auto():
    last_hour = '25'
    while True:
        o_hour = time.strftime('%H',time.localtime(time.time()))
        o_min = time.strftime('%M', time.localtime(time.time()))
        print str(o_hour) + ":" + str(o_min) + " /" + str(last_hour)
        if o_min == '00' and int(o_hour) != int(last_hour):
            # 这里的文件名与最上面的一致
            conn = sqlite3.connect('./werobot_session_1.sqlite3')
            cur = conn.cursor()
            row_data = cur.execute("SELECT * FROM WeRoBot")
            for row in row_data:
                details = json.loads(row[1])
                if 'auto' in details and details['auto'] == True:
                    send_data = {"data": {
                        "value": (get_now_weather(str(details['d_location_1']), str(details['d_location_2']))).encode(
                            'utf8')}}
                    # 模板id在公众号后台获取。记得模板内必须包含data.DATA
                    status = client.send_template_message(str(row[0]),
                                                          '这里输入模板id', send_data,
                                                          "www.caiyunapp.com/map")
                    print(status)
            last_hour = o_hour
        time.sleep(45)


def get_tomorrow_weather(place_2):
    # 彩云天气api令牌请自行申请
    data = json.loads(
        requests.get(
            str.format("https://api.caiyunapp.com/v2/输入你的彩云天气api的令牌/" + place_2 + "/weather.json")).content)
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
        r_data = "经纬度：[" + str(place_2) + "]\n小时降雨预报：" + str(hours) + "\n明天天气：" + str(wea) + "\n最高 " + str(
            daily_temp_max) + "℃ \n最低 " + str(daily_temp_min) + "℃ \n平均 " + str(daily_temp_avg) + "℃ \n数据来源：彩云科技"
        return r_data
    else:
        return "获取天气失败，可能服务器出问题了，请稍后再试"


def get_now_weather(place_1, place_2):
    # 彩云天气api令牌请自行申请
    json_text = requests.get(
        str.format("https://api.caiyunapp.com/v2/输入你的彩云天气api的令牌/" + place_2 + "/realtime.json")).content
    data = json.loads(json_text)
    status = data['status']
    if status == 'failed':
        # 心知天气的api请自行申请
        json_text = requests.get(str.format(
            "https://api.seniverse.com/v3/weather/now.json?key=请输入你的心知天气api的token&location=" + place_1 + "&language=zh-Hans&unit=c")).content
        r_data = json.loads(json_text)
        data = r_data['results'][0]
        wea = data['now']['text']
        tem = data['now']['temperature']
        location = data['location']['name']
        utime = data['last_update']
        send_data = location + "，" + wea + "，" + tem + "℃ \n更新时间：" + utime + "\n数据来源：心知天气" + "\n若想查看您所在地的天气，可访问www.caiyunapp.com/map"
        return send_data
    else:
        # 彩云天气api令牌请自行申请
        json_text_1 = requests.get(
            str.format("https://api.caiyunapp.com/v2/输入你的彩云天气api的令牌/" + place_2 + "/minutely.json")).content
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


def get_u_openid():
    users = json.dumps(client.get_followers())
    users_text = json.loads(users)
    u_openid = (users_text[u'data'])[u'openid']
    return u_openid


thread.start_new_thread(auto, ())
robot.config['HOST']='0.0.0.0'
robot.config['PORT']=8080
robot.run()
