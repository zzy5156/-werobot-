#!/usr/bin/python 
# -- coding: utf-8 --
import sys 
reload(sys) 
sys.setdefaultencoding('utf8')
import datetime
import requests
import json
import time
def sleeptime(hour,min,sec):
    return hour*3600 + min*60 + sec;
second = sleeptime(0,30,0);#30分钟刷新一次
def get_access_token():
    """
    获取微信全局接口的凭证(默认有效期俩个小时)
    如果不每天请求次数过多, 通过设置缓存即可
    """
    result = requests.get(
        url="https://api.weixin.qq.com/cgi-bin/token",
        params={
            "grant_type": "client_credential",
            "appid": "输入你的公众号appid",
            "secret": "输入你的公众号的appid_secret",
        }
    ).json()

    if result.get("access_token"):
        access_token = result.get('access_token')
    else:
        access_token = None
    return access_token

def sendmsg(openid,msg):

    access_token = get_access_token()

    body = {
        "touser": openid,
        "template_id":"输入你的模板id",
        "url":"www.baidu.com",
        "data": {
            "weather":{
            "value": msg,
            "color":"#173177"
           }
        }
    }
    response = requests.post(
        url="https://api.weixin.qq.com/cgi-bin/message/template/send?access_token="+access_token,
        
        data=bytes(json.dumps(body, ensure_ascii=False))
    )
    # 这里可根据回执code进行判定是否发送成功(也可以根据code根据错误信息)
    result = response.json()
    print(result)
while True: 
    json_text = requests.get(str.format("https://api.caiyunapp.com/v2/输入你的api/输入查询地方的经纬度/minutely.json")).content
    self_realtime_data = json.loads(json_text)
    now_data=self_realtime_data['result']['forecast_keypoint']
    print ("降雨预报："+now_data)
    nowTime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print ("更新于："+nowTime)
    send_data="\n"+now_data+"\n更新于："+nowTime
    if __name__ == '__main__':
        sendmsg('输入接收信息的id',send_data)
    time.sleep(second);

