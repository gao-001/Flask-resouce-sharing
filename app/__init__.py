from flask_sqlalchemy import SQLAlchemy
from flask import Flask, redirect, url_for, request
from flask_migrate import Migrate
from config import Schedule
from flask_admin import Admin, BaseView, expose, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_login import LoginManager, current_user, login_required
import os

login_manage = LoginManager()
login_manage.login_view = 'auth.login'
db = SQLAlchemy()
admin = Admin()

basedir = os.path.abspath(os.path.dirname(__file__))

from .models import Playlist, Musicfile, Music, Movie, DetailUrl, User


class MyView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('auth.login', next=request.url))


admin.add_view(MyView(Movie, db.session))
admin.add_view(MyView(Playlist, db.session))
admin.add_view(MyView(Music, db.session))
admin.add_view(MyView(Musicfile, db.session))
admin.add_view(MyView(DetailUrl, db.session))


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # 配置数据库
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://user:password@localhost:3306/movie'

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data_dev.sqlite')

    app.config['SCHEDULER_API_ENABLED'] = True
    app.config['SECRET_KEY'] = 'dgajkdgfaslui'
    app.config.from_object(Schedule())  # 定时任务
    db.init_app(app)
    admin.init_app(app)
    login_manage.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    return app
