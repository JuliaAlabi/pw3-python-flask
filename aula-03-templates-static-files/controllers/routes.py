from flask import render_template, request, redirect, url_for

jogadores = ['Julia', 'Yasmin', 'Millie']

gamelist = [{
            'titulo': 'cs-go',
            'ano': 2012,
            'categoria': 'FPS Online'
            }]
consolelist = [{
            'nome': 'xbox 360',
            'fabricante': 'microsoft',
            'ano': 2005,
            'preco': 2000
}]


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

        jogos = ['Roblox', 'Minecraft',  'Talking Tom',
                 'Tetris', 'Super Mario Bros', 'Pacman']

        return render_template('games.html',
                               game=game,
                               jogadores=jogadores,
                               jogos=jogos)

    @app.route('/cadgames', methods=['GET', 'POST'])
    def cadgames():
        if request.method == 'POST':
            if request.form.get('titulo') and request.form.get('ano') and request.form.get('categoria'):
                gamelist.append({'titulo': request.form.get('titulo'), 'ano': request.form.get(
                    'ano'), 'categoria': request.form.get('categoria')})
                return redirect(url_for('cadgames'))
        return render_template('cadgames.html',
                               gamelist=gamelist)
        
    @app.route('/console', methods=['GET', 'POST'])
    def cadconsole():
        if request.method == 'POST':
            if request.form.get('nome') and request.form.get('fabricante') and request.form.get('ano') and request.form.get('preco'):
                consolelist.append({'nome': request.form.get('nome'), 'fabricante': request.form.get('fabricante'), 'ano': request.form.get('ano'), 'preco':
                request.form.get('preco')})
                return redirect(url_for('cadconsole'))
        return render_template('cadconsole.html',
                               consolelist=consolelist)
                
