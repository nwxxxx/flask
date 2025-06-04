import os

from flask import Flask, render_template


def create_app(test_config=None):
    # 创建并配置这个app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),#数据库文件路径
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'
    
    #首页（做博客视图之前演示它）
    #@app.route('/')
    #def index():
    #    return render_template('base.html')

    #初始化数据库
    from . import db #. 表示 当前包，即flaskr；导入db.py里的内容
    db.init_app(app)

    #注册蓝图auth   
    from . import auth
    app.register_blueprint(auth.bp)

    #注册蓝图blog
    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')


    return app