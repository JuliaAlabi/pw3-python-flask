# importando o flask
from flask import Flask, render_template

from controllers import routes

# carregando o flask na variavel app
app = Flask(__name__, template_folder='views')

routes.init_app(app)

if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
