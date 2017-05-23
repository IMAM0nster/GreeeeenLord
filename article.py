# -*-coding:utf-8-*-
__author__ = 'fyy'
import urllib2
from bs4 import BeautifulSoup
from bs4 import NavigableString


def get_string_of_tag(tag, without_blockquote):
    if type(tag) is NavigableString:
        return tag
    content = ""
    if without_blockquote and tag.name == "blockquote":
        return content
    for child in tag.children:
        content += get_string_of_tag(child, without_blockquote)
    return content


# 帖子的作者， 包括其主页的URL， 以及其ID
class Author:
    def __init__(self, user_id, url):
        self.url = url
        self.user_id = user_id


# 评论类，包括作者，评论所在的帖子的id暨URL，评论的具体内容，评论的对象——如果没有引用其他楼的发言，视为对楼主的回复
class Comment:
    def __init__(self, author, article_id, content, quote_origin):
        self.author = author
        self.article_id = article_id
        self.content = content
        self.quote_origin = quote_origin


# 帖子类，包括该帖子的URL，作者，标题，以及回复数量
class Article:
    def __init__(self, url, author, title, reply_num):
        self.url = url
        self.author = author
        self.title = title
        self.reply_num = reply_num

    # 请求帖子所在的html页面
    def get_html_doc(self, page):
        request_url = "https://bbs.hupu.com"+self.url
        if page != 1:
            request_url = request_url[:-5]+"-"+str(page)+request_url[-5:]
        request = urllib2.Request(request_url)
        response = urllib2.urlopen(request)
        return response.read()

    # 请求帖子的内容
    def get_article_content(self):
        html_doc = self.get_html_doc(1)
        soup = BeautifulSoup(html_doc, "lxml")
        content = ""
        floors = soup.find_all("div", class_="floor")
        if len(floors):
            content_div = floors[0].find_all("div", class_="quote-content", limit=1)
            if len(content_div):
                for child in content_div[0].children:
                    content += get_string_of_tag(child, False)
        return content

    @staticmethod
    def __get_quote(tag):
        a = tag.find("a", "u")
        author = Author("", "")
        author.url = a["href"]
        author.user_id = a.string
        return author

    # 获取评论，参数为评论的页数
    def get_comments(self, page):
        html_doc = self.get_html_doc(page)
        soup = BeautifulSoup(html_doc, "lxml")
        comment_list = list()
        if page == 1:
            w_reply = soup.find("div", "w_reply clearfix")
            if w_reply is None:
                floor = soup.find("div", "floor")
            else:
                floor = w_reply.find_next_sibling("div", "floor")
        else:
            floor = soup.find("div", "floor")
        while floor is not None:
            # get author
            a = floor.find("a", "u")
            author = Author("", "")
            author.url = a["href"]
            author.user_id = a.string
            # get content
            d = floor.find("div", "quote-content")
            content = get_string_of_tag(d, True)
            blockquote = d.find("blockquote")
            comment = Comment(author, self.url, content, self.author)
            if blockquote is not None:
                quote_origin = self.__get_quote(blockquote)
                comment.quote_origin = quote_origin
            comment_list.append(comment)
            floor = floor.find_next_sibling("div", "floor")
        return comment_list