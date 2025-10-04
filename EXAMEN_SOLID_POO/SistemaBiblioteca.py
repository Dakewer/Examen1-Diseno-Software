from biblioteca_examen import Libro, Prestamo
from busqueda import (
    BusquedaPorTitulo,
    BusquedaPorAutor,
    BusquedaPorISBN,
    BusquedaPorDisponibilidad
)

from ValidadorBiblioteca import ValidadorBiblioteca
from RepositorioBiblioteca import RepositorioBiblioteca
from ServicioNotificaciones import ServicioNotificaciones


class SistemaBiblioteca:
    def __init__(self):
        self.libros = []
        self.prestamos = []
        self.contador_libro = 1
        self.contador_prestamo = 1
        self.archivo = "biblioteca.txt"

        self.validador = ValidadorBiblioteca()
        self.repositorio = RepositorioBiblioteca()
        self.notificador = ServicioNotificaciones()

        self.estrategias_busqueda = {
            "titulo": BusquedaPorTitulo(),
            "autor": BusquedaPorAutor(),
            "isbn": BusquedaPorISBN(),
            "disponible": BusquedaPorDisponibilidad()
        }

    def agregar_libro(self, titulo, autor, isbn):
        error = self.validador.validar_libro(titulo, autor, isbn)
        if error:
            return error

        libro = Libro(self.contador_libro, titulo, autor, isbn)
        self.libros.append(libro)
        self.contador_libro += 1

        self.repositorio.guardar_estado(self.libros, self.prestamos)

        return f"Libro '{titulo}' agregado exitosamente"

    def buscar_libro(self, criterio, valor):

        if criterio not in self.estrategias_busqueda:
            return []

        estrategia = self.estrategias_busqueda[criterio]
        resultados = []

        for libro in self.libros:
            if estrategia.cumple_criterio(libro, valor):
                resultados.append(libro)

        return resultados

    def realizar_prestamo(self, libro_id, usuario):
        error_usuario = self.validador.validar_usuario(usuario)
        if error_usuario:
            return error_usuario

        libro = self.repositorio.buscar_libro_por_id(self.libros, libro_id)

        error_prestamo = self.validador.validar_prestamo(libro, usuario)
        if error_prestamo:
            return error_prestamo

        from datetime import datetime
        prestamo = Prestamo(
            self.contador_prestamo,
            libro_id,
            usuario,
            datetime.now().strftime("%Y-%m-%d")
        )

        self.prestamos.append(prestamo)
        self.contador_prestamo += 1
        libro.disponible = False
        self.repositorio.guardar_estado(self.libros, self.prestamos)
        self.notificador.enviar_notificacion_prestamo(usuario, libro.titulo)

        return f"Préstamo realizado a {usuario}"

    def devolver_libro(self, prestamo_id):
        prestamo = self.repositorio.buscar_prestamo_por_id(self.prestamos, prestamo_id)

        if not prestamo:
            return "Error: Préstamo no encontrado"

        if prestamo.devuelto:
            return "Error: Libro ya devuelto"

        libro = self.repositorio.buscar_libro_por_id(self.libros, prestamo.libro_id)
        if libro:
            libro.disponible = True

        prestamo.devuelto = True

        self.repositorio.guardar_estado(self.libros, self.prestamos)

        if libro:
            self.notificador.enviar_notificacion_devolucion(prestamo.usuario, libro.titulo)

        return "Libro devuelto exitosamente"

    def obtener_todos_libros(self):
        return self.libros

    def obtener_libros_disponibles(self):
        return [libro for libro in self.libros if libro.disponible]

    def obtener_prestamos_activos(self):
        return [p for p in self.prestamos if not p.devuelto]

    def _guardar_en_archivo(self):
        with open(self.archivo, 'w') as f:
            f.write(f"Libros: {len(self.libros)}\n")
            f.write(f"Préstamos: {len(self.prestamos)}\n")

    def _cargar_desde_archivo(self):
        try:
            with open(self.archivo, 'r') as f:
                data = f.read()
            return True
        except:
            return False

    def _enviar_notificacion(self, usuario, libro):
        print(f"[NOTIFICACIÓN] {usuario}: Préstamo de '{libro}'")


"""

        BLOQUE  MAIN NO TOCAR

"""

def main():
    sistema = SistemaBiblioteca()

    print("=== AGREGANDO LIBROS ===")
    print(sistema.agregar_libro("Cien Años de Soledad", "Gabriel García Márquez", "9780060883287"))
    print(sistema.agregar_libro("El Principito", "Antoine de Saint-Exupéry", "9780156012195"))
    print(sistema.agregar_libro("1984", "George Orwell", "9780451524935"))

    print("\n=== BÚSQUEDA POR AUTOR ===")
    resultados = sistema.buscar_libro("autor", "Garcia")
    for libro in resultados:
        print(f"- {libro.titulo} por {libro.autor}")

    print("\n=== REALIZAR PRÉSTAMO ===")
    print(sistema.realizar_prestamo(1, "Juan Pérez"))

    print("\n=== LIBROS DISPONIBLES ===")
    disponibles = sistema.obtener_libros_disponibles()
    for libro in disponibles:
        print(f"- {libro.titulo}")

    print("\n=== DEVOLVER LIBRO ===")
    print(sistema.devolver_libro(1))

    print("\n=== PRÉSTAMOS ACTIVOS ===")
    activos = sistema.obtener_prestamos_activos()
    print(f"Total de préstamos activos: {len(activos)}")


if __name__ == "__main__":
    main()
