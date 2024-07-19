from flask import Flask
# from flask_restful import Api,Resource,reqparse,abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

db=SQLAlchemy()
migrate=Migrate()
def create_app():
    app=Flask(__name__)

    app.config['SECRET_KEY']='FDSFHDFHFdfdfg'
    app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///dev.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

  

    from .views import views
    from .auth import auth
    from .models import User,Blog,Comment


    migrate.init_app(app,db)

    app.register_blueprint(views,url_prefix='/')
    app.register_blueprint(auth,url_prefix='/')
    login_manager=LoginManager()
    login_manager.login_view='auth.login'  # type: ignore
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    return app









   



