# GreeeeenLord
Fyy&amp;XG&amp;WJW
#######################################################################

单机版爬虫 By Fyy 2017/5/23

#######################################################################

运行程序之前：请确保自己电脑上安装了python以及mongoDB
程序需要正确运行，还需要安装几个必须的python库， 包括 bs4，lxml，pymongo
pip install均可安装
运行前请先开启mongo DB服务
在hupudb.py中修改底部代码，运行爬虫，将数据插入mongodb
在hupudb.py中的HupuMongo类中提供了访问数据的相应接口，可根据需要修改
代码中已经包含注释
有问题群里讨论
之后我会模拟登陆状态爬取具体用户的更多发帖
并搭建分布式架构
两位可先用目前开发的对算法进行测试，运行遇到bug或者有其他需求烦请告知
算法输出结果的格式告知我之后我开始准备可视化相关的内容

以上

#######################################################################

现在利用本地cookie，伪装已登陆状态，获取指定用户发过的所有的帖子。
运行非监督学习算法时，可直接运行这个函数即时爬取数据，
也可以从mongoDB中获取相关帖子。
运行监督式学习,建议从mongodb 中获取相关帖子以及作者的互动情况

#######################################################################