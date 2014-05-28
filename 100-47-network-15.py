#coding=utf-8
"""
This script copies entries from a CSDN blog to an other weblog, using the MetaWeblog API.
It can move both posts and comments.
Require 'BeautifulSoup' module
Released under the GPL. Report bugs to davelv@qq.com
Thanks for ordinary author Wei Wei(live space mover)
(C) Davelv, homepage http://www.davelv.net
(C) Wei Wei,homepage: http://www.broom9.com
General Public License: http://www.gnu.org/copyleft/gpl.html
Last modified 2012-01-03 06:21
"""
__VERSION__ = "1.0"
__PROGRAM__ = "CsdnBlogMover"
import sys
import os
import codecs
import httplib
import urllib2
import re
import logging
from datetime import datetime, timedelta
import time
from optparse import OptionParser
from string import Template
import pickle
from xml.sax import saxutils
import json

from BeautifulSoup import BeautifulSoup


class IDGenerator:
    start = 0
    current = 0
    dict = {0: 0}

    def __init__(self, start):
        self.start = start
        self.current = start

    def GetID(self, key):
        if not self.dict.has_key(key):
            self.dict[key] = self.current
            self.current += 1
        return self.dict[key]


postIDGenerator = ''
commentIDGenerator = ''
csdnDatetimePattern = u'%Y-%m-%d %H:%M';
csdnHost = u'blog.csdn.net'
csdnCommentsPre = u''
http = httplib.HTTPConnection(csdnHost)
hlightdict = {"syntaxhighlight": u'<pre class="brush: \g<1>">\g<2></pre>',
              "geshi": u'<pre lang="\g<1>">\g<2></pre>'}


def GetPage(url, retryTimes=5, retryIntvl=3):
    global http
    userAgent = {u'User-Agent': u'Fiddler',
                 u'Connection': u'keep-alive'}
    while retryTimes > 0:
        try:
            logging.info("get url:" + url)
            http.request("GET", url, headers=userAgent)
            return http.getresponse().read().decode("utf8")
        except httplib.CannotSendRequest:
            logging.warning("Fetch data failure, reconnect after %ds", retryIntvl)
            http.close()
        except:
            logging.warning("Fetch data failure, retry after %ds", retryIntvl)
        finally:
            retryTimes -= 1
            if retryTimes == 0:
                raise
            time.sleep(retryIntvl)


def CheckAttachmentURL(url, attachEntrys):
    for ae in attachEntrys:
        if url == ae['url']: return False
    return True


def ProcessAttachment(articleEntry, attachEntries=[]):
    attachRe = re.compile(u'http://hi.csdn.net/attachment/[^"]+')
    attachurls = attachRe.findall(articleEntry['content'])
    for attachurl in attachurls:
        if not CheckAttachmentURL(attachurl, attachEntries):
            continue
        attachEntry = {}
        attachEntry['title'] = attachurl.split(u'/')[-1]
        attachEntry['date'] = articleEntry['date']
        attachEntry['url'] = attachurl
        attachEntry['parentId'] = articleEntry['id']
        attachEntry['id'] = postIDGenerator.GetID(attachurl)
        attachEntry['metaKey'] = u"_wp_attached_file"
        attachEntry['metaValue'] = attachEntry['title']
        attachEntry['status'] = u"inherit"
        attachEntry['type'] = u"attachment"
        attachEntry['content'] = attachEntry['comments'] = attachEntry['category'] = u''
        attachEntries.append(attachEntry)

    return


def PrettyCode(content, hlight):
    """
    Pretty code area in article content use pre to replace textarea
    surpport SyntaxHighlighter & GeSHi
    working...
    """
    textarea = re.compile(u'<textarea.+?name="code".+?class="([^"]+)">(.+?)</textarea>', re.S)
    return textarea.sub(hlightdict[hlight], content)


def PrettyComment(comment):
    quote = re.compile(u'^\[quote=([^\]]+)\](.+)\[/quote\]', re.S)
    comment = quote.sub(u'<fieldset><legend>引用 \g<1>:</legend>\g<2></fieldset>', comment)
    reply = re.compile(u'\[reply\]([^\[]+)\[/reply\]')
    return reply.sub(u'回复 \g<1>:', comment)


