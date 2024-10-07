import mysql.connector
from datetime import datetime
#Se crea una clase que va a representar la venta
# atributos correspondiente fecha, clientes y productos
class Venta:
    def __init__(self, fecha, cliente, productos):
        self.fecha = fecha
        self.cliente = cliente
        self.productos = productos

    def to_dict(self):
        return {
            'fecha': self.fecha.strftime('%Y-%m-%d %H:%M:%S'),
            'cliente': self.cliente,
            'productos': self.productos
        }

class VentaOnline(Venta):
    def __init__(self, fecha, cliente, productos, direccion_envio, metodo_pago):
        super().__init__(fecha, cliente, productos)
        self.direccion_envio = direccion_envio
        self.metodo_pago = metodo_pago

    def to_dict(self):
        data = super().to_dict()
        data.update({
            'direccion_envio': self.direccion_envio,
            'metodo_pago': self.metodo_pago,
            'tipo': 'online'
        })
        return data

class VentaLocal(Venta):
    #Inicializa una nueva instancia de la clase Venta.__init__
    def __init__(self, fecha, cliente, productos, cajero, tienda):
        super().__init__(fecha, cliente, productos)
        self.cajero = cajero
        self.tienda = tienda

    def to_dict(self):    #Convierte la instancia de Venta a un diccionario.
        data = super().to_dict()
        data.update({
            'cajero': self.cajero,
            'tienda': self.tienda,
            'tipo': 'local'
        })
        return data
# db_config (dict): uso de un diccionario que contiene la configuración de conexión
#El método __init__ crea una instancia de la clase SistemaGestionVtas 
# y establece la conexión a la base de datos
class SistemaGestionVtas: 
    def __init__(self, db_config):
        self.db_config = db_config
        self.conn = mysql.connector.connect(**self.db_config)
        self.cursor = self.conn.cursor()
        self.crear_tablas()

    def crear_tablas(self):
        # Crea tablas en MySQL para las ventas generales, locales y online
        self.cursor.execute('''    
            CREATE TABLE IF NOT EXISTS ventas (
                id INT AUTO_INCREMENT PRIMARY KEY,
                fecha DATETIME,
                cliente VARCHAR(255),
                productos TEXT,
                tipo VARCHAR(50)
            )
        ''')

        self.cursor.execute('''        
            CREATE TABLE IF NOT EXISTS ventas_online (
                id INT AUTO_INCREMENT PRIMARY KEY,
                venta_id INT,
                direccion_envio VARCHAR(255),
                metodo_pago VARCHAR(255),
                FOREIGN KEY (venta_id) REFERENCES ventas(id)
            );
        ''')

        self.cursor.execute('''        
            CREATE TABLE IF NOT EXISTS ventas_locales (
                id INT AUTO_INCREMENT PRIMARY KEY,
                venta_id INT,
                cajero VARCHAR(255),
                tienda VARCHAR(255),
                FOREIGN KEY (venta_id) REFERENCES ventas(id)
            )
        ''')
        self.conn.commit()

    def agregar_venta(self, venta):
        # Inserta la venta en la tabla principal de ventas una nueva venta en la base de datos.
        try:
           
            venta_data = venta.to_dict()
            self.cursor.execute('''
                INSERT INTO ventas (fecha, cliente, productos, tipo)
                VALUES (%s, %s, %s, %s)
            ''', (venta_data['fecha'], venta_data['cliente'], str(venta_data['productos']), venta_data['tipo']))
            venta_id = self.cursor.lastrowid

            # Insertar detalles específicos para ventas online o locales
            if venta_data['tipo'] == 'online':
                self.cursor.execute('''
                    INSERT INTO ventas_online (venta_id, direccion_envio, metodo_pago)
                    VALUES (%s, %s, %s)
                ''', (venta_id, venta_data['direccion_envio'], venta_data['metodo_pago']))
            elif venta_data['tipo'] == 'local':
                self.cursor.execute('''
                    INSERT INTO ventas_locales (venta_id, cajero, tienda)
                    VALUES (%s, %s, %s)
                ''', (venta_id, venta_data['cajero'], venta_data['tienda']))

            self.conn.commit()
            print("Venta agregada exitosamente.")
        except mysql.connector.Error as e:
            print(f"Error al agregar la venta: {e}")

    def obtener_venta(self, venta_id):
        self.cursor.execute('SELECT * FROM ventas WHERE id = %s', (venta_id,))
        venta = self.cursor.fetchone()

        if venta:
            venta_dict = {
                'id': venta[0],
                'fecha': venta[1],
                'cliente': venta[2],
                'productos': venta[3],
                'tipo': venta[4]
            }

            if venta_dict['tipo'] == 'online':
                self.cursor.execute('SELECT * FROM ventas_online WHERE venta_id = %s', (venta_id,))
                venta_online = self.cursor.fetchone()
                if venta_online:
                    venta_dict.update({
                        'direccion_envio': venta_online[2],
                        'metodo_pago': venta_online[3]
                    })
            elif venta_dict['tipo'] == 'local':
                self.cursor.execute('SELECT * FROM ventas_locales WHERE venta_id = %s', (venta_id,))
                venta_local = self.cursor.fetchone()
                if venta_local:
                    venta_dict.update({
                        'cajero': venta_local[2],
                        'tienda': venta_local[3]
                    })

            return venta_dict
        else:
            print("Venta no encontrada")
            return None

    def actualizar_venta(self, venta_id, venta): #Este método actualiza los detalles de una venta en la base de datos. 
        venta_data = venta.to_dict()
        self.cursor.execute('''
            UPDATE ventas
            SET fecha = %s, cliente = %s, productos = %s, tipo = %s
            WHERE id = %s
        ''', (venta_data['fecha'], venta_data['cliente'], str(venta_data['productos']), venta_data['tipo'], venta_id))

        if venta_data['tipo'] == 'online':
            self.cursor.execute('''
                UPDATE ventas_online
                SET direccion_envio = %s, metodo_pago = %s
                WHERE venta_id = %s
            ''', (venta_data['direccion_envio'], venta_data['metodo_pago'], venta_id))
        elif venta_data['tipo'] == 'local':
            self.cursor.execute('''
                UPDATE ventas_locales
                SET cajero = %s, tienda = %s
                WHERE venta_id = %s
            ''', (venta_data['cajero'], venta_data['tienda'], venta_id))

        self.conn.commit()
    # Elimina una venta específica y los detalles correspondientes en las tablas de ventas online y locales 
    def eliminar_venta(self, venta_id):
        self.cursor.execute('DELETE FROM ventas WHERE id = %s', (venta_id,))
        self.cursor.execute('DELETE FROM ventas_online WHERE venta_id = %s', (venta_id,))
        self.cursor.execute('DELETE FROM ventas_locales WHERE venta_id = %s', (venta_id,))
        self.conn.commit()

    def borrar_todas_ventas(self): #Borra todas las ventas y sus detalles, vaciando las tablas relacionadas.
        self.cursor.execute('DELETE FROM ventas')
        self.cursor.execute('DELETE FROM ventas_online')
        self.cursor.execute('DELETE FROM ventas_locales')
        self.conn.commit()
        print("Todas las ventas han sido borradas.")
