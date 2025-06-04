import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db


bp = Blueprint('auth', __name__, url_prefix='/auth')#创建一个名称为 'auth' 的蓝图Blueprint

'''
这里创建了一个名称为 'auth' 的蓝图Blueprint。
和应用对象一样， 蓝图需要知道是在哪里定义的，因此把 __name__ 作为函数的第二个参数。 
url_prefix的值为'/auth'，会添加在所有与该蓝图关联的 URL 前面。
'''

#注册的路由装饰器：由于@蓝图变量bp，实际的路由是/auth/register
@bp.route('/register', methods=('GET', 'POST'))
def register():
    '''
    注册的视图函数   
    '''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            try:
                db.execute(
                    "INSERT INTO user (username, password) VALUES (?, ?)",
                    (username, generate_password_hash(password)),#密码加密处理
                )
                db.commit()#提交
            except db.IntegrityError:
                error = f"User {username} is already registered."
            else:
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template('auth/register.html')


#登录的路由装饰器：由于@蓝图变量bp，实际的路由是/auth/login
@bp.route('/login', methods=('GET', 'POST'))
def login():
    '''
    登录的视图函数
    '''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db() #连接数据库
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone() #根据查询返回一个记录行

        if user is None:
            error = 'Incorrect username.'
            #check_password_hash：以相同的方式哈希提交的 密码并安全的比较哈希值
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')

#在所有请求开始时，执行预处理：检查用户是否已登录
@bp.before_app_request
def load_logged_in_user():
    '''
    视图函数：在所有请求开始时，检查用户是否已登录
    '''
    user_id = session.get('user_id')
    #检查用户 id 是否已经储存在 session 中，并从数据库中获取用户数据，然后储存在 g.user 中。 g.user 的持续时间比请求要长
    if user_id is None: #不存在
        g.user = None
    else:
        g.user = get_db().execute(#登录后生成全局变量g.user
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()

#注销的路由装饰器：由于@蓝图变量bp，实际的路由是/auth/logout
@bp.route('/logout')
def logout():
    '''
    注销的视图函数
    '''
    session.clear()
    return redirect(url_for('index'))


def login_required(view):
    """
    登录验证装饰器：用于保护需要登录才能访问的视图函数
    
    参数：
        view: 被装饰的视图函数
    
    返回：
        wrapped_view: 包装后的视图函数，增加了登录验证功能
    
    工作流程：
        1. 检查用户是否已登录（通过 g.user 判断）
        2. 如果未登录，重定向到登录页面
        3. 如果已登录，执行原视图函数
    
    使用示例：
        @login_required
        def create_post():
            # 只有登录用户才能访问这个视图
            return render_template('create.html')
    """
    @functools.wraps(view)  # 保留原视图函数的元信息（如函数名、文档字符串等）
    def wrapped_view(**kwargs):
        # 检查用户是否已登录
        if g.user is None:
            # 未登录则重定向到登录页面
            return redirect(url_for('auth.login'))

        # 已登录则执行原视图函数，并传递所有参数
        return view(**kwargs)

    return wrapped_view

