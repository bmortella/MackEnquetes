from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin

from enquete_app import app

app.config['SECRET_KEY'] = "randomstring"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

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


