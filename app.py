from flask import Flask, flash, redirect, render_template,request
from tempfile import mkdtemp
import sqlite3

# Configure application
app = Flask(__name__)

# Conectar a la base de datos
conn = sqlite3.connect("database.db")
c = conn.cursor()

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
@app.route('/')
@app.route('/index.html')
def index():
    return render_template('index.html')

@app.route('/agregar', methods=['GET', 'POST'])
def agregar():
    return render_template('agregar2.html')

@app.route('/agendando', methods=['POST'])
def agendar():
    if request.method == 'POST':
        primerNombre = request.form['primerNombre']
        segundoNombre = request.form['segundoNombre']
        primerApellido = request.form['primerApellido']
        segundoApellido = request.form['segundoApellido']
        cedula = request.form['cedula']
        telefono = request.form['telefono']
        fecha = request.form['calendario']
        hora = request.form['hora']
        servicio = request.form['servicio']
        descripcion = request.form['descripcion']
        
        nombreCompleto = f"{primerNombre} {segundoNombre}"
        apellidoCompleto = f"{primerApellido} {segundoApellido}"
        
        # Conectar a la base de datos
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        
        try:
            # Insertar paciente en la tabla pacientes
            c.execute('''
                INSERT INTO pacientes (nombre, apellido, celular, cedula)
                VALUES (?, ?, ?, ?)
            ''', (nombreCompleto, apellidoCompleto, telefono, cedula))
            
            conn.commit()
            
            # Obtener el ID del paciente recién insertado
            c.execute('''
                SELECT id FROM pacientes WHERE cedula = ?
            ''', (cedula,))
            paciente_id = c.fetchone()[0]  # Obtener el primer resultado
            
            # Insertar cita en la tabla citas
            c.execute('''
                INSERT INTO citas (paciente_id, servicio_id, fecha, hora, descripcion)
                VALUES (?, ?, ?, ?, ?)
            ''', (paciente_id, servicio, fecha, hora, descripcion))
            
            conn.commit()
            
            # Cerrar la conexión
            c.close()
            
            return render_template('agregar2.html')
        
        except sqlite3.Error as e:
            print(f"Error SQLite: {e}")
            conn.rollback()  # Revertir cambios si hay algún error
            
            # Puedes manejar el error y redirigir a una página de error
            return render_template('error.html', message="Error al agregar cita.")
    
    # Si no es una solicitud POST, redirigir o renderizar según tu lógica
    return render_template('agregar2.html')


if __name__ == '__main__':
    app.run(debug=True)
