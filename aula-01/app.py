# importando o flask
from flask import Flask, render_template

# carregando o flask na variavel app
app = Flask(__name__, template_folder='views')


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/games')
def games():
    titulo= 'cs-go'
    ano= 2012
    categoria = 'FPS Online'
    jogadores = ['Julia', 'Yasmin', 'Millie']
    jogos =['Roblox', 'Minecraft', 'Talking Tom', 'Tetris', 'Super Mario Boss', 'Pacman']
    return render_template('games.html',
                           titulo= titulo,
                           ano=ano,
                           categoria=categoria,
                           jogadores=jogadores,
                           jogos=jogos)


# iniciando o servidor no locaçhost, porta 5000, modo de depuração ativado
if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
