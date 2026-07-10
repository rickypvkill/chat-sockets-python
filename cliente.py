import socket
import threading

HOST = input("IP del servidor: ")
PORT = 5000

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def recibir_mensajes():
    while True:
        try:
            mensaje = client.recv(1024).decode()
            print("\n" + mensaje)
        except:
            break


client.connect((HOST, PORT))

nombre = input("Ingrese su nombre: ")

client.send(nombre.encode())

respuesta = client.recv(1024).decode()

if respuesta == "ERROR":
    print("❌ El nombre ya está en uso.")
    client.close()

elif respuesta == "OK":

    print("✅ Conectado al servidor.")

    hilo_recibir = threading.Thread(target=recibir_mensajes)
    hilo_recibir.daemon = True
    hilo_recibir.start()

    while True:
        mensaje = input()
        if mensaje == "/salir":
            client.close()
            break
        client.send(mensaje.encode())