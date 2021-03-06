from flask import Flask, request, flash, url_for, redirect, render_template, Blueprint
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user, login_user, logout_user

from .models import Usuario, Pergunta, Escolha
from app import db

enquetes = Blueprint('enquetes', __name__, url_prefix='/enquetes')

class NewModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated
    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('enquetes.login'))

class PerguntaModelView(ModelView):
    inline_models = (Escolha,)
    
class NewAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated
    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('enquetes.login'))


@enquetes.route('/')
def index():
   return render_template('enquetes/index.html', enquetes=Pergunta.query.all())

@enquetes.route('/resultados/<int:pergunta_id>')
def resultados(pergunta_id):
   return render_template('enquetes/resultados.html', pergunta=Pergunta.query.get_or_404(pergunta_id))

@enquetes.route('/detalhes/<int:pergunta_id>', methods=['GET', 'POST'])
def detalhes(pergunta_id):
    if request.method == 'POST':
        if not request.form.get('escolha'):
            flash('Escolha uma opção')
        else:
            escolha = Escolha.query.filter_by(id=request.form['escolha']).first()
            escolha.votos = escolha.votos + 1
            db.session.commit()

            return redirect(url_for('enquetes.resultados', pergunta_id=pergunta_id))

    return render_template('enquetes/detalhes.html', pergunta=Pergunta.query.get_or_404(pergunta_id))

@enquetes.route('/login', methods=['GET', 'POST'])
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

    return render_template('enquetes/login.html')

@enquetes.route('/logout')
def logout():
    logout_user()
    return render_template('enquetes/logout.html')