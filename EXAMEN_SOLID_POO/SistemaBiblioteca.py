"""
Sistema de Biblioteca Refactorizado - Implementación OCP
"""

from biblioteca_examen import Libro, Prestamo
from busqueda import (
    Busqueda,
    BusquedaPorTitulo,
    BusquedaPorAutor,
    BusquedaPorISBN,
    BusquedaPorDisponibilidad
)


class SistemaBiblioteca:
    def __init__(self):
        self.libros = []
        self.prestamos = []
        self.contador_libro = 1
        self.contador_prestamo = 1
        self.archivo = "biblioteca.txt"

        # Mapeo de estrategias de búsqueda - FÁCIL DE EXTENDER
        self.Busqueda = {
            "titulo": BusquedaPorTitulo(),
            "autor": BusquedaPorAutor(),
            "isbn": BusquedaPorISBN(),
            "disponible": BusquedaPorDisponibilidad()
        }

    def agregar_libro(self, titulo, autor, isbn):
        if not titulo or len(titulo) < 2:
            return "Error: Título inválido"
        if not autor or len(autor) < 3:
            return "Error: Autor inválido"
        if not isbn or len(isbn) < 10:
            return "Error: ISBN inválido"

        libro = Libro(self.contador_libro, titulo, autor, isbn)
        self.libros.append(libro)
        self.contador_libro += 1
        self._guardar_en_archivo()

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
        if not usuario or len(usuario) < 3:
            return "Error: Nombre de usuario inválido"

        libro = None
        for l in self.libros:
            if l.id == libro_id:
                libro = l
                break

        if not libro:
            return "Error: Libro no encontrado"

        if not libro.disponible:
            return "Error: Libro no disponible"

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
        self._guardar_en_archivo()
        self._enviar_notificacion(usuario, libro.titulo)

        return f"Préstamo realizado a {usuario}"

    def devolver_libro(self, prestamo_id):
        prestamo = None
        for p in self.prestamos:
            if p.id == prestamo_id:
                prestamo = p
                break

        if not prestamo:
            return "Error: Préstamo no encontrado"

        if prestamo.devuelto:
            return "Error: Libro ya devuelto"

        for libro in self.libros:
            if libro.id == prestamo.libro_id:
                libro.disponible = True
                break

        prestamo.devuelto = True
        self._guardar_en_archivo()

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