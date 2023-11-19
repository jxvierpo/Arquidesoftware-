import sqlite3

class ServicioInformes:
    def __init__(self):
        self.conn = sqlite3.connect('db/arqui.db')  

    def consultar_personas_ingresadas_hoy(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM registro WHERE fecha_hora >= DATE('now') AND registro = 'Ingreso'")
        resultado = cursor.fetchone()
        return resultado[0]

    def consultar_cantidad_personas_recinto(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT COUNT(DISTINCT user_id) 
            FROM registro 
            WHERE registro = 'Ingreso' AND user_id NOT IN (
                SELECT user_id 
                FROM registro 
                WHERE registro = 'Salida' AND fecha_hora >= (
                    SELECT MAX(fecha_hora) 
                    FROM registro 
                    WHERE registro = 'Ingreso'
                )
            )
        """)
        resultado = cursor.fetchone()
        return resultado[0]

    def consultar_cantidad_personas_piso(self, piso):
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT COUNT(DISTINCT r.user_id) 
            FROM registro r 
            JOIN usuario u ON r.user_id = u.id 
            JOIN area a ON u.area_id = a.id 
            WHERE r.registro = 'Ingreso' AND a.piso = ? AND r.user_id NOT IN (
                SELECT user_id 
                FROM registro 
                WHERE registro = 'Salida' AND fecha_hora >= (
                    SELECT MAX(fecha_hora) 
                    FROM registro 
                    WHERE registro = 'Ingreso'
                )
            )
        """, (piso,))
        resultado = cursor.fetchone()
        return resultado[0]

    def consultar_historial_trabajador(self, id_trabajador):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM registro WHERE user_id = ?", (id_trabajador,))
        resultados = cursor.fetchall()
        return resultados

'''
informes = ServicioInformes()
print("Personas ingresadas hoy:", informes.consultar_personas_ingresadas_hoy())
print("Cantidad de personas en el recinto:", informes.consultar_cantidad_personas_recinto())
print("Cantidad de personas en el piso 2:", informes.consultar_cantidad_personas_piso(2))
print("Historial del trabajador con ID 123:", informes.consultar_historial_trabajador(123))
'''