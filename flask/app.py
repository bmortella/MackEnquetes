from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask import render_template

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
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
    votos = db.Column(db.Integer)

    pergunta_id = db.Column(db.Integer, db.ForeignKey('pergunta.id'), nullable=False)

    def __repr__(self):
        return '<Escolha %r, Votos %r>' % (self.texto, self.votos)


@app.route('/')
def index():
   return render_template('index.html', enquetes=Pergunta.query.all())

@app.route('/resultados/<int:pergunta_id>')
def resultados(pergunta_id):
   return render_template('resultados.html', pergunta=Pergunta.query.get_or_404(pergunta_id))

if __name__ == '__main__':
   app.run(debug=True)
