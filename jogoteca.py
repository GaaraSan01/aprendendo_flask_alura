from flask import Flask, render_template, request, redirect, session, flash, url_for


class Jogo:
    def __init__(self, nome, categoria, console):
        self.nome = nome
        self.categoria = categoria
        self.console = console

class Usuario:
    def __init__(self, name, nikename, password):
        self.name = name
        self.nikename = nikename
        self.password = password


app = Flask(__name__)
app.secret_key = 'vnici'

jogo01 = Jogo('Mobile Legends', 'Mobile', 'Mobile')
jogo02 = Jogo('Mortal Kombat', 'Luta', 'PS1')
jogo03 = Jogo('Minecraft', 'Survivavel', 'PC')

# Usuários

usuario01 = Usuario('Vinicius h.', 'GaaraSan01', 'Vhms2023')
usuario02 = Usuario('Caroline r.', 'Enilorac', 'Crs2023')
usuario03 = Usuario('Samuel a.', 'Arthur', 'Samrs2023')

usuarios = {
    usuario01.nikename: usuario01,
    usuario02.nikename: usuario02,
    usuario03.nikename: usuario03
}

lista = [jogo01, jogo02, jogo03]

@app.route('/')
def index():
    return render_template('index.html', titulo='Jogos', jogos=lista)

@app.route('/novo')
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('novo')))
    return render_template('novo.html', titulo='Novo jogo')

@app.route('/criar', methods=['POST',])
def criar():
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']

    jogo = Jogo(nome, categoria, console)
    lista.append(jogo)
    return redirect(url_for('index'))

@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima=proxima)

@app.route('/autenticar', methods=['POST',])
def autenticar():
    if request.form['usuario'] in usuarios:
       usuario = usuarios[request.form['usuario']]
       if request.form['senha'] == usuario.password:
            session['usuario_logado'] = usuario.nikename
            flash(f'Usuário {usuario.nikename} logado com sucesso!')
            proxima_pagina = request.form['proxima']
            return redirect(proxima_pagina)
    else:
        flash('Usuário não logado!')
        return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Logout realizado com sucesso!')
    return redirect(url_for('login'))

app.run(debug=True)