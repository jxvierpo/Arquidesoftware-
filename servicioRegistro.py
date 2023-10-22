import socket

class ServidorAcceso:
    def __init__(self, host='localhost', port=5000):
        self.server_address = (host, port)
        # Un simple diccionario para mantener el estado de los trabajadores
        # True indica que el trabajador está dentro y False indica que está fuera.
        self.trabajadores = {}

    def handle_request(self, data):
        service_name = data[5:10]
        id_trabajador = data[10:]
        print(data)

        # Longitudes conocidas
        len_service_name = 5
        len_resp = 2

        if service_name == "regis":
            if id_trabajador not in self.trabajadores:
                self.trabajadores[id_trabajador] = False
                total_length = len_service_name + len_resp + len(id_trabajador)
                return f"{total_length:05}{service_name}OK{id_trabajador}"
            else:
                total_length = len_service_name + len_resp + len(id_trabajador)
                return f"{total_length:05}{service_name}NK{id_trabajador}"
        
        elif service_name == "regus":
            datos = data_content.split(',')
            try:
                self.cursor.execute("INSERT INTO Usuario (nombre, email, contraseña, rol_id, codigo_personal, QR) VALUES (?, ?, ?, ?, ?, ?)", datos)
                self.conn.commit()
                response = "OKRegistro exitoso"
            except Exception as e:
                response = f"NK{str(e)}"
            return f"{len(response):05}{response}"

        elif service_name == "ingre":
            if id_trabajador in self.trabajadores:
                if not self.trabajadores[id_trabajador]:  # si el trabajador no está dentro
                    self.trabajadores[id_trabajador] = True
                    total_length = len_service_name + len_resp + len(id_trabajador)
                    return f"{total_length:05}{service_name}OK{id_trabajador}"
                else:
                    total_length = len_service_name + len_resp + len(id_trabajador)
                    return f"{total_length:05}{service_name}NK{id_trabajador}"
            else:
                total_length = len_service_name + len_resp + len(id_trabajador)
                return f"{total_length:05}{service_name}NK{id_trabajador}"

        elif service_name == "salid":
            if id_trabajador in self.trabajadores:
                if self.trabajadores[id_trabajador]:  # si el trabajador  está dentro
                    self.trabajadores[id_trabajador] = False
                    total_length = len_service_name + len_resp + len(id_trabajador)
                    return f"{total_length:05}{service_name}OK{id_trabajador}"
                else:
                    total_length = len_service_name + len_resp + len(id_trabajador)
                    return f"{total_length:05}{service_name}NK{id_trabajador}"
            else:
                total_length = len_service_name + len_resp + len(id_trabajador)
                return f"{total_length:05}{service_name}NK{id_trabajador}"
            

    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(self.server_address)
            s.listen(1)
            print(f"Servidor iniciado en {self.server_address}")
            while True:
                conn, addr = s.accept()
                with conn:
                    data = conn.recv(1024)
                    response = self.handle_request(data.decode())
                    print(response)
                    conn.sendall(response.encode())

if __name__ == "__main__":
    servidor = ServidorAcceso()
    servidor.run()
