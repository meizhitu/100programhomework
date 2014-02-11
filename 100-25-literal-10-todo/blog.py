#coding=utf-8
import sys
import os

import web
import model
import config

if sys.getdefaultencoding() != 'utf-8':
    reload(sys)
    sys.setdefaultencoding('utf-8')
###url mapping
urls = (
    '/', 'Index',
    '/view/(\d+)', 'View',
    '/new', 'New',
    '/delete/(\d+)', 'Delete',
    '/edit/(\d+)', 'Edit',
    '/imgs/(.*)', 'Imgs'
)

render = config.render


class Index:
    def GET(self):
        posts = model.get_posts()
        return render.index(posts)


class View:
    def GET(self, id):
        post = model.get_post(int(id))
        return render.view(post)


class New:
    form = web.form.Form(
        web.form.Textbox('title', web.form.notnull,
                         size=30,
                         description=u'日志标题'),
        web.form.Textarea('content', web.form.notnull,
                          rows=30, cols=80,
                          description=u'日志内容'),
        web.form.Button(u'提交')
    )

    def GET(self):
        form = self.form()
        return render.new(form)

    def POST(self):
        form = self.form()
        if not form.validates():
            return render.new(form)
        model.new_post(form.d.title, form.d.content)
        raise web.seeother('/')


class Delete:
    def POST(self, id):
        model.del_post(int(id))
        raise web.seeother('/')


class Edit:
    def GET(self, id):
        post = model.get_post(int(id))
        form = New.form()
        form.fill(post)
        return render.edit(post, form)

    def POST(self, id):
        form = New.form()
        post = model.get_post(int(id))
        if not form.validates():
            return render.edit(post, form)
        model.update_post(int(id), form.d.title, form.d.content)
        raise web.seeother('/')


class Imgs:
    def GET(self, name):
        ext = name.split(".")[-1]
        cType = {
            "png": "images/png",
            "jpg": "images/jpeg",
            "gif": "images/gif",
            "ico": "images/x-icon"
        }
        if name in os.listdir('imgs'):
            web.header("Content-Type", cType[ext])
            return open('imgs/%s' % name, "rb").read()
        else:
            raise web.notfound()


app = web.application(urls, globals())
if __name__ == '__main__':
    app.run()