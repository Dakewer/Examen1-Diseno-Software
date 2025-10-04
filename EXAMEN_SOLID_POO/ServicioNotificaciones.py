class ServicioNotificaciones:

    @staticmethod
    def enviar_notificacion_prestamo(usuario, libro_titulo):
        print(f"[NOTIFICACIÓN] {usuario}: Préstamo de '{libro_titulo}'")

    @staticmethod
    def enviar_notificacion_devolucion(usuario, libro_titulo):
        print(f"[NOTIFICACIÓN] {usuario}: Devolución de '{libro_titulo}'")

    @staticmethod
    def enviar_recordatorio(usuario, libro_titulo, dias_retraso):
        print(f"[RECORDATORIO] {usuario}: '{libro_titulo}' tiene {dias_retraso} días de retraso")