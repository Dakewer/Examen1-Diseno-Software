class ValidadorBiblioteca:

    @staticmethod
    def validar_libro(titulo, autor, isbn):
        if not titulo or len(titulo) <= 1:
            return "Error: Título inválido"
        if not autor or len(autor) <= 1:
            return "Error: Autor inválido"
        if not isbn or len(isbn) < 13:
            return "Error: ISBN inválido"
        return None

    @staticmethod
    def validar_usuario(usuario):
        if not usuario or len(usuario) <= 1:
            return "Error: Nombre de usuario inválido"
        return None

    @staticmethod
    def validar_prestamo(libro, usuario):
        if not libro:
            return "Error: Libro no encontrado"
        if not libro.disponible:
            return "Error: Libro no disponible"
        error_usuario = ValidadorBiblioteca.validar_usuario(usuario)
        if error_usuario:
            return error_usuario
        return None