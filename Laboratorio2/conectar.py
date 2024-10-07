import mysql.connector
from mysql.connector import Error

def crear_conexion():
    """Establece la conexión con la base de datos MySQL."""
    try:
        conexion = mysql.connector.connect(
            host='localhost',
            user='root',          # Cambia por tu usuario de MySQL
            password='XXXXX'      # Cambia por tu contraseña de MySQL
        )
        if conexion.is_connected():
            print("Conexión exitosa a la base de datos")
            return conexion
    except Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None

def crear_base_de_datos(conexion):
    """Crea una base de datos si no existe."""
    try:
        cursor = conexion.cursor()
        cursor.execute('CREATE DATABASE IF NOT EXISTS gestorventas')  # Cambia el nombre según necesites
        print("Base de datos creada o ya existe.")
    except Error as e:
        print(f"Error al crear la base de datos: {e}")

def crear_tablas(conexion):
    """Crea las tablas necesarias."""
    try:
        cursor = conexion.cursor()
        cursor.execute(""" 
            CREATE TABLE IF NOT EXISTS ventas (
                id INT AUTO_INCREMENT PRIMARY KEY,
                fecha DATETIME NOT NULL,
                cliente VARCHAR(255) NOT NULL,
                productos TEXT NOT NULL,
                direccion_envio VARCHAR(255),
                metodo_pago VARCHAR(50),
                cajero VARCHAR(255),                       
                tienda VARCHAR(255),
                tipo VARCHAR(50)    
            )
        """)
        print("Tabla 'ventas' creada o ya existe.")
    except Error as e:
        print(f"Error al crear la tabla: {e}")

def inicializar_bd():
    """Función para inicializar la base de datos y tablas."""
    conexion = crear_conexion()
    if conexion:
        crear_base_de_datos(conexion)
        # Cambia la base de datos actual a "gestorventas"
        conexion.database = 'gestorventas'
        crear_tablas(conexion)
        conexion.close()

# Ejecutar la función para inicializar la base de datos
inicializar_bd()
