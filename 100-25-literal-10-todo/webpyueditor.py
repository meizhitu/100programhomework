__author__ = 'rui'
#coding=utf-8
import base64
import uuid
import urllib2
import os

import web

ueconfig_dir = 'static/upload'
ueconfig_url = '/' + ueconfig_dir


def listImage(rootDir, retlist):
    for cfile in os.listdir(rootDir):
        path = os.path.join(rootDir, cfile)
        if os.path.isdir(path):
            listImage(path, retlist)
        else:
            if cfile.endswith('.gif') or cfile.endswith('.png') or cfile.endswith('.jpg') or cfile.endswith('.bmp'):
                retlist.append('/static/upload/' + cfile)


def saveUploadFile(fileName, content):
    fileName = fileName.replace('\\', '/') # replaces the windows-style slashes with linux ones.
    fout = open(ueconfig_dir + '/' + fileName, 'wb') # creates the file where the uploaded file should be stored
    fout.write(content) # writes the uploaded file to the newly created file.
    fout.close() # closes the file, upload complete.


class Ue_ImageUp:
    def GET(self):
        reqData = web.input()
        if 'fetch' in reqData:
            web.header('Content-Type', 'text/javascript')
            return 'updateSavePath(["upload"]);'
        web.header("Content-Type", "text/html; charset=utf-8")
        return ""

    def POST(self):
        postData = web.input(upfile={}, pictitle="")
        web.debug(postData)
        fileObj = postData.upfile
        picTitle = postData.pictitle
        fileName = fileObj.filename
        newFileName = str(uuid.uuid1()) + ".png"
        saveUploadFile(newFileName, fileObj.file.read())
        return "{'url':'" + ueconfig_url + '/' + newFileName + "','title':'" + picTitle + "','original':'" + fileName + "','state':'" + "SUCCESS" + "'}"


class Ue_FileUp:
    def GET(self):
        web.header("Content-Type", "text/html; charset=utf-8")
        return ""

    def POST(self):
        postData = web.input(upfile={})
        fileObj = postData.upfile
        fileName = postData.Filename
        ext = '.' + fileName.split('.')[-1]
        #web.py的static目录对中文文件名不支持，会404
        newFileName = str(uuid.uuid1()) + ext
        #fileNameFormat = postData.fileNameFormat
        saveUploadFile(newFileName, fileObj.file.read())
        return "{'url':'" + ueconfig_url + '/' + newFileName + "','fileType':'" + ext + "','original':'" + fileName + "','state':'" + "SUCCESS" + "'}"


class Ue_ScrawlUp:
    def GET(self):
        web.header("Content-Type", "text/html; charset=utf-8")
        return ""

    def POST(self):
        reqData = web.input(upfile={})
        if 'action' in reqData:
            if reqData.action == 'tmpImg':
                #上传背景
                fileObj = reqData.upfile
                fileName = fileObj.filename
                saveUploadFile(fileName, fileObj.file.read())
                return "<script>parent.ue_callback(" + ueconfig_url + '/' + fileName + "','" + "SUCCESS" + "')</script>"
        else:
            base64Content = reqData.content
            fileName = str(uuid.uuid1()) + '.png'
            saveUploadFile(fileName, base64.decodestring(base64Content))
            return "{'url':'" + ueconfig_url + '/' + fileName + "',state:'" + "SUCCESS" + "'}"


class Ue_GetRemoteImage:
    def GET(self):
        web.header("Content-Type", "text/html; charset=utf-8")
        return ""

    def POST(self):
        postData = web.input()
        urls = postData.upfile
        #urls = urls.replace('&amp','&')
        urllist = urls.split("ue_separate_ue")
        fileType = [".gif", ".png", ".jpg", ".jpeg", ".bmp"]
        outlist = []
        for fileurl in urllist:
            if not fileurl.startswith('http'):
                continue
            ext = "." + fileurl.split('.')[-1]
            web.debug(ext + "|" + fileurl)
            if ext in fileType:
                fileName = str(uuid.uuid1()) + ext
                saveUploadFile(fileName, urllib2.urlopen(fileurl).read())
                outlist.append(ueconfig_url + "/" + fileName)
        outlist = "ue_separate_ue".join(outlist)
        return "{'url':'" + outlist + "','tip':'远程图片抓取成功！','srcUrl':'" + urls + "'}"


class Ue_GetMovie:
    def POST(self):
        reqData = web.input()
        skey = reqData.searchKey
        vtype = reqData.videoType
        surl = 'http://api.tudou.com/v3/gw?method=item.search&appKey=myKey&format=json&kw=' + skey + '&pageNo=1&pageSize=20&channelId=' + vtype + '&inDays=7&media=v&sort=s'
        htmlContent = urllib2.urlopen(surl).read()
        web.debug(htmlContent)
        return htmlContent


class Ue_ImageManager:
    def POST(self):
        reqData = web.input()
        if 'action' in reqData:
            if reqData.action == 'get':
                retfiles = []
                listImage(ueconfig_dir, retfiles)
                htmlContent = "ue_separate_ue".join(retfiles)
                return htmlContent

