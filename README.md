# -README
基于werobot，通过调用彩云科技api获取降水预报，并通过公众号发给用户

使用python2编写，已确认不兼容python3

获取降水预报的代码参考https://github.com/jihao/colorfulclouds-hass

定时发送的代码参考https://www.cnblogs.com/supery007/p/8136295.html

关键字回复的代码参考https://www.jianshu.com/p/1ec2ad95f599

彩云个人api申请地址http://caiyunapp.com/

心知个人api申请地址https://www.seniverse.com/

简易教程https://www.coolapk.com/feed/13419174?shareKey=Njc5ZmZiYjc0ZTYzNWQ1ZTdjZDI~&shareUid=489818&shareFrom=com.coolapk.market_9.5-beta2


autoreply.py为关键字回复,采用心知数据（已弃用，最新版本是在autoreply_1.py的基础上新增功能）

autoreply_1.py采用彩云科技数据，心知为备用数据源

caiyun.py为定时发送

可根据实际需求选择其中一个或同时运行

autoreply.py已实现功能：查询指定位置的降雨预报（直接发送位置）以及明天的天气（先发送 明天天气 ，再发送位置）、今天的宜忌（发送 今天）、广东天气最新的两条微博（发送 微博，更改查询用户需改动代码的url）、群发模板消息给所有关注了这个公众号的用户（发送 群发 消息 网址，默认只允许一个用户拥有此权限，但可以去掉此限制）
