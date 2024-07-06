import sqlite3

# Conectar a la base de datos
conn = sqlite3.connect("database.db")
c = conn.cursor()

# Crear la tabla pacientes si no existe
c.execute('''
CREATE TABLE IF NOT EXISTS pacientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    apellido TEXT NOT NULL,
    celular TEXT,
    cedula TEXT
)
''')

# Crear la tabla servicio si no existe
c.execute('''
CREATE TABLE IF NOT EXISTS servicio (
    id INTEGER PRIMARY KEY,
    nombreServicio TEXT NOT NULL
)
''')


c.execute('''
    INSERT INTO servicio (id, nombreServicio)
    VALUES
        (1, 'Odontología Preventiva'),
        (2, 'Rehabilitación Oral y Estética Dental'),
        (3, 'Implantología Quirúrgica y Protésica'),
        (4, 'Periodoncia'),
        (5, 'Ortodoncia'),
        (6, 'Endodoncia')
    ''')

# Crear la tabla citas con llaves foráneas que referencian a pacientes(id) y servicio(id)
c.execute('''
CREATE TABLE IF NOT EXISTS citas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    paciente_id INTEGER NOT NULL,
    servicio_id INTEGER NOT NULL,
    fecha DATE NOT NULL,
    hora TEXT NOT NULL,
    descripcion TEXT,
    FOREIGN KEY (paciente_id) REFERENCES pacientes(id),
    FOREIGN KEY (servicio_id) REFERENCES servicio(id)
)
''')

conn.commit()
conn.close()
