from flask import render_template, request, url_for, redirect, flash, session
from models.database import db, Game, Console, Usuario, Imagem
import urllib 
import json 
from werkzeug.security import generate_password_hash, check_password_hash
import os
import uuid

jogadores = ['Miguel José', 'Miguel Isack', 'Leaf',
             'Quemario', 'Trop', 'Aspax', 'maxxdiego']
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

    @app.route('/games/estoque', methods=['GET', 'POST'])
    @app.route('/games/estoque/delete/<int:id>')
    def gamesEstoque(id=None):
        if id:
            game = Game.query.get(id)
            db.session.delete(game)
            db.session.commit()
            return redirect(url_for('gamesEstoque'))
        if request.method == 'POST':
            newgame = Game(request.form['titulo'], request.form['ano'], request.form['categoria'],
                           request.form['preco'], request.form['quantidade'], request.form['console'])
            db.session.add(newgame)
            db.session.commit()
            return redirect(url_for('gamesEstoque'))
        else:
            page = request.args.get('page', 1, type=int)
            per_page = 3
            games_page = Game.query.paginate(page=page, per_page=per_page)
            
            consoles = Console.query.all()
                       
            return render_template('gamesestoque.html', gamesestoque=games_page, consoles=consoles)

    @app.route('/games/edit/<int:id>', methods=['GET', 'POST'])
    def gameEdit(id):
        g = Game.query.get(id)
        if request.method == 'POST':
            g.titulo = request.form['titulo']
            g.ano = request.form['ano']
            g.categoria = request.form['categoria']
            
            g.console_id = request.form['console']
            
            g.preco = request.form['preco']
            g.quantidade = request.form['quantidade']
            db.session.commit()
            return redirect(url_for('gamesEstoque'))
        
        consoles = Console.query.all()
        return render_template('editgame.html', g=g, consoles=consoles)

    @app.route('/consoles/estoque', methods=['GET', 'POST'])
    @app.route('/consoles/estoque/delete/<int:id>')
    def consolesEstoque(id=None):
        if id:
            console = Console.query.get(id)
            db.session.delete(console)
            db.session.commit()
            return redirect(url_for('consolesEstoque'))
        
        if request.method == 'POST':
            newconsole = Console(request.form['nome'], request.form['fabricante'], request.form['ano_lancamento'])
            db.session.add(newconsole)
            db.session.commit()
            return redirect(url_for('consolesEstoque'))
        else:
            page = request.args.get('page', 1, type=int)
            per_page = 3
            consoles_page = Console.query.paginate(page=page, per_page=per_page)
            return render_template('consolesestoque.html', consolesestoque=consoles_page)

    @app.route('/consoles/edit/<int:id>', methods=['GET', 'POST'])
    def consoleEdit(id):
        console = Console.query.get(id)
        if request.method == 'POST':
            console.nome = request.form['nome']
            console.fabricante = request.form['fabricante']
            console.ano_lancamento = request.form['ano_lancamento']
            db.session.commit()
            return redirect(url_for('consolesEstoque'))
        return render_template('editconsole.html', console=console)
    

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
                return render_template('gameinfo.html', gameInfo=gameInfo)
            else:
                return f'Game com a ID {id} não foi encontrado.'        
        return render_template('apigames.html', listaJogos=listaJogos)

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method=='POST':
            email = request.form['email']
            senha = request.form['senha']
            
            user = Usuario.query.filter_by(email=email).first()
            
            if user and check_password_hash(user.senha, senha):
                session ['user_id'] = user.id
                session ['user_email'] = user.email
                flash(f'Login realizado com sucesso! Bem vindo {user.nome}', 'success')
                return redirect(url_for('home'))
            else: 
                flash ("Falha no login! Verifique o nome do usuário e tente novamente")
                return redirect(url_for('login'))
        return render_template('login.html')

    @app.route('/caduser', methods=['GET', 'POST'])
    def caduser():
        if request.method== 'POST':
            nome = request.form['nome']
            email = request.form ['email']
            senha = request.form ['senha']
            
            user = Usuario.query.filter_by(email=email).first()
            if user:
                flash("Usuário já cadastrado! Faça login!")
                
            else: 
                hashed_password= generate_password_hash(senha, method='scrypt')
                new_user = Usuario(nome=nome, email=email, senha=hashed_password)
                db.session.add(new_user)
                db.session.commit()
                flash("Cadastro realizado com sucesso! Faça o login", "success")
                return redirect(url_for('login'))
        return render_template('caduser.html')
    
    FILE_TYPES = set(['png', 'jpg', 'jpeg', 'gif'])
    def arquivos_permitidos(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in FILE_TYPES
    
    @app.route('/galeria', methods=['GET', 'POST'])
    def galeria():
        imagens = Imagem.query.all()
        if request.method == 'POST':
            file=request.files['file']
            if not arquivos_permitidos(file.filename):
                flash("Utilize os tipos de arquivos referentes a imagem.", 'danger')
                return redirect(request.url)
            
            filename = str(uuid.uuid4())
            
            img = Imagem(filename)
            db.session.add(img)
            db.session.commit()
            
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash("Imagem enviada com sucesso!", 'success')
        return render_template('galeria.html', imagens=imagens)