# -*- coding: utf-8 -*-
# 2017/1/4 10:32
"""
-------------------------------------------------------------------------------
Function:   a small simple of our web app
Version:    1.0
Author:     SLY
Contact:    slysly759@gmail.com 
 
-------------------------------------------------------------------------------
"""

import logging
logging.basicConfig(level=logging.INFO)
import asyncio, json, os, time
from aiohttp import web
# 首要解决的就是这个parse函数自解析
from webframe.factory import logger_factory,data_factory, response_factory, auth_factory
import webframe.orm
from base import add_routes, add_static
from jinja2 import Environment, FileSystemLoader
from login_data_transfer import datetime_filter

# 注意：这里jinjia的模板做了一个渲染映射 那么我很想重新写一个 感觉不复杂 主要是我用到的不复杂
# 让我想想 我只需要一个html 渲染 和 html 路径映射的什么
def init_jinjia2(app, **kw):
    logging.info('init jinja2 template...')
    options=dict(
        autoescape = kw.get('autoescape', True),
        block_start_string = kw.get('block_start_string','{%',),
        block_end_string=kw.get('block_end_string','%}'),
        variable_start_string=kw.get('variable_start_string','{{'),
        variable_end_string=kw.get('variable_end_string','}}'),
        auto_reload=kw.get('auto_reload', True)
    )
    path=kw.get('path',None)
    if path is None:
        # 以下代码如果只是将路径指向templates的绝对路径的话 作者你过来我保证不打死你
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'templates')
        logging.info('The jinjia template is set here: %s'% path)
        env = Environment(loader=FileSystemLoader(path), **options)
        filters=kw.get('filters', None)
        if filters is not None:
            for name, f in filters.items():
                env.filters[name]=f
        app['__templating__']= env
def init_fuckcnf():
    conf=''.join(open('db.conf',encoding='utf8').readlines())
    my_conf=eval(conf)# 没事别用轮子给自己加戏谢谢
    global my_host,my_port,my_username,my_password,my_db
    my_host=my_conf.get('host','localhost')
    my_port=my_conf.get('port',3308)
    my_username=my_conf.get('user','root')
    my_password=my_conf.get('password','root')
    my_db=my_conf.get('db','fuckblog')
    return
# 数据库初始化工具
# 因为这个初始化只用到一次不是aio或者异步类型，我仅需要做链接测试建库就好
def init_fuckdb():
    import pymysql
    con = pymysql.connections.Connection(host=my_host, port=my_port, user=my_username, password=my_password, charset='utf8mb4',
                                         cursorclass=pymysql.cursors.DictCursor)
    cur = con.cursor()
    sql = ''.join(open('db-start.sql', encoding='utf8').readlines())
    cur.execute(sql)
    con.commit()
    con.close()
    return


# def replace_jinja(app,**kw):
#     path=kw.get('path',None)
#     if path is None:
#         # 以下代码如果只是将路径指向templates的绝对路径的话 作者你过来我保证不打死你
#         path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'templates')
#         logging.info('The jinjia template is set here: %s'% path)
#         env = Environment(loader=FileSystemLoader(path))
#         filters=kw.get('filters', None)
#         if filters is not None:
#             for name, f in filters.items():
#                 env.filters[name]=f
#         app['__templating__']= env

# 现在需要对数据库配置进行一点外部化 （虽然达不到wp那种直接在网页上操作的，但随大流写记事本上总可以）


@asyncio.coroutine
def fuck_init(loop):
    yield from webframe.orm.create_pool(loop=loop,host=my_host, port=my_port, user=my_username, password=my_password,db=my_db)
    app = web.Application(loop=loop, middlewares=[
        logger_factory, response_factory, data_factory,auth_factory
    ])
    init_jinjia2(app, filters=dict(datetime=datetime_filter))
    add_routes(app,'api')
    add_static(app)
    srv=yield from loop.create_server(app.make_handler(),'127.0.0.1',9000)
    logging.info('server is starting at 9000 port')
    return srv
init_fuckcnf()
init_fuckdb()
loop = asyncio.get_event_loop()
loop.run_until_complete(fuck_init(loop))
loop.run_forever()
