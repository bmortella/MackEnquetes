from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Pergunta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    enunciado = db.Column(db.String(200), unique=True, nullable=False)
    data_pub = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    escolha = db.relationship('Escolha', backref='person', lazy=True)

    def __repr__(self):
        return '<Pergunta %r>' % self.enunciado

class Escolha(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    texto = db.Column(db.String(200), unique=True, nullable=False)
    votos = db.Column(db.Integer)

    pergunta_id = db.Column(db.Integer, db.ForeignKey('pergunta.id'), nullable=False)

    def __repr__(self):
        return '<Escolha %r>' % self.title
