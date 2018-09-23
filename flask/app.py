from flask import Flask, request, flash, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView


app = Flask(__name__)
app.config['SECRET_KEY'] = "randomstring"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

admin = Admin(app)

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

admin.add_view(ModelView(Pergunta, db.session))
admin.add_view(ModelView(Escolha, db.session))


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


if __name__ == '__main__':
   app.run(debug=True)
