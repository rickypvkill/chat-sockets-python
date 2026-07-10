import socket
import threading
from datetime import datetime

HOST = "0.0.0.0"
PORT = 5000

usuarios = {}
def broadcast(mensaje):
    for socket_cliente in usuarios.values():
        try:
            socket_cliente.send(mensaje.encode())
        except:
            pass

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

print(f"Servidor escuchando en puerto {PORT}...")

def obtener_hora():
    return datetime.now().strftime("%H:%M")

def manejar_cliente(client_socket, nombre):

    print(f"-Hilo iniciado para {nombre}")

    while True:

        try:
            mensaje = client_socket.recv(1024).decode()

            if not mensaje:
                break

            mensaje_completo = f"[{obtener_hora()}] {nombre}: {mensaje}"

            print(mensaje_completo)

            broadcast(mensaje_completo)

        except:
            break

    print(f"\n[DESCONEXIÓN]")
    print(f"Usuario: {nombre}")

    if nombre in usuarios:
        del usuarios[nombre]

    mensaje_sistema = f"*** {nombre} se ha desconectado ***"

    broadcast(mensaje_sistema)

    print("\nUsuarios conectados:")
    for usuario in usuarios:
        print(f"- {usuario}")

    client_socket.close()


while True:
    client_socket, address = server.accept()

    nombre = client_socket.recv(1024).decode()

    if nombre in usuarios:
        client_socket.send("ERROR".encode())
        client_socket.close()
        print(f"Intento rechazado: {nombre}")
        continue

    usuarios[nombre] = client_socket

    client_socket.send("OK".encode())

    # Log del servidor
    print(f"\n[NUEVA CONEXIÓN]")
    print(f"Usuario: {nombre}")
    print(f"Dirección: {address}")

    # Mensaje para los clientes
    mensaje_sistema = f"[{obtener_hora()}] *** {nombre} se ha conectado ***"

    broadcast(mensaje_sistema)

    print("\nUsuarios conectados:")
    for usuario in usuarios:
        print(f"- {usuario}")

    # Crear hilo para el cliente
    hilo = threading.Thread(
        target=manejar_cliente,
        args=(client_socket, nombre)
    )

    hilo.start()
#127.0.0.1