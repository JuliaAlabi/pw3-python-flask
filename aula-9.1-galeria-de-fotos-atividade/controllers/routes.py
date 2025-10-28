from flask import render_template, request, url_for, redirect, flash, session
from models.database import db, Imagem
import urllib 
import json 
import os
import uuid

def init_app(app):
    @app.route('/')
    def home():
        ultimas_obras = Imagem.query.order_by(Imagem.id.desc()).limit(8).all()
    
        total_obras = Imagem.query.count()
        total_artistas = Imagem.query.distinct(Imagem.artista).count() if hasattr(Imagem, 'artista') else total_obras
        total_visitas = 10000  
    
        return render_template('index.html', 
                         ultimas_obras=ultimas_obras,
                         total_obras=total_obras,
                         total_artistas=total_artistas,
                         total_visitas=total_visitas)

    
    FILE_TYPES = set(['png', 'jpg', 'jpeg', 'gif'])
    def arquivos_permitidos(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in FILE_TYPES
    
    @app.route('/galeria', methods=['GET', 'POST'])
    def galeria():
        imagens = Imagem.query.all()
        if request.method == 'POST':
            file = request.files['file']
            nome_obra = request.form.get('nome_obra')
            
            if not arquivos_permitidos(file.filename):
                flash("Utilize os tipos de arquivos referentes a imagem.", 'danger')
                return redirect(request.url)
            
            if not nome_obra:
                flash("Por favor, informe o nome da obra.", 'danger')
                return redirect(request.url)

            file_extension = file.filename.rsplit('.', 1)[1].lower()

            filename = f"{str(uuid.uuid4())}.{file_extension}"

            img = Imagem(filename=filename, nome_obra=nome_obra)
            db.session.add(img)
            db.session.commit()
            
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash("Obra enviada com sucesso!", 'success')
            return redirect(url_for('galeria'))
        
        return render_template('galeria.html', imagens=imagens)