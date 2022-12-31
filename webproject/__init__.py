from flask import Flask, redirect, render_template, request
from flask_login import LoginManager

from webproject.extensions import db, migrate


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///blockhain.db"
    app.config["SECRET_KEY"] = "ABC"

    db.init_app(app)
    migrate.init_app(app,db)

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    from webproject.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from webproject.routes.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from webproject.routes.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from webproject.routes.nfts import nfts as nft_blueprint
    app.register_blueprint(nft_blueprint)

    from webproject.routes.assets import assets as assets_blueprint
    app.register_blueprint(assets_blueprint)

    return app
