__author__ = 'rui'
#coding=utf-8

import datetime

import web

db = web.database(dbn='sqlite', db='blog.db')


def get_posts():
    return db.select('entries', order='id desc')


def get_post(id):
    try:
        return db.select('entries', where='id=$id',
                         vars=locals())[0]
    except IndexError:
        return None


def new_post(title, text):
    db.insert('entries', title=title, content=text,
              posted_on=datetime.datetime.utcnow())


def del_post(id):
    db.delete('entries', where='id=$id', vars=locals())


def update_post(id, title, text):
    db.update('entries', where='id=$id', vars=locals(),
              title=title, content=text)


def transform_datestr(posted_on):
    datetime_obj = datetime.datetime.strptime(posted_on, '%Y-%m-%d %H:%M:%S.%f')
    return web.datestr(datetime_obj)