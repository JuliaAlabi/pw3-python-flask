#importando o flask
from flask import Flask

#carregando o flask na variavel app
app = Flask(__name__)

@app.route('/')
def home ():
    return '<h1>Bem vindo ao meu primeiro site em flask</h1>'

#iniciando o servidor no locaçhost, porta 5000, modo de depuração ativado
if __name__ == '__main__':
 app.run(host='localhost', port=5000, debug=True)