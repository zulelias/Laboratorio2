import mysql.connector
from datetime import datetime
from gestion_ventas import SistemaGestionVtas, VentaOnline, VentaLocal  # Asegúrate de que el nombre de tu archivo sea correcto

# Configuración de la base de datos
db_config = {
    'host': 'localhost',
    'user': 'root',        # Reemplazar el usuario y contraseña de MySQL
    'password': 'XXXXX',    
    'database': 'gestorventas'  
}
#Función principal que inicializa el sistema de gestión de ventas y presenta un menú al usuario
  #  para agregar ventas online o locales.
def main():
    sistema = SistemaGestionVtas(db_config) # Instancia del sistema de gestión de ventas
     #Bucle que muestra el menú y permite al usuario elegir entre agregar ventas o salir.   
    while True:
        print("\nOpciones:")
        print("1. Agregar venta online")
        print("2. Agregar venta local")
        print("3. Salir")
        
        opcion = input("Selecciona una opción (1, 2 o 3): ")
       
        if opcion == '1':
            # Obtener detalles de la venta online
            fecha = datetime.now()
            cliente = input("Nombre del cliente: ")
            productos = input("Productos (separados por comas): ")
            direccion_envio = input("Dirección de envío: ")
            metodo_pago = input("Método de pago: ")
            venta_online = VentaOnline(fecha, cliente, productos, direccion_envio, metodo_pago)
            sistema.agregar_venta(venta_online) # Llama al método para agregar la venta en la base de datos.
            print("Venta online agregada.")

        elif opcion == '2':
            # Obtener detalles de la venta local
            fecha = datetime.now()
            cliente = input("Nombre del cliente: ")
            productos = input("Productos (separados por comas): ")
            cajero = input("Nombre del cajero: ")
            tienda = input("Nombre de la tienda: ")
            venta_local = VentaLocal(fecha, cliente, productos, cajero, tienda)
            sistema.agregar_venta(venta_local) #Llama al método para agregar la venta en la base de datos.
            print("Venta local agregada.")

        elif opcion == '3':
            print("Saliendo del sistema...")
            break
        else:
            print("Opción no válida, por favor selecciona de nuevo.")
# Este bloque verifica si el archivo se está ejecutando directamente (no como módulo),
# y si es así, llama a la función main() para iniciar el programa.
if __name__ == "__main__":
    main()
