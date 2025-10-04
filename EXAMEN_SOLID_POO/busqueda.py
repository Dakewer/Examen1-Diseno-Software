from abc import ABC, abstractmethod
from biblioteca_examen import Libro

class Busqueda(ABC):
    @abstractmethod
    def cumple_criterio(self, libro: Libro, valor: str) -> bool:
        pass

class BusquedaPorTitulo(Busqueda):
    def cumple_criterio(self, libro: Libro, valor: str) -> bool:
        return valor.lower() in libro.titulo.lower()

class BusquedaPorAutor(Busqueda):
    def cumple_criterio(self, libro: Libro, valor: str) -> bool:
        return valor.lower() in libro.autor.lower()

class BusquedaPorISBN(Busqueda):
    def cumple_criterio(self, libro: Libro, valor: str) -> bool:
        return libro.isbn == valor

class BusquedaPorDisponibilidad(Busqueda):
    def cumple_criterio(self, libro: Libro, valor: str) -> bool:
        disponible = valor.lower() == "true"
        return libro.disponible == disponible
