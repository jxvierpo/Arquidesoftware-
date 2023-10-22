import socket

class Acceso:
    def __init__(self):
        self.server_address = ('localhost', 5000)
        
    def send_request(self, service_name, data):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect(self.server_address)

            transaction = f"{(len(service_name) + len(data)):05}{service_name}{data}"
            print(transaction)
            sock.sendall(transaction.encode())

            amount_received = 0
            amount_expected = int(sock.recv(5).decode())
            response = ""
            while amount_received < amount_expected:
                
                data = sock.recv(amount_expected - amount_received).decode()
                amount_received += len(data)
                response += data
            print(response)    
            
        status = response[5:7]  # OK o NK
        data_response = response[7:]
        
        return status, data_response

    def registrar_trabajador(self, id_trabajador):
        status, response = self.send_request("regis", id_trabajador)
        if status == "OK":
            '''
            print(f"Solicitud de registro para el trabajador {id_trabajador} aceptada.")
            nombre = input("Ingrese el nombre del trabajador: ")
            email = input("Ingrese el email del trabajador: ")
            contraseña = input("Ingrese la contraseña del trabajador: ")
            rol_id = input("Ingrese el rol_id del trabajador: ")
            codigo_personal = input("Ingrese el código personal del trabajador: ")
            QR = input("Ingrese el QR del trabajador: ")

            data = f"{nombre},{email},{contraseña},{rol_id},{codigo_personal},{QR}"
            status, response = self.send_request("regus", data)
            '''
            print(f"Trabajador {id_trabajador} registrado correctamente.")
            '''
            if status == "OK":
                print(f"Trabajador {id_trabajador} registrado correctamente.")
            else:
                print(f"Error al registrar al trabajador {nombre}: {response}")
            '''
        
        else:
            print(f"Error al solicitar registro para el trabajador {id_trabajador}: {response}")

    def ingreso(self, id_trabajador):
        status, response = self.send_request("ingre", id_trabajador)
        if status == "OK":
            print(f"Trabajador {id_trabajador} ingresó correctamente.")
        else:
            print(f"Error en el ingreso del trabajador {id_trabajador}: {response}")

    def salida(self, id_trabajador):
        status, response = self.send_request("salid", id_trabajador)
        if status == "OK":
            print(f"Trabajador {id_trabajador} salió correctamente.")
        else:
            print(f"Error en la salida del trabajador {id_trabajador}: {response}")

    def verificar_estado(self, id_trabajador):
        status, response = self.send_request("estad", id_trabajador)
        if status == "OK":
            print(f"Estado del trabajador {id_trabajador}: {response}")
        else:
            print(f"Error al verificar el estado del trabajador {id_trabajador}: {response}")




if __name__ == "__main__":
    control_acceso = Acceso()

    while True:
        print("\n--- Sistema de Control de Acceso ---")
        print("1. Registrar trabajador")
        print("2. Ingreso de trabajador")
        print("3. Salida de trabajador")
        print("4. Verificar estado del trabajador")
        print("5. Salir")

        opcion = int(input("Seleccione una opción: "))

        if opcion == 1:
            id_trabajador = input("Ingrese ID del trabajador: ")
            control_acceso.registrar_trabajador(id_trabajador)
        elif opcion == 2:
            id_trabajador = input("Ingrese ID del trabajador: ")
            control_acceso.ingreso(id_trabajador)
        elif opcion == 3:
            id_trabajador = input("Ingrese ID del trabajador: ")
            control_acceso.salida(id_trabajador)
        elif opcion == 4:
            id_trabajador = input("Ingrese ID del trabajador: ")
            control_acceso.verificar_estado(id_trabajador)
        elif opcion == 5:
            break
