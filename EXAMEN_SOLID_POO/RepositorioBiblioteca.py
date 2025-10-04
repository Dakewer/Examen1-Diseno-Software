class RepositorioBiblioteca:

    def __init__(self, archivo="biblioteca.txt"):
        self.archivo = archivo

    def guardar_estado(self, libros, prestamos):
        try:
            with open(self.archivo, 'w') as f:
                f.write(f"Libros: {len(libros)}\n")
                f.write(f"Préstamos: {len(prestamos)}\n")
            return True
        except Exception as e:
            print(f"Error guardando: {e}")
            return False

    def cargar_estado(self):
        try:
            with open(self.archivo, 'r') as f:
                data = f.read()
            return True
        except:
            return False

    def buscar_libro_por_id(self, libros, libro_id):
        for libro in libros:
            if libro.id == libro_id:
                return libro
        return None

    def buscar_prestamo_por_id(self, prestamos, prestamo_id):
        for prestamo in prestamos:
            if prestamo.id == prestamo_id:
                return prestamo
        return None