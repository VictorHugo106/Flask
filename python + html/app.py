# verifico a pasta do meu projeto, verifico se esta no meu github
# git remote -v
# executar
# git pull origin master (main)

# pip install flask
# pip install Flask-SQLAlchemy
# pip install Flask-Migrate
# pip install Flask-Script
# pip install pymsql

# flask db init
# flask db migrate -m "Migração Inicial"
# flask db upgrade
# flask run --debug  





from flask import Flask, render_template, request, flash, redirect
from database import db
from flask_migrate import Migrate
from models import Equipamentos

app = Flask(__name__)
app.config['SECRET_KEY'] = '21g3y2g72gsA'

# drive://usuario//senha@servidor/banco_dados
conexao = "mysql+pymysql://alunos:cefetmg@127.0.0.1/flaskVictor"
app.config['SQLALCHEMY_DATABASE_URI'] = conexao
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/aula')
@app.route('/aula/<nome>')
@app.route('/aula/<nome>/<curso>')
@app.route('/aula/<nome>/<curso>/<int:ano>')
def aula(nome = "Maria", curso='Informática', ano = 1):
     dados = {'nome': nome, 'curso': curso, 'ano': ano}
     return render_template('aula.html', dados_html = dados)

@app.route('/form')
def form():
    return render_template("form.html")

@app.route('/dados', methods=['POST'])
def dados():
    dados = request.form
    return render_template("dados.html", dados = dados)


@app.route("/usuario")
def usuario():
    u = Equipamentos.query.all()
    return render_template("usuario_lista.html", dados = u)


@app.route("/usuario/add")
def usuario_add():
    return render_template("usuario_add.html")

@app.route("/usuario/save", methods=['POST'])
def usuario_save():
    nome = request.form.get("nome")
    codigo = request.form.get("codigo")
    data_aquisicao = request.form.get("data_aquisicao")
    if nome and codigo and data_aquisicao:
        usuario = Equipamentos(nome, codigo, data_aquisicao)
        db.session.add(usuario)
        db.session.commit()
        flash('Usuario cadastrado com sucesso')
        return redirect("/usuario")
    
    else:
        flash("preencha todos os campos")
        return redirect("/usuario/add")
    
@app.route("/usuario/remove/<int:id_equipamento>")
def usuario_remove(id_equipamento):
    if id_equipamento > 0:
        usuario = Equipamentos.query.get(id_equipamento)
        db.session.delete(usuario)
        db.session.commit()
        flash("Usuario removido com sucesso! ")
        return redirect("/usuario")
    else:
        flash("Caminho INCORRETO")
        return redirect("/usuario")


@app.route("/usuario/edita/<int:id_equipamento>")
def usuario_edita(id_equipamento):
    usuario = Equipamentos.query.get(id_equipamento)
    return render_template("usuario_edita.html", dados = usuario)

@app.route("/usuario/editasave", methods=['POST'])
def usuario_editasave():
    id_equipamento = request.form.get("id_equipamento")
    nome = request.form.get("nome")
    codigo = request.form.get("codigo")
    data_aquisicao = request.form.get("data_aquisicao")
    if id_equipamento and nome and codigo and data_aquisicao:
        usuario = Equipamentos.query.get(id_equipamento)
        usuario.nome = nome
        usuario.codigo = codigo
        usuario.data_aquisicao = data_aquisicao
        db.session.commit()
        flash("Dados atualizados com sucesso!")
        return redirect("/usuario")
    else:
        flash("Faltando dados seu idiota")
        return redirect("/usuario")

if __name__ == '__main__':
    app.run()

