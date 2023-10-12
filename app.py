from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ejemplo.db'  # Nombre de la base de datos
db = SQLAlchemy(app)

class Tarea(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(200), nullable=False)

#Rutas
@app.route('/')
def index():
    with app.app_context():
        tareas = Tarea.query.all()
    return render_template('index.html', tareas=tareas)

@app.route('/agregar_tarea', methods=['GET', 'POST'])
def agregar_tarea():
    if request.method == 'POST':    
        tarea_descripcion = request.form['descripcion']
        nueva_tarea = Tarea(descripcion=tarea_descripcion)
        db.session.add(nueva_tarea)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('agregar_tarea.html')

@app.route('/eliminar_tarea/<int:id>', methods=['GET'])
def eliminar_tarea(id):
    tarea = Tarea.query.get(id)
    if tarea:
        db.session.delete(tarea)
        db.session.commit()
    return redirect(url_for('index'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
