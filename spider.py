# -*-coding:utf-8-*-
__author__ = 'fyy'
from article import *


home_page = "https://bbs.hupu.com"


def to_page(section, number):
    if number == 1:
        return home_page+"/" + section
    return home_page+"/"+section+"-" + str(number)


# 爬取虎扑某个板块某页的所有帖子的信息，并存入表中返回
# section 为 string 类型，如"bxj","love"
# page 为页码
# number 为爬取的帖子的数量上限
def index_spider(section, page, number):
    articles = list()
    request = urllib2.Request(to_page(section, page))
    response = urllib2.urlopen(request)
    html_doc = response.read()
    soup = BeautifulSoup(html_doc, "lxml")
    trs = soup.find_all("tr", limit=number)
    for tr in trs:
        # get reply number
        reply = tr.select('.p_re')
        if len(reply):
            reply_and_view = reply[0].string.split("/")
            reply = int(reply_and_view[0])
        else:
            continue
        # get author information
        author = Author("", "")
        author_info = tr.select('.u')
        if len(author_info):
            author.user_id = author_info[0].string
            author.url = author_info[0]['href']
        else:
            continue
        # get title and url, and set the parameters of the article and append it to the articles list
        title = tr.a
        if title is not None:
            a = Article(title['href'], author, title.string, reply)
            articles.append(a)
    return articles

# ats = index_spider("love", 1, 11)
# for article in ats:
#     print "标题:", article.title
#     print "内容:", article.get_article_content()
#
# article = Article("/5550484.html", "", "", 0)
# print article.get_comments(1)