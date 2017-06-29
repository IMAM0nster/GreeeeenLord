# -*-coding:utf-8-*-
__author__ = 'fy'
from pymongo import *
from spider import *
import time
import threading


class HoopDB:
    def __init__(self):
        self.client = MongoClient()
        self.db = self.client.test

    def insert_articles(self, articles):
        collection = self.db.article
        for a in articles:
            article_content = a.get_article_content()
            # if len(article_content) < 20:
            #     return
            article_data = {"url": a.url, "title": a.title, "author_id": a.author.user_id, "author_url": a.author.url,
                            "content": article_content}
            collection.insert_one(article_data)

    def insert_comments(self, comments):
        collection = self.db.comment
        for c in comments:
            comment_content = c.content
            if len(comment_content) < 10:
                return
            comment = {"author_id": c.author.user_id, "author_url": c.author.url,
                       "article_id": c.article_id, "target_user": c.quote_origin.user_id,
                       "target_url": c.quote_origin.url,
                       "content": comment_content}
            collection.insert_one(comment)

    def get_article_content_by_url(self, url):
        collection = self.db.article
        return collection.find_one({"url": url})

    def get_all_comments(self):
        collection = self.db.comment
        result = collection.find()
        result_num = result.count()
        return result, result_num

    def get_articles_of_particular_author(self, author_id):
        collection = self.db.article
        return collection.find({"author_id": author_id})


# section为板块，page 为页数， number 为帖子数上限, comment_num为评论页数
def prepare_comment_data(section, start_page, end_page, number, comment_num):
    # hoop_articles = list()
    hoop_db = HoopDB()
    for page in range(start_page, end_page):
        time.sleep(1)
        print "获取第", page, "页"
        hoop_articles = index_spider(section, page, number)
        hoop_db.insert_articles(hoop_articles)
        for hoop in hoop_articles:
            hoop_comments = hoop.get_comments(comment_num)
            hoop_db.insert_comments(hoop_comments)



# 将情感区前100页的帖子及其中所有帖子的第一页的评论全部爬下
# 并存入mongodb中，以备用于fast unfolding算法
# print "插入评论以及帖子"
# prepare_comment_data("love-postdate", 1, 101, 40, 1)
# print "插入完毕"
# hoop_db = HoopDB().db
# collection = hoop_db.comment
# comment = collection.find_one()
# print comment
# print comment["target_url"] == comment["author_url"]


h = HoopDB().db
collection = h.test
# comment = collection.find_one({"target_user": "白带拌香菜"})
# print comment["target_url"]
collection.find_one_and_update({"a": 1}, {"$set": {"b": 3}})