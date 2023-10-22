import socket
import sqlite3

class Servidor:
    def __init__(self):
        self.server_address = ('localhost', 5000)
        self.conn = sqlite3.connect('arqui.bd')
        self.cursor = self.conn.cursor()

    def handle_request(self, client_socket):
        data_length = int(client_socket.recv(5).decode())
        data = client_socket.recv(data_length).decode()
        service_name = data[:5]
        data_content = data[5:]

        if service_name == "regusr":
            datos = data_content.split(',')
            try:
                self.cursor.execute("INSERT INTO Usuario (nombre, email, contraseña, rol_id, codigo_personal, QR) VALUES (?, ?, ?, ?, ?, ?)", datos)
                self.conn.commit()
                response = "OKRegistro exitoso"
            except Exception as e:
                response = f"NK{str(e)}"
            client_socket.sendall(f"{len(response):05}{response}".encode())

    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind(self.server_address)
            server_socket.listen()
            print(f"Servidor escuchando en {self.server_address}")
            while True:
                client_socket, client_address = server_socket.accept()
                self.handle_request(client_socket)
                client_socket.close()

if __name__ == "__main__":
    server = Servidor()
    server.run()
