baymax
========

搭建自己的个人生活数据库-大白，数据包括上网，打车，运动，身体健康指标统计等等。

[![repo](http://ohmyrepo.ml/static/ohmyrepo.png)](http://ohmyrepo.ml/show?u=no13bus&r=baymax)

# 开始
- pip install -r requirements.txt
- 修改baymax中的config中的相关配置，比如celery的配置，mysql数据库的配置，APP回调地址的配置
- 在相关APP的api申请网址中注册自己的应用和回调地址等，并将其key secret更新到config.py文件中
- `python manage.py initdb`
- `python manage.py insert`
- `python manage.py run`
- 开启celery队列: `celery worker -A manage.celery -l info -P gevent -c 10`
- 开启定时任务: `celery -A manage.celery beat`

# 部署
- 使用nginx+gunicorn+supervisor进行部署
- `gunicorn -b 0.0.0.0:6666 -w 2 manage:app`

# 目前支持的数据提供方
- [GitHub](http://github.com)
- [健康应用: Fitbit](https://dev.fitbit.com)
- [上网时间数据分析神器: rescuetime](https://www.rescuetime.com/developers)

# 将要支持的数据提供方
- [乐动力](http://ledongli.cn)
- [bong](http://www.bong.cn/)
- [小米手环](http://www.mi.com/shouhuan)
- [Nike+](https://developer.nike.com/index.html)
- [Moves](https://dev.moves-app.com/)
- [Withings](http://oauth.withings.com/api)
- [Uber](http://uber.com)
- ..............

# 原理
- 用户首先使用GitHub登录项目，在项目中对相关的APP进行权限认证后，网站后台会每天定时抓取用户的该认证APP上面的数据， 比如Fitbit。
- 然后网站会对用户的走路，跑步，上网时间分布，github代码提交次数进行生活，工作，coding的统计和展示。


# 使用到的技术
- Flask
- sqlalchemy
- Bootstrap
- celery
- redis

# Fork
欢迎大家fok，因为有些智能硬件本人没有，一些智能硬件的api接口申请不到。如果你碰巧这2者都有的话，欢迎为项目增砖添瓦，
将接口放至于libs文件夹内。
目前知道的Nike的接口必须是需要nike的合作方才能申请到。小米手环没有api, 需要hack。bong和乐动力有接口，但是需要提交申请
材料才能拿到接口权限。
打车应用中只有Uber有api接口，国内的APP为无。

# 关于
- 我一直坚信科技，技术是要为更加便捷，高效的生活所服务的。一切能提高生活效率和改善生活状态的事物都是极具活力的。
- 项目开始的起因是因为现在智能穿戴设备的兴起以及越来越多的健康类应用的爆发。后来想到了一个人生活在社会中，身处于信息爆发的时代，
借助公共的API接口或者Hack，个人生活，工作，coding的数据现在是可以有迹可循的，目前缺乏的就是如何整合他们的数据，并且以一个相对流畅的方式展示出来。然后这就是
这个项目的起因。
- 开源的目的一方面是因为大家对数据私密的敏感性，如果觉得不ok，可以自己拿去搭建自己的生活数据库。另一方面主要是因为硬件设备的限制，
因为个人没有那么多的硬件产品(目前只有个手机)，大家fork之后的话可以借助手中的硬件去hack，调试，开发libs库，进而扩充整个生活API。

# 截图
![1](https://raw.githubusercontent.com/no13bus/baymax/master/screen/1.png)
![2](https://raw.githubusercontent.com/no13bus/baymax/master/screen/2.png)
![3](https://raw.githubusercontent.com/no13bus/baymax/master/screen/3.png)
![4](https://raw.githubusercontent.com/no13bus/baymax/master/screen/4.png)
![5](https://raw.githubusercontent.com/no13bus/baymax/master/screen/5.png)
![6](https://raw.githubusercontent.com/no13bus/baymax/master/screen/6.png)
![7](https://raw.githubusercontent.com/no13bus/baymax/master/screen/7.png)
