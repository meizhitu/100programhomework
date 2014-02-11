__author__ = 'rui'
#coding=utf-8
import web
import model

render = web.template.render('templates', base='base')
web.config.debug = True

config = web.storage(
    site_name='博客',
    datestr=model.transform_datestr
)

web.template.Template.globals['config'] = config
web.template.Template.globals['render'] = render