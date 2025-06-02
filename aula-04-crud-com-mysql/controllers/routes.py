from flask import render_template, redirect, url_for, request
from models.database import Game, Console, db

jogadores = ['Miguel José', 'Miguel Isack', 'Leaf',
             'Quemario', 'Trop', 'Aspax', 'maxxdiego']

gamelist = [{
    'Título': 'CS-GO',
    'Ano': 2012,
    'Categoria': 'FPS Online'
}]


def init_app(app):
    @app.route('/')
    def home():
        return render_template('index.html')

    @app.route('/games', methods=['GET', 'POST'])
    def games():
        game = gamelist[0]
        if request.method == 'POST':
            jogador = request.form.get('jogador')
            if jogador:
                jogadores.append(jogador)
            return redirect(url_for('games'))

        jogos = ['Jogo 1', 'Jogo 2', 'Jogo 3', 'Jogo 4', 'Jogo 5', 'Jogo 6']
        return render_template('games.html',
                               game=game,
                               jogadores=jogadores,
                               jogos=jogos)

    @app.route('/cadgames', methods=['GET', 'POST'])
    def cadgames():
        if request.method == 'POST':
            titulo = request.form.get('titulo')
            ano = request.form.get('ano')
            categoria = request.form.get('categoria')

            if titulo and ano and categoria:
                gamelist.append({
                    'Título': titulo,
                    'Ano': ano,
                    'Categoria': categoria
                })

            return redirect(url_for('cadgames'))

        return render_template('cadgames.html', gamelist=gamelist)

    @app.route('/estoque', methods=['GET', 'POST'])
    def estoque():
        if request.method == 'POST':
            newgame = Game(
                titulo=request.form['titulo'],
                ano=request.form['ano'],
                categoria=request.form['categoria'],
                plataforma=request.form['plataforma'],
                preco=request.form['preco'],
                quantidade=request.form['quantidade']
            )
            db.session.add(newgame)
            db.session.commit()
            return redirect(url_for('estoque'))

        page = request.args.get('page', 1, type=int)
        per_page = 3
        games_page = Game.query.paginate(page=page, per_page=per_page)
        return render_template('estoque.html', gamesestoque=games_page)

    @app.route('/estoqueconsole', methods=['GET', 'POST'])
    @app.route('/estoqueconsole/<int:id>', methods=['POST', 'DELETE'])
    def estoqueconsole(id=None):
        if id:
            console = Console.query.get(id)
            if console:
                db.session.delete(console)
                db.session.commit()
            return redirect(url_for('estoqueconsole'))

        if request.method == 'POST' and not id:
            newconsole = Console(
                nome=request.form['nome'],
                fabricante=request.form['fabricante'],
                preco=request.form['preco'],
                quantidade=request.form['quantidade']
            )
            db.session.add(newconsole)
            db.session.commit()
            return redirect(url_for('estoqueconsole'))

        consoles = Console.query.all()
        return render_template('estoqueconsole.html', estoqueconsole=consoles)

    @app.route('/editgame/<int:id>', methods=['GET', 'POST'])
    def editgame(id):
        game = Game.query.get(id)
        if not game:
            return "Jogo não encontrado", 404

        if request.method == 'POST':
            game.titulo = request.form['titulo']
            game.ano = request.form['ano']
            game.categoria = request.form['categoria']
            game.plataforma = request.form['plataforma']
            game.preco = request.form['preco']
            game.quantidade = request.form['quantidade']
            db.session.commit()
            return redirect(url_for('estoque'))

        return render_template('editgame.html', game=game)

    @app.route('/editconsole/<int:id>', methods=['GET', 'POST'])
    def editconsole(id):
        console = Console.query.get(id)
        if not console:
            return "Console não encontrado", 404

        if request.method == 'POST':
            console.nome = request.form['nome']
            console.fabricante = request.form['fabricante']
            console.preco = request.form['preco']
            console.quantidade = request.form['quantidade']
            db.session.commit()
            return redirect(url_for('estoqueconsole'))

        return render_template('editconsole.html', console=console)
