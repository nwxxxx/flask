import sqlite3
from datetime import datetime

import click
from flask import current_app, g
'''
这里，
g 是一个特殊对象，独立于每一个请求。在处理请求过程中，
它可以用于储存可能多个函数都会用到的数据。把连接储存于其中，
可以多次使用， 而不用在同一个请求中每次调用 get_db 时都创建一个新的连接。

current_app 是另一个特殊对象，该对象指向处理请求的 Flask 应用。 
'''


def init_db():
    '''
    在init_db里，先连接数据库，然后执行'schema.sql'里的SQL语句建库建表
    '''
    db = get_db()

    with current_app.open_resource('schema.sql') as f:#打开一个文件
        db.executescript(f.read().decode('utf8'))


@click.command('init-db') #定义一个名为 init-db 命令行，后面可以命令行中运行它
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


sqlite3.register_converter( #告诉 Python 如何解释数据库中 的时间戳值，我们将值转换为 datetime.datetime 。
    "timestamp", lambda v: datetime.fromisoformat(v.decode())
)

def get_db():#连接数据库
    if 'db' not in g: #g.db类似一个全局变量
        g.db = sqlite3.connect( 
            current_app.config['DATABASE'], #建立一个数据库连接，该连接指向配置中的 DATABASE 指定的文件
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row #将数据库的行转换为字典

    return g.db


def close_db(e=None):
    db = g.pop('db', None) #取得g中的db

    if db is not None:
        db.close() #关闭数据库连接

def init_app(app):
    app.teardown_appcontext(close_db)
    '''
    teardown_appcontext 是 Flask 的一个装饰器，用于注册在请求上下文结束时需要执行的函数
    用于在请求结束后自动关闭数据库连接
    '''
    app.cli.add_command(init_db_command)
    '''
    这行代码向 Flask 的命令行接口（CLI）添加了一个新的命令
    允许你通过命令行来初始化数据库
    '''

