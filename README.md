baymax
========

Build your personal life database, including of internet, taxi, sports and health data analysis.

[![repo](http://ohmyrepo.ml/static/ohmyrepo.png)](http://ohmyrepo.ml/show?u=no13bus&r=baymax)

[中文文档](https://github.com/no13bus/baymax/blob/master/README_CN.md)

# Let's start
- pip install -r requirements.txt
- Modify the config file, such as celery, MySQL configuration, APP callback address and apps' client_id.
- python manage.py initdb
- python manage.py insert
- python manage.py run

# Deployment
- 使用nginx+gunicorn+supervisor

# Which app we support now
- [GitHub](http://github.com)
- [Health App: Fitbit](https://dev.fitbit.com)
- [rescuetime](https://www.rescuetime.com/developers)

# Which app we will support
- [ledongli](http://ledongli.cn)
- [bong](http://www.bong.cn/)
- [xiaomi](http://www.mi.com/shouhuan)
- [Nike+](https://developer.nike.com/index.html)
- [Moves](https://dev.moves-app.com/)
- [Withings](http://oauth.withings.com/api)
- [Uber](http://uber.com)
- ..............

# Mechanism
- Users first use GitHub account to sign in, after we get the authentication for the apps, 
the backend will to grab the app life data every day.
- And then baymax will display the life data, including of walking, running, surfing the net time distribution, 
GitHub code submitted times and statistics.


# The tech we use
- Flask
- sqlalchemy
- Bootstrap
- celery
- redis


# 截图
![1](https://raw.githubusercontent.com/no13bus/baymax/master/screen/1.png)
![2](https://raw.githubusercontent.com/no13bus/baymax/master/screen/2.png)
![3](https://raw.githubusercontent.com/no13bus/baymax/master/screen/3.png)
![4](https://raw.githubusercontent.com/no13bus/baymax/master/screen/4.png)
![5](https://raw.githubusercontent.com/no13bus/baymax/master/screen/5.png)
![6](https://raw.githubusercontent.com/no13bus/baymax/master/screen/6.png)
![7](https://raw.githubusercontent.com/no13bus/baymax/master/screen/7.png)