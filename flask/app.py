from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import  LoginManager
from flask_admin import Admin


db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    app.config['SECRET_KEY'] = "randomstring"
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    db.init_app(app)

    from enquetes.views import enquetes, NewAdminIndexView, NewModelView
    app.register_blueprint(enquetes)

    #Registra admin
    from enquetes.models import Usuario, Pergunta, Escolha
    login = LoginManager(app)

    @login.user_loader
    def load_user(user_id):
        return Usuario.query.get(user_id)

    admin = Admin(app, index_view=NewAdminIndexView())
    admin.add_view(NewModelView(Pergunta, db.session))
    admin.add_view(NewModelView(Escolha, db.session))
    admin.add_view(NewModelView(Usuario, db.session))
    
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)