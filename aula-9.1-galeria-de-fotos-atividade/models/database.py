from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Imagem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(120), unique=True, nullable=False)
    nome_obra = db.Column(db.String(100), nullable=False)  
    
    def __init__(self, filename, nome_obra, artista='Artista Anônimo'):
        self.filename = filename
        self.nome_obra = nome_obra
