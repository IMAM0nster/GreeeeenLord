####################################################################### 

GreeeeenLord
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

用法:将自己的hupu的cookie放在名为cookie的文件中
并与spider.py同一个文件夹下,

#######################################################################

社区发现 （fast unfolding) By Fyy 2017/5/28

#######################################################################

WARNING:尚未测试过程序的正确性，谨慎运行！
运行程序前请安装networkx以及matplotlib分别用于网络的管理以及绘制

reference:

http://networkx.readthedocs.io/en/networkx-1.11/overview.html
http://blog.csdn.net/google19890102/article/details/48660239
https://arxiv.org/pdf/0803.0476.pdf
#######################################################################

bug已修复，算法应该没什么问题
可视化效果不行！

#######################################################################
