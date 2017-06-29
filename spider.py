# -*-coding:utf-8-*-
__author__ = 'fyy'
from article import *
import cookielib


home_page = "https://bbs.hupu.com"


def to_page(section, number):
    if number == 1:
        return home_page+"/" + section
    return home_page+"/"+section+"-" + str(number)


def make_cookie(name, value, domain, path):
    return cookielib.Cookie(
        version=0, name=name, value=value, port=None, port_specified=False,
        domain=domain, domain_specified=True, domain_initial_dot=False,
        path=path, path_specified=True, secure=False,
        expires=None, discard=False, comment=None, comment_url=None, rest=None
    )


def hupu_login(cookie_str, path, domain, headers):
    cookie_jar = cookielib.CookieJar()
    cookie_list = cookie_str.replace("\t", "").replace(" ", "").split(";")
    for cookie in cookie_list:
        cookie_pair = cookie.split("=")
        cookie_jar.set_cookie(make_cookie(cookie_pair[0], cookie_pair[1], domain, path))
    cookie_processor = urllib2.HTTPCookieProcessor(cookie_jar)
    opener = urllib2.build_opener(cookie_processor)
    opener.addheaders = headers
    return opener


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
            author.url = author_info[0]['href'][20:]
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


def load_cookie(file_name):
    with open(file_name, "r") as f:
        cookie = f.read()
    return cookie


def get_topics_by_author(author):
    cookie_string = load_cookie("cookie")
    header = [("User-agent", "Mozilla/5.0"), ("Referer", "https://my.hupu.com/")]
    # print cookie_string
    opener = hupu_login(cookie_string, "/", ".hupu.com", header)
    response = opener.open("https://my.hupu.com/"+author+"/topic")
    doc = response.read()
    return doc


def get_articles_by_author(author_url, section):
    html_doc = get_topics_by_author(author_url)
    soup = BeautifulSoup(html_doc, "lxml")
    author_id = soup.find("h1", "t1").string[:-3]
    articles = list()
    topic_data = soup.find_all("td", class_="p_title")
    if len(topic_data):
        for topic_td in topic_data:
            article_url = topic_td.a["href"][14:]
            section_article = unicode(topic_td.next_sibling.next_sibling.string).encode("utf-8")
            if section != section_article:
                continue
            article = Article(article_url, Author(author_id, author_url), topic_td.a.string, 0)
            articles.append(article)
    return articles

# 测试获得用户url为219344802208829的用户发过的所有帖子
# result = get_articles_by_author("219344802208829", "情感区")
# for article in result:
#     content = article.get_article_content()
#     print content
# 测试完毕