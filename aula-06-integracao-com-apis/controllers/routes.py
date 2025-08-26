from flask import render_template, request, url_for, redirect
from models.database import db, Game, Console
import urllib  # Permitir ler URL das APIS
import json  # Conversão de dados

# Lista de jogadores
jogadores = ['Miguel José', 'Miguel Isack', 'Leaf',
             'Quemario', 'Trop', 'Aspax', 'maxxdiego']
# Lista de jogos
gamelist = [{'Título': 'CS-GO', 'Ano': 2012, 'Categoria': 'FPS Online'}]


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
        return render_template('games.html',
                               game=game,
                               jogadores=jogadores)

    @app.route('/cadgames', methods=['GET', 'POST'])
    def cadgames():
        if request.method == 'POST':
            if request.form.get('titulo') and request.form.get('ano') and request.form.get('categoria'):
                gamelist.append({'Título': request.form.get('titulo'), 'Ano': request.form.get(
                    'ano'), 'Categoria': request.form.get('categoria')})
                return redirect(url_for('cadgames'))

        return render_template('cadgames.html',
                               gamelist=gamelist)

    # CRUD GAMES - LISTAGEM, CADASTRO E EXCLUSÃO
    @app.route('/games/estoque', methods=['GET', 'POST'])
    @app.route('/games/estoque/delete/<int:id>')
    def gamesEstoque(id=None):
        if id:
            game = Game.query.get(id)
            # Deleta o jogo cadastro pela ID
            db.session.delete(game)
            db.session.commit()
            return redirect(url_for('gamesEstoque'))
        # Cadastra um novo jogo
        if request.method == 'POST':
            newgame = Game(request.form['titulo'], request.form['ano'], request.form['categoria'],
                           request.form['preco'], request.form['quantidade'])
            db.session.add(newgame)
            db.session.commit()
            return redirect(url_for('gamesEstoque'))
        else:
            # Captura o valor de 'page' que foi passado pelo método GET
            # Define como padrão o valor 1 e o tipo inteiro
            page = request.args.get('page', 1, type=int)
            # Valor padrão de registros por página (definimos 3)
            per_page = 3
            # Faz um SELECT no banco a partir da pagina informada (page)
            # Filtrando os registro de 3 em 3 (per_page)
            games_page = Game.query.paginate(page=page, per_page=per_page)

            return render_template('gamesestoque.html', gamesestoque=games_page)

    # CRUD GAMES - EDIÇÃO
    @app.route('/games/edit/<int:id>', methods=['GET', 'POST'])
    def gameEdit(id):
        g = Game.query.get(id)
        # Edita o jogo com as informações do formulário
        if request.method == 'POST':
            g.titulo = request.form['titulo']
            g.ano = request.form['ano']
            g.categoria = request.form['categoria']
            g.preco = request.form['preco']
            g.quantidade = request.form['quantidade']
            db.session.commit()
            return redirect(url_for('gamesEstoque'))
        return render_template('editgame.html', g=g)

    # CRUD CONSOLES - LISTAGEM, CADASTRO E EXCLUSÃO
    @app.route('/consoles/estoque', methods=['GET', 'POST'])
    @app.route('/consoles/estoque/delete/<int:id>')
    def consolesEstoque(id=None):
        if id:
            console = Console.query.get(id)
            # Deleta o console cadastro pela ID
            db.session.delete(console)
            db.session.commit()
            return redirect(url_for('consolesEstoque'))
        # Cadastra um novo console
        if request.method == 'POST':
            newconsole = Console(
                request.form['nome'], request.form['fabricante'], request.form['ano_lancamento'])
            db.session.add(newconsole)
            db.session.commit()
            return redirect(url_for('consolesEstoque'))
        else:
            # Captura o valor de 'page' que foi passado pelo método GET
            # Define como padrão o valor 1 e o tipo inteiro
            page = request.args.get('page', 1, type=int)
            # Valor padrão de registros por página (definimos 3)
            per_page = 3
            # Faz um SELECT no banco a partir da pagina informada (page)
            # Filtrando os registro de 3 em 3 (per_page)
            consoles_page = Console.query.paginate(
                page=page, per_page=per_page)
            return render_template('consolesestoque.html', consolesestoque=consoles_page)

    # CRUD CONSOLES - EDIÇÃO
    @app.route('/consoles/edit/<int:id>', methods=['GET', 'POST'])
    def consoleEdit(id):
        console = Console.query.get(id)
        # Edita o console com as informações do formulário
        if request.method == 'POST':
            console.nome = request.form['nome']
            console.fabricante = request.form['fabricante']
            console.ano_lancamento = request.form['ano_lancamento']
            db.session.commit()
            return redirect(url_for('consolesEstoque'))
        return render_template('editconsole.html', console=console)

    # ROTA de Catálogo de Jogos (Consumo da API)
    @app.route('/apigames', methods=['GET', 'POST'])
    @app.route('/apigames/<int:id>', methods=['GET', 'POST'])
    def apigames(id=None):
        urlApi = 'https://www.freetogame.com/api/games'
        response = urllib.request.urlopen(urlApi)
        apiData = response.read()
        listaJogos = json.loads(apiData)

        if id:
            gameInfo = []
            for jogo in listaJogos:
                if jogo['id'] == id:
                    gameInfo = jogo
                    break
            if gameInfo:
                return render_template('gameinfo.html',
                                           gameInfo=gameInfo)
            else:
                return f'Game com a id {id} não foi encontrado'

        return render_template('apigames.html', listaJogos=listaJogos)
