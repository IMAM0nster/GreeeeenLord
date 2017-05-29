# -*-coding:utf-8-*-
__author__ = 'fy'
from pymongo import *
from spider import *


class HoopDB:
    def __init__(self):
        self.client = MongoClient()
        self.db = self.client.test

    def insert_articles(self, articles):
        collection = self.db.test_article
        for a in articles:
            article_content = a.get_article_content()
            article_data = {"url": a.url, "title": a.title, "author_id": a.author.user_id, "author_url": a.author.url,
                            "content": article_content}
            collection.insert_one(article_data)

    def insert_comments(self, comments):
        db = self.client.test
        collection = db.test_comment
        for c in comments:
            comment_content = c.content
            comment = {"author_id": c.author.user_id, "author_url": c.author.url,
                       "article_id": c.article_id, "target_user": c.quote_origin.user_id,
                       "target_url": c.quote_origin.url,
                       "content": comment_content}
            collection.insert_one(comment)

    def get_article_content_by_url(self, url):
        collection = self.db.test_article
        return collection.find_one({"url": url})

    def get_all_comments(self):
        collection = self.db.test_comment
        result = collection.find()
        result_num = result.count()
        return result, result_num

    def get_articles_of_particular_author(self, author_id):
        collection = self.db.test_article
        return collection.find({"author_id": author_id})


def prepare_comment_data():
    hoop_articles = list()
    hoop_db = HoopDB()
    for page in range(10):
        hoop_articles.extend(index_spider("love", 1, 20))
    for hoop in hoop_articles:
        hoop_comments = hoop.get_comments(1)
        hoop_db.insert_comments(hoop_comments)
    hoop_db.insert_articles(hoop_articles)


# 将情感区前10页的帖子及其中所有帖子的第一页的评论全部爬下，并存入mongodb中，以备用于fast unfolding算法
# print "插入评论以及帖子"
# prepare_comment_data()
# print "插入完毕"
# hoop_db = HoopDB().db
# collection = hoop_db.test_comment
# comment = collection.find_one()
# print comment
# print comment["target_url"] == comment["author_url"]