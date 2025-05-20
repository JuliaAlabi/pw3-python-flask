from flask import render_template, redirect, url_for, request
from models.database import Game, db
from models.database import Console

# Lista de jogadores
jogadores = ['Miguel José', 'Miguel Isack', 'Leaf',
             'Quemario', 'Trop', 'Aspax', 'maxxdiego']

# Array de objetos - Lista de games
gamelist = [{'Título': 'CS-GO',
            'Ano': 2012,
             'Categoria': 'FPS Online'}]


def init_app(app):
    @app.route('/')
    def home():
        return render_template('index.html')

    @app.route('/games', methods=['GET', 'POST'])
    def games():
        game = gamelist[0]
        if request.method == 'POST':
            if request.form.get('jogador'):
                jogadores.append(request.form.get('jogador'))
            return redirect(url_for('games'))

        jogos = ['Jogo 1', 'Jogo 2', 'Jogo 3', 'Jogo 4', 'Jogo 5', 'Jogo 6']
        return render_template('games.html',
                               game=game,
                               jogadores=jogadores,
                               jogos=jogos)

    @app.route('/cadgames', methods=['GET', 'POST'])
    def cadgames():
        if request.method == 'POST':
            if request.form.get('titulo') and request.form.get('ano') and request.form.get('categoria'):
                gamelist.append({
                    'Título': request.form.get('titulo'),
                    'Ano': request.form.get('ano'),
                    'Categoria': request.form.get('categoria')
                })
            return redirect(url_for('cadgames'))
        return render_template('cadgames.html',
                               gamelist=gamelist)

    @app.route('/estoque', methods=['GET','POST'])
    @app.route('/estoqueconsole/<int:id>', methods=['GET', 'POST', 'DELETE'])
    def estoque(id=None):
        if id:
            game = Game.query.get(id)
            db.session.delete(game)
            db.session.commit()
            return redirect(url_for('estoque'))
        
        if request.method =='POST':
            newgame=  Game(request.form['titulo'], request.form['ano'],
            request.form['categoria'], request.form['plataforma'],
            request.form['preco'],
            request.form['quantidade'])
            db.session.add(newgame)
            db.session.commit()
            return redirect(url_for('estoque'))
            
        
        gamesestoque =Game.query.all()
        return render_template('estoque.html',
        gamesestoque=gamesestoque)
    
    @app.route('/estoqueconsole', methods=['GET', 'POST'])
    @app.route('/estoqueconsole/<int:id>', methods=['GET', 'POST', 'DELETE'])
    def estoqueconsole(id=None):
        if id:
           console = Console.query.get(id)
           db.session.delete(console)
           db.session.commit()
           return redirect(url_for('estoqueconsole'))
    
        if request.method =='POST':
            newconsole = Console(request.form['nome'], request.form['fabricante'],
                           request.form['preco'],
                           request.form['quantidade'])
            db.session.add(newconsole)
            db.session.commit()
            return redirect(url_for('estoqueconsole'))
        
        estoqueconsole = Console.query.all()
        return render_template('estoqueconsole.html',
                           estoqueconsole=estoqueconsole)
        
    @app.route('/editgame/<int:id>', methods=['GET', 'POST'])
    def editgame(id):
        game = Game.query.get(id)
        
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
