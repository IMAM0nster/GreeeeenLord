# -*-coding:utf-8-*-
__author__ = 'fy'
from pymongo import *
from spider import *


class Hupu_mongo:
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
        collection = db.teet_comment
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

    def get_articles_of_particular_author(self, author_id):
        collection = self.db.test_article
        return collection.find({"author_id": author_id})


hupu_articles = list()
hupu_mongo = Hupu_nongo()
# 将情感区前10页的帖子及其中所有帖子的第一页的评论全部爬下，并存入mongodb中
for page in range(10):
    hupu_articles.extend(index_spider("love", 1, 20))
for hupu in hupu_articles:
    hupu_comments = hupu.get_comments(1)
    hupu_mongo.insert_comments(hupu_comments)
hupu_mongo.insert_articles(hupu_articles)