def ParseCommentDate(dateStr):
    #"""
    #Parse date string in comments
    #examples:
    #刚刚
    #11分钟前
    #11小时前
    #昨天 11:11
    #前天 11:11
    #3天前 11:11
    #2011-11-11 11:11
    #"""
    datetimeNow = datetime.today()
    reg_method = {
        u'\d{4}-\d{1,2}-\d{1,2} \d{1,2}:\d{1,2}': lambda m: datetime.strptime(m.group(0), csdnDatetimePattern),
        u'(\d)天前 (\d{1,2}):(\d{1,2})': lambda m: datetimeNow.replace(hour=int(m.group(2)),
                                                                     minute=int(m.group(3))) - timedelta(
            days=int(m.group(1))),
        u'前天 (\d{1,2}):(\d{1,2})': lambda m: datetimeNow.replace(hour=int(m.group(1)),
                                                                 minute=int(m.group(2))) - timedelta(days=2),
        u'昨天 (\d{1,2}):(\d{1,2})': lambda m: datetimeNow.replace(hour=int(m.group(1)),
                                                                 minute=int(m.group(2))) - timedelta(days=1),
        u'(\d{1,2})小时前': lambda m: datetimeNow - timedelta(hours=int(m.group(1))),
        u'(\d{1,2})分钟前': lambda m: datetimeNow - timedelta(minutes=int(m.group(1))),
        u'刚刚': lambda m: datetimeNow}
    for k, v in reg_method.items():
        m = re.search(k, dateStr)
        if m:
            return v(m)


def FetchEntry(url, datetimePattern='%Y-%m-%d %H:%M', isPostOnly=False):
    """
    Structure of entry
    entry
    |-title
    |-manage
    |   |-category (maybe NULL)
    |   |-date
    |   |-view' counts
    |   |-comments' counts
    |-content
    |-permalLink (permalLink of previous entry, may be NULL)
    |-comments
        |-email
        |-author
        |-comment
        |-date
    """
    temp = url.split('/')
    articleID = temp[-1]
    logging.debug("Fetch article page from %s", url)
    soup = BeautifulSoup(GetPage(url))
    #logging.debug("Got Page Content\n---------------\n%s",soup.prettify())
    item = {'title': '', 'date': '', 'content': '', 'category': [], 'prevLink': '', 'id': int(articleID),
            'comments': [],
            'parentId': 0, 'type': u'post', 'status': u'publish', 'metaKey': u'views', 'metaValue': 0}
    #find article
    article = soup.find(id="article_details")
    if article:
        logging.debug("Found article")
    else:
        logging.debug("Can't found article")
        sys.exit(2)
        #title
    temp = article.find(attrs={"class": "article_title"}).find(attrs={"class": "link_title"}).find('a')
    if temp:
        item['title'] = u'' + temp.contents[0].string
        logging.debug("Found title %s", item['title'])
    else:
        logging.warning("Can't find title")
        sys.exit(2)
        #category / date / view times / comments times
    manage = article.find(attrs={"class": "article_manage"})
    #category
    temp = manage.find(attrs={"class": "link_categories"})
    if temp:
        item['category'] = map(lambda a: u'' + a.text, temp.findAll('a'))
        categoryStr = u''
        for cate in item['category']: categoryStr += cate + u', '
        logging.debug("Found category %s", categoryStr[:-2])
        #global categories
        #categories.update(item['category'])
    else:
        logging.debug("No category, use default")
        #date
    temp = manage.find(attrs={"class": "link_postdate"})
    if temp:
        item['date'] = datetime.strptime(u'' + temp.contents[0].string, datetimePattern)
        logging.debug("Found date %s", item['date'])
    else:
        logging.warning("Can't find date")
        sys.exit(2)
        #views
    temp = manage.find(attrs={"class": "link_view"})
    if temp:
        item['metaValue'] = int(temp.contents[0][0:-3])
        logging.debug("Found views count %d", item['metaValue'])
    else:
        logging.warning("Can't find views count")
        sys.exit(2)
        #comments count
    temp = manage.find(attrs={"class": "link_comments"})
    comments_cnt = 0
    if temp:
        comments_cnt = int(temp.contents[1][1:-1])
        logging.debug("Found comments count %d", comments_cnt)
    else:
        logging.warning("Can't find comments count")
        sys.exit(2)
        #content
    temp = article.find(id="article_content") or article.find(attrs={"class": "article_content"})
    if temp:
        item['content'] = u''.join(map(unicode, temp.contents))
        logging.debug("Found content");
    else:
        logging.warning("Can't find content")

    #previous entry link
    temp = article.find('li', attrs={'class': 'prev_article'});
    if temp:
        item['prevLink'] = u'' + temp.find('a')['href']
        logging.debug("Found previous permaLink %s", item['prevLink'])
        #comments get from server
    if isPostOnly or comments_cnt == 0:
        return item
    commentsURL = csdnCommentsPre + articleID
    logging.debug("Fetch comments from %s", commentsURL)
    page = GetPage(commentsURL)
    #OMG, when I write out the parse functon by using regex
    #I found it can be solved by json ulity in one line!!!
    #{"list":[{"ArticleId":7079224,"BlogId":66847,"CommentId":2065153,"Content":"XXXX","ParentId":0,"PostTime":"昨天 11:26","Replies":null,"UserName":"evilhacker","Userface":"http://xxx.jpg"},...],...}
    item['comments'] = json.loads(page)['list']
    if item['comments'] == None:
        logging.warning("Can't find conments")
    for v in item['comments']:
        uselessPriorities = ['ArticleId', 'BlogId', 'Replies', 'Userface']
        for i in uselessPriorities: del v[i]
        v['PostTime'] = ParseCommentDate(v['PostTime'])

    return item


