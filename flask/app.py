from flask import Flask, request, flash, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_login import UserMixin, LoginManager, current_user, login_user, logout_user

app = Flask(__name__)
app.config['SECRET_KEY'] = "randomstring"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login = LoginManager(app)

@login.user_loader
def load_user(user_id):
    return Usuario.query.get(user_id)


class Pergunta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    enunciado = db.Column(db.String(200), unique=True, nullable=False)
    data_pub = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    escolha = db.relationship('Escolha', backref='pergunta', lazy=False)

    def __repr__(self):
        return '<Pergunta %r>' % self.enunciado

    def __str__(self):
        return self.enunciado

class Escolha(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    texto = db.Column(db.String(200), unique=True, nullable=False)
    votos = db.Column(db.Integer, default=0)

    pergunta_id = db.Column(db.Integer, db.ForeignKey('pergunta.id'), nullable=False)

    def __repr__(self):
        return '<Escolha %r, Votos %r>' % (self.texto, self.votos)

class Usuario(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(15), unique=True, nullable=False)
    senha = db.Column(db.String(20), unique=True, nullable=False)

    def __repr__(self):
        return '<Usuario %r, Senha%r>' % (self.usuario, self.senha)

class NewModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated
    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login'))
    
class NewAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated
    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login'))

admin = Admin(app, index_view=NewAdminIndexView())
admin.add_view(NewModelView(Pergunta, db.session))
admin.add_view(NewModelView(Escolha, db.session))
admin.add_view(NewModelView(Usuario, db.session))


@app.route('/')
def index():
   return render_template('index.html', enquetes=Pergunta.query.all())

@app.route('/resultados/<int:pergunta_id>')
def resultados(pergunta_id):
   return render_template('resultados.html', pergunta=Pergunta.query.get_or_404(pergunta_id))

@app.route('/detalhes/<int:pergunta_id>', methods=['GET', 'POST'])
def detalhes(pergunta_id):
    if request.method == 'POST':
        if not request.form.get('escolha'):
            flash('Escolha uma opção')
        else:
            escolha = Escolha.query.filter_by(id=request.form['escolha']).first()
            escolha.votos = escolha.votos + 1
            db.session.commit()

            return redirect(url_for('resultados', pergunta_id=pergunta_id))

    return render_template('detalhes.html', pergunta=Pergunta.query.get_or_404(pergunta_id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if not request.form['usuario'] or not request.form['senha']:
           flash('Digite o Usuário e a Senha')

        else:
            exists = db.session.query(db.exists().where(Usuario.usuario == request.form['usuario'] )).scalar()

            if exists:
                usuario = Usuario.query.filter_by(usuario=request.form['usuario']).first()
                if usuario.senha ==  request.form['senha']:

                    login_user(usuario)
                    return redirect(url_for('admin.index'))
                else:
                    flash('Usuário desconhecido ou senha incorreta')
            else:
                flash('Usuário desconhecido ou senha incorreta')

    return render_template('login.html')

@app.route('/logout')
def logout():
    logout_user()
    return render_template('logout.html')

if __name__ == '__main__':
   app.run(debug=True)
