# 爬虫管理系统

### 项目所涉及的和Django相关的功能

项目的目的是为了给Django的初学者一个完整项目的参考案例，所以尽可能多的选择了初学者常用的方法处理一些问题，比如在视图的处理上选择了视图处理函数，而不是更好用的视图处理类。在参数传递上只使用了标准的POST和GET的方式传参，而没有使用url地址中提取参数的办法。该项目中主要涉及到的Django框架相关的内容有：

* Models模型字段用法，外键关系用法。 [文档](https://docs.djangoproject.com/en/1.9/topics/db/models/)

* 使用ORM进行数据库查询。 [文档](https://docs.djangoproject.com/en/1.9/topics/db/queries/)

* Urls配置文件的写法，Urls命名与反向查询。 [文档](https://docs.djangoproject.com/en/1.9/topics/http/urls/)

* Views视图处理函数。 [文档](https://docs.djangoproject.com/en/1.9/topics/http/views/)

* Templates模板。 [文档](https://docs.djangoproject.com/en/1.9/ref/templates/language/)

* 在admin站点中注册模型。 [文档](https://docs.djangoproject.com/en/1.9/ref/contrib/admin/)

* Django自带用户模块的注册和登录。 [文档](https://docs.djangoproject.com/en/1.9/topics/auth/default/)

* 对Django自带的用户模块进行拓展。 [文档](https://docs.djangoproject.com/en/1.9/topics/auth/customizing/)

* 静态文件处理。 [文档](https://docs.djangoproject.com/en/1.9/ref/contrib/staticfiles/)

* 还有一大堆其他的……


### 系统说明

* 本系统使用Python的Django框架搭建。
* 前端部分使用bootstrap。


### 运行说明

* 请参考Django官方文档[下载](https://www.djangoproject.com/download/)Django<del>1.71</del>1.9.1版。
* 请按照Django官方文档[安装](https://docs.djangoproject.com/en/1.9/intro/install/)Django。
* 如果是水果电脑。。。请额外安装[PIL](http://www.pythonware.com/products/pil/)库。
* 通过终端进入项目文件夹。
* 在终端中执行`python manage.py runserver`命令即可运行本地开发服务器。
* 在浏览器里访问`http://127.0.0.1:8000`即可查看该网站。