def FetchBlogInfo(url, needPermaLink=True):
    global csdnCommentsPre
    blogInfo = {}
    logging.info("connectiong to web page %s", url)
    body = GetPage(url)
    soup = BeautifulSoup(body)
    blogInfo['user'] = u'' + re.search(csdnHost + "/([^/]+)", url).group(1)
    blogInfo['blogURL'] = u'http://' + csdnHost + '/' + blogInfo['user'] + '/'
    csdnCommentsPre = blogInfo['blogURL'] + "comment/list/"
    logging.info('Blog URL is %s', blogInfo['blogURL'])
    blogInfo['nowTime'] = u'' + datetime.now().strftime('%a, %d %b %Y %H:%M:%S +0800')
    blogInfo['blogTitle'] = u'' + soup.find("div", {"id": "blog_title"}).h2.text
    blogInfo['blogDesc'] = u'' + soup.find(id='blog_title').h3.text
    logging.debug('Blog Title is %s', blogInfo['blogTitle'])

    if not needPermaLink:
        blogInfo["permaLink"] = url
        return blogInfo

    linkNode = soup.find(attrs={"class": "link_title"}).find('a')
    if linkNode:
        #if the linkNode is like "/davelv/article/details/6191987" concat after "http://blog.csdn.net/"
        blogInfo["permaLink"] = linkNode["href"]
    else:
        logging.error("Can't find permaLink")
    return blogInfo


def ExportHead(f, dic, categories=[]):
    t = Template(u"""<?xml version="1.0" encoding="UTF-8"?>
<!--
    This is a WordPress eXtended RSS file generated by Live Space Mover as an export of
    your blog. It contains information about your blog's posts, comments, and
    categories. You may use this file to transfer that content from one site to
    another. This file is not intended to serve as a complete backup of your
    blog.

    To import this information into a WordPress blog follow these steps:

    1.  Log into that blog as an administrator.
    2.  Go to Manage > Import in the blog's admin.
    3.  Choose "WordPress" from the list of importers.
    4.  Upload this file using the form provided on that page.
    5.  You will first be asked to map the authors in this export file to users
        on the blog. For each author, you may choose to map an existing user on
        the blog or to create a new user.
    6.  WordPress will then import each of the posts, comments, and categories
        contained in this file onto your blog.
-->

<!-- generator="{programInfo}" created="${nowTime}"-->
<rss version="2.0"
    xmlns:excerpt="http://wordpress.org/export/1.1/excerpt/"
    xmlns:content="http://purl.org/rss/1.0/modules/content/"
    xmlns:wfw="http://wellformedweb.org/CommentAPI/"
    xmlns:dc="http://purl.org/dc/elements/1.1/"
    xmlns:wp="http://wordpress.org/export/1.1/"
>

<channel>
    <title>${blogTitle}</title>
    <link>${blogURL}</link>
    <description>${blogDesc}</description>
    <pubDate>${nowTime}</pubDate>
    <generator>${programInfo}</generator>
    <language>zh</language>
    <wp:wxr_version>1.1</wp:wxr_version>""") #need blogTitle, nowTime, blogURL
    catT = Template(u'''
    <wp:category><wp:term_id>${categoryId}</wp:term_id><wp:category_nicename>${niceName}</wp:category_nicename><wp:category_parent/><wp:cat_name><![CDATA[${category}]]></wp:cat_name></wp:category>
    <wp:tag><wp:term_id>${tagId}</wp:term_id><wp:tag_slug>${niceName}</wp:tag_slug><wp:tag_name><![CDATA[${category}]]></wp:tag_name></wp:tag>''')
    catStr = u''
    i = -1
    for cat in categories:
        i = i + 2
        logging.debug("Cate:%s", cat)
        catStr += catT.substitute(
            categoryId=i,
            tagId=i + 1,
            category=cat,
            niceName=urllib2.quote(cat.encode('utf-8'))
        )
    dic['blogTitle'] = saxutils.escape(dic['blogTitle'])
    dic['programInfo'] = u'' + __PROGRAM__ + __VERSION__
    f.write(t.substitute(dic))
    f.write(catStr)


def GenerateComments(comments):
    commentT = Template(u"""
        <wp:comment>
            <wp:comment_id>${commentId}</wp:comment_id>
            <wp:comment_author><![CDATA[${commentAuthor}]]></wp:comment_author>
            <wp:comment_author_email></wp:comment_author_email>
            <wp:comment_author_url>${authorURL}</wp:comment_author_url>
            <wp:comment_author_IP></wp:comment_author_IP>
            <wp:comment_date>${commentDate}</wp:comment_date>
            <wp:comment_date_gmt>${commentDateGMT}</wp:comment_date_gmt>
            <wp:comment_content><![CDATA[${commentContent}]]></wp:comment_content>
            <wp:comment_approved>1</wp:comment_approved>
            <wp:comment_type></wp:comment_type>
            <wp:comment_parent>${parentId}</wp:comment_parent>
        </wp:comment>""") #need commentId, commentAuthor, commentEmail, commentURL,commentDate,commentContent
    commentsStr = u""
    #logging.debug(entry)
    for comment in comments:
        commentsStr += commentT.substitute(
            commentId=comment['CommentId'],
            commentAuthor=saxutils.escape(comment['UserName']),
            authorURL=u'http://' + csdnHost + u'/' + saxutils.escape(comment['UserName']),
            commentDate=comment['PostTime'].strftime('%Y-%m-%d %H:%M:%S'),
            commentDateGMT=(comment['PostTime'] - timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S'),
            commentContent=comment['Content'],
            parentId=comment['ParentId'])
        #logging.debug(comment['comment'])
    return commentsStr


def GeneratePostCategories(categories):
    cateT = Template(u"""
        <category domain="category" nicename="${niceName}"><![CDATA[${category}]]></category>
        <category domain="post_tag" nicename="${niceName}"><![CDATA[${category}]]></category>""")#nedd category niceName
    #category
    categoryStr = u''
    for cate in categories:
        categoryStr += cateT.substitute(
            category=cate,
            niceName=urllib2.quote(cate.encode('utf-8')))
    return categoryStr


def GenerateMeta(key, value):
    metaT = Template(u"""
            <wp:meta_key>${metaKey}</wp:meta_key>
            <wp:meta_value><![CDATA[${metaValue}]]></wp:meta_value>
            """)
    metaStr = metaT.substitute(metaKey=key, metaValue=value)
    return metaStr


def GenerateAttatchmentURL(url):
    return u"\n        <wp:attachment_url>" + url + u"</wp:attachment_url>"


def ExportEntry(f, entry, user):
    itemT = Template(u"""
    <item>
        <title>${entryTitle}</title>
        <link>${entryURL}</link>
        <pubDate>${pubDate}</pubDate>
        <dc:creator>${entryAuthor}</dc:creator>${categories}
        <guid isPermaLink="false"></guid>
        <description></description>
        <content:encoded><![CDATA[${entryContent}]]></content:encoded>
        <wp:post_id>${entryId}</wp:post_id>
        <wp:post_date>${postDate}</wp:post_date>
        <wp:post_date_gmt>${postDateGMT}</wp:post_date_gmt>
        <wp:comment_status>open</wp:comment_status>
        <wp:ping_status>open</wp:ping_status>
        <wp:post_name>${postName}</wp:post_name>
        <wp:status>${status}</wp:status>
        <wp:post_parent>${parentId}</wp:post_parent>
        <wp:menu_order>0</wp:menu_order>
        <wp:post_type>${type}</wp:post_type>${attachmentURL}
        <wp:postmeta>${postMeta}</wp:postmeta>${comments}
    </item>""") #need entryTitle, entryURL, entryAuthor, category, entryContent, entryId, postDate,postDateGMT, pubDate,views

    #logging.debug(entry['category'])

    itemStr = itemT.substitute(
        entryURL='',
        entryAuthor=user,
        entryId=entry['id'],
        entryContent=entry['content'],
        status=entry['status'],
        parentId=entry['parentId'],
        type=entry['type'],
        entryTitle=saxutils.escape(entry['title']),
        postName=urllib2.quote(entry['title'].encode('utf-8')),
        postDate=entry['date'].strftime('%Y-%m-%d %H:%M:%S'),
        pubDate=entry['date'].strftime('%a, %d %b %Y %H:%M:%S +0800'),
        postDateGMT=(entry['date'] - timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S'),
        comments=GenerateComments(entry['comments']),
        categories=GeneratePostCategories(entry['category']),
        postMeta=GenerateMeta(entry['metaKey'], entry['metaValue']),
        attachmentURL=u'' if not entry.has_key('url') else GenerateAttatchmentURL(entry['url'])
    )

    #logging.debug(itemStr)
    f.write(itemStr)


def ExportFoot(f):
    f.write("""
</channel>
</rss>
""")
    f.close()


def LoadCache(fileName='entries.cache'):
    entries = []
    if not os.path.exists(fileName):
        return entries
    logging.info('Found cache file')
    cacheFile = open(fileName, 'r')
    try:
        while True:
            entry = pickle.load(cacheFile)
            logging.info('Load entry from cache file with title %s', entry['title'])
            entries.append(entry)
    except (pickle.PickleError, EOFError):
        logging.info("No more entries in cache file for loading")
    finally:
        cacheFile.close()
    return entries


def LoopFetchEntry(catchFileName, permaLink, isPostOnly=False, limit=0):
    count = 0
    entries = []
    cacheFile = open(catchFileName, 'a')
    try:
        while permaLink:
            item = FetchEntry(permaLink, isPostOnly=isPostOnly)
            logging.info("Got a blog entry titled %s with %d comments successfully", item['title'],
                         len(item['comments']))
            entries.append(item)
            pickle.dump(item, cacheFile)
            cacheFile.flush()
            logging.debug("-----------------------")
            if 'prevLink' in item:
                permaLink = item['prevLink']
            else:
                break
            count += 1
            if limit != 0 and count >= limit: break
    finally:
        cacheFile.close()
    return entries


def ArrangeEntries(entries, highlight, isAttach=True):
    """
    entries to postEntries, attachmentEntries, categories
    """
    logging.info("Arrange entries")
    categories = set([])
    attachEntries = []
    entries.sort(key=lambda e: e['id'])
    #sort entries
    for en in entries:
        #genearte new article id
        en['id'] = postIDGenerator.GetID(en['id'])
        #category
        categories.update(en['category'])
        #pretty code and comment
        en['content'] = PrettyCode(en['content'], highlight)
        for co in en['comments']: co['Content'] = PrettyComment(co['Content'])
        #new comment id
        en['comments'].sort(key=lambda e: e['CommentId'])
        for co in en['comments']:
            co['CommentId'] = commentIDGenerator.GetID(co['CommentId'])
            co['ParentId'] = commentIDGenerator.GetID(co['ParentId'])
            #attachment
        if isAttach:
            ProcessAttachment(en, attachEntries)
    logging.info("Arrange done")
    return entries, attachEntries, categories


def main(blogUrl):
    #main procedure begin, use optparse for compatible

    parser = OptionParser(usage="%prog -s|b URL [Options]\n CSDN博客搬家程序".decode('utf-8'), version="%prog " + __VERSION__)
    parser.add_option("-s", "--source", action="store", type="string", dest="srcURL", help="CSDN博客地址".decode('utf-8'))
    parser.add_option("-b", "--begin", action="store", type="string", dest="beginURL",
                      help="指定一个日志链接作为起始地址".decode('utf-8'))
    parser.add_option("-n", "--number", action="store", type="int", dest="limit", default=0,
                      help="导出的日志数目,默认无限制(0)".decode('utf-8'))
    parser.add_option("-o", "--postonly", action="store_true", dest="isPostOnly", default=False,
                      help="不导出日志的评论".decode('utf-8'))
    parser.add_option("-a", "--noattach", action="store_false", dest="isAttach", default=True,
                      help="不处理日志附件（CSDN博客附件不支持外链，慎用）".decode('utf-8'))
    parser.add_option("-i", "--idstart", action="store", type="int", dest="startId", default=10,
                      help="导出日志/评论在Wordpress中起始编号，默认10".decode('utf-8'))
    parser.add_option("-l", "--highlight", action="store", type="string", dest="lighttype", default="syntaxhighlight",
                      help="代码高亮可选syntaxhighlight和geshi两种，默认第一种，需对应插件支持".decode('utf-8'))

    (options, args) = parser.parse_args()
    options.lighttype = options.lighttype.lower()

    if not hlightdict.has_key(options.lighttype):
        logging.warning("Hightlight type error,exit")
        sys.exit(2)
    logging.info("Use code highlight type: %s", options.lighttype)
    #ID generate
    global postIDGenerator
    postIDGenerator = IDGenerator(options.startId)
    global commentIDGenerator
    commentIDGenerator = IDGenerator(options.startId)

    #find blog info
    if (blogUrl):
        blogInfo = FetchBlogInfo(blogUrl, True)
        logging.info('Start fetching from %s', blogUrl)
        options.srcURL = blogUrl
    elif options.beginURL:
        blogInfo = FetchBlogInfo(options.beginURL, False)
        logging.info('Start fetching from %s', options.beginURL)
    elif options.srcURL:
        blogInfo = FetchBlogInfo(options.srcURL, True)
        logging.info("Found permaLink %s", blogInfo["permaLink"])
    else:
        logging.error("Error, you must give either srcURL or beginURL")
        sys.exit(2)
        #load cache and resume from the last post in it
    cacheName = 'entries.cache'
    entries = LoadCache(cacheName)
    if len(entries) > 0 and not options.beginURL:
        permaLink = entries[-1]['prevLink']
    else:
        permaLink = blogInfo['permaLink']
        #main loop, get blog data and
    entries.extend(LoopFetchEntry(cacheName, permaLink, options.isPostOnly, options.limit))
    #data arrangement
    postEntries, attachEntries, categories = ArrangeEntries(entries, options.lighttype, options.isAttach)
    #export header

    exportFileName = 'export_' + datetime.now().strftime('%Y%m%d-%H%M%S') + '.xml'
    f = codecs.open(exportFileName, 'w', 'utf-8')
    if f:
        logging.info('Export XML to file %s', exportFileName)
    else:
        logging.error("Can't open export file %s for writing", exportFileName)
        sys.exit(2)
    ExportHead(f, blogInfo, categories)
    logging.debug('Exported header')
    #export attachment
    for entry in attachEntries:
        ExportEntry(f, entry, blogInfo['user'])
        #export entries
    for entry in postEntries:
        ExportEntry(f, entry, blogInfo['user'])
        #export Foot
    ExportFoot(f)
    logging.debug('Exported footer')
    #Delete cache file
    os.remove(cacheName)
    logging.info("Deleted cache file")
    logging.info("Finished! Congratulations!")


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG,
                        format='LINE %(lineno)-4d  %(levelname)-8s %(message)s',
                        datefmt='%m-%d %H:%M',
                        filename='blog-mover.log',
                        filemode='w');
    # define a Handler which writes INFO messages or higher to the sys.stderr
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    # set a format which is simpler for console use
    formatter = logging.Formatter('LINE %(lineno)-4d : %(levelname)-8s %(message)s')
    # tell the handler to use this format
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)
    try:
        main("http://blog.csdn.net/v_july_v")
    except SystemExit:
        pass
    except:
        logging.exception("Unexpected error")
        raise