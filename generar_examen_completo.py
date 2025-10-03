"""
GENERADOR DE ARCHIVOS - EXAMEN SOLID
Ejecuta este script para crear todos los archivos automáticamente

Uso: python generar_examen_completo.py
"""

import os

def crear_carpeta(ruta):
    """Crea una carpeta si no existe"""
    if not os.path.exists(ruta):
        os.makedirs(ruta)
        print(f"✓ Carpeta creada: {ruta}")

def crear_archivo(ruta, contenido):
    """Crea un archivo con contenido"""
    with open(ruta, 'w', encoding='utf-8') as f:
        f.write(contenido)
    print(f"✓ Archivo creado: {ruta}")

print("="*70)
print("GENERADOR DE ARCHIVOS - EXAMEN SOLID 2 HORAS")
print("="*70)
print()

# Crear estructura de carpetas
crear_carpeta("EXAMEN_SOLID_POO")
crear_carpeta("EXAMEN_SOLID_POO/templates")

print("\nGenerando archivos...\n")

# =============================================================================
# ARCHIVO 1: biblioteca_examen.py
# =============================================================================

CODIGO_EXAMEN = '''"""
EXAMEN PRINCIPIOS SOLID - 2 HORAS
Sistema de Mini-Biblioteca

INSTRUCCIONES:
1. NO modifiques este archivo
2. Crea archivos nuevos para tus refactorizaciones
3. Asegúrate que el código siga funcionando

CÓDIGO BASE CON VIOLACIONES DELIBERADAS DE SOLID
"""

class Libro:
    def __init__(self, id, titulo, autor, isbn, disponible=True):
        self.id = id
        self.titulo = titulo
        self.autor = autor
        self.isbn = isbn
        self.disponible = disponible

class Prestamo:
    def __init__(self, id, libro_id, usuario, fecha):
        self.id = libro_id
        self.libro_id = libro_id
        self.usuario = usuario
        self.fecha = fecha
        self.devuelto = False

# VIOLACIÓN: Esta clase hace DEMASIADAS cosas (SRP)
# VIOLACIÓN: Búsqueda con if/elif (OCP)
# VIOLACIÓN: Dependencia directa de implementación (DIP)
class SistemaBiblioteca:
    def __init__(self):
        self.libros = []
        self.prestamos = []
        self.contador_libro = 1
        self.contador_prestamo = 1
        self.archivo = "biblioteca.txt"
    
    # VIOLACIÓN SRP: Mezcla validación + lógica de negocio + persistencia
    def agregar_libro(self, titulo, autor, isbn):
        # Validación inline
        if not titulo or len(titulo) < 2:
            return "Error: Título inválido"
        if not autor or len(autor) < 3:
            return "Error: Autor inválido"
        if not isbn or len(isbn) < 10:
            return "Error: ISBN inválido"
        
        # Lógica de negocio
        libro = Libro(self.contador_libro, titulo, autor, isbn)
        self.libros.append(libro)
        self.contador_libro += 1
        
        # Persistencia
        self._guardar_en_archivo()
        
        return f"Libro '{titulo}' agregado exitosamente"
    
    # VIOLACIÓN OCP: Método cerrado a extensión
    def buscar_libro(self, criterio, valor):
        resultados = []
        
        if criterio == "titulo":
            for libro in self.libros:
                if valor.lower() in libro.titulo.lower():
                    resultados.append(libro)
        
        elif criterio == "autor":
            for libro in self.libros:
                if valor.lower() in libro.autor.lower():
                    resultados.append(libro)
        
        elif criterio == "isbn":
            for libro in self.libros:
                if libro.isbn == valor:
                    resultados.append(libro)
        
        elif criterio == "disponible":
            disponible = valor.lower() == "true"
            for libro in self.libros:
                if libro.disponible == disponible:
                    resultados.append(libro)
        
        return resultados
    
    # VIOLACIÓN SRP: Mezcla validación + lógica + persistencia
    def realizar_prestamo(self, libro_id, usuario):
        # Validación
        if not usuario or len(usuario) < 3:
            return "Error: Nombre de usuario inválido"
        
        # Buscar libro
        libro = None
        for l in self.libros:
            if l.id == libro_id:
                libro = l
                break
        
        if not libro:
            return "Error: Libro no encontrado"
        
        if not libro.disponible:
            return "Error: Libro no disponible"
        
        # Lógica de negocio
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
        
        # Persistencia
        self._guardar_en_archivo()
        
        # Notificación
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
    
    # VIOLACIÓN SRP: Persistencia mezclada
    def _guardar_en_archivo(self):
        with open(self.archivo, 'w') as f:
            f.write(f"Libros: {len(self.libros)}\\n")
            f.write(f"Préstamos: {len(self.prestamos)}\\n")
    
    def _cargar_desde_archivo(self):
        try:
            with open(self.archivo, 'r') as f:
                data = f.read()
            return True
        except:
            return False
    
    # VIOLACIÓN SRP: Notificación es otra responsabilidad
    def _enviar_notificacion(self, usuario, libro):
        print(f"[NOTIFICACIÓN] {usuario}: Préstamo de '{libro}'")


# VIOLACIÓN DIP: Dependencia directa de implementación
def main():
    sistema = SistemaBiblioteca()
    
    print("=== AGREGANDO LIBROS ===")
    print(sistema.agregar_libro("Cien Años de Soledad", "Gabriel García Márquez", "9780060883287"))
    print(sistema.agregar_libro("El Principito", "Antoine de Saint-Exupéry", "9780156012195"))
    print(sistema.agregar_libro("1984", "George Orwell", "9780451524935"))
    
    print("\\n=== BÚSQUEDA POR AUTOR ===")
    resultados = sistema.buscar_libro("autor", "Garcia")
    for libro in resultados:
        print(f"- {libro.titulo} por {libro.autor}")
    
    print("\\n=== REALIZAR PRÉSTAMO ===")
    print(sistema.realizar_prestamo(1, "Juan Pérez"))
    
    print("\\n=== LIBROS DISPONIBLES ===")
    disponibles = sistema.obtener_libros_disponibles()
    for libro in disponibles:
        print(f"- {libro.titulo}")
    
    print("\\n=== DEVOLVER LIBRO ===")
    print(sistema.devolver_libro(1))
    
    print("\\n=== PRÉSTAMOS ACTIVOS ===")
    activos = sistema.obtener_prestamos_activos()
    print(f"Total de préstamos activos: {len(activos)}")


if __name__ == "__main__":
    main()
'''

crear_archivo("EXAMEN_SOLID_POO/biblioteca_examen.py", CODIGO_EXAMEN)

# =============================================================================
# ARCHIVO 2: EXAMEN_2_HORAS.md (INSTRUCCIONES COMPLETAS)
# =============================================================================

INSTRUCCIONES = '''# 📝 EXAMEN: Principios SOLID - Sistema de Biblioteca

## ⏱️ DURACIÓN: 2 HORAS
## ⏱️ REPOSITORIO: Subir a Github

### Distribución de Tiempo Sugerida:
- ⏰ **0:00 - 0:10**: Lectura y setup (10 min)
- ⏰ **0:10 - 0:35**: Ejercicio 1 - OCP (25 min)
- ⏰ **0:35 - 1:15**: Ejercicio 2 - SRP (40 min)
- ⏰ **1:15 - 1:50**: Ejercicio 3 - DIP (35 min)
- ⏰ **1:50 - 2:00**: Revisión y entrega (10 min)

---

## 📋 INSTRUCCIONES GENERALES

### ✅ Qué DEBES hacer:
1. Leer completamente este documento
2. Verificar que el código base funciona
3. Crear archivos nuevos para tus refactorizaciones
4. Mantener la funcionalidad original
5. Comentar tus cambios
6. Entregar todos los archivos Python

### ❌ Qué NO debes hacer:
1. Modificar biblioteca_examen.py original
2. Agregar funcionalidades nuevas
3. Usar librerías externas
4. Copiar código

---

## 📊 EVALUACIÓN (100 puntos)

| Ejercicio | Principio | Puntos | Tiempo |
|-----------|-----------|--------|--------|
| Ejercicio 1 | OCP | 30 | 25 min |
| Ejercicio 2 | SRP | 30 | 40 min |
| Ejercicio 3 | DIP | 30 | 35 min |
| Teórico | LSP + ISP | 10 | 20 min |
| **TOTAL** | | **100** | **120 min** |

---

## 🟢 EJERCICIO 1: Open/Closed Principle (30 pts - 25 min)

### Problema:
El método `buscar_libro()` viola OCP con múltiples.

### Tu Tarea:
1. Crea clase abstracta para generar una estrategia de búsqueda
2. Implementa 3 estrategias de busqueda
3. Refactoriza el método para usar estrategias
4. Agrega BusquedaPorDisponibilidad SIN modificar código existente

### Entregable:
- Clase abstracta + 4 estrategias
- Método refactorizado
- Documentación demostrando uso (como probar que funciona)

---

## 🟡 EJERCICIO 2: Single Responsibility Principle (30 pts - 40 min)

### Problema:
`SistemaBiblioteca` tiene múltiples responsabilidades.

### Tu Tarea:
1. Crea `ValidadorBiblioteca` (solo validación)
2. Crea `RepositorioBiblioteca` (solo persistencia)
3. Crea `ServicioNotificaciones` (solo notificaciones)
4. Refactoriza `SistemaBiblioteca` para usar estas clases

### Entregable:
- 3 clases separadas
- SistemaBiblioteca refactorizada
- main() funcionando
- Documentación demostrando uso (como probar que funciona)

---

## 🔴 EJERCICIO 3: Dependency Inversion Principle (30 pts - 35 min)

### Problema:
Dependencia directa de implementaciones concretas.

### Tu Tarea:
1. Crea interfaz para el repositorio (clase abstracta)
2. Implementa `RepositorioArchivo`
3. Refactoriza `SistemaBiblioteca` con inyección de dependencias
4. Refactoriza main() con configuración de dependencias
5. BONUS: Crea `RepositorioMemoria`

### Entregable:
- Interfaz IRepositorio
- RepositorioArchivo
- Inyección de dependencias
- main() con DI

---

## 📝 PREGUNTAS TEÓRICAS (10 puntos)

### Pregunta 1: LSP (5 pts)

**a) (5 pts)** Explica qué es LSP y cómo se aplica al ejemplo:

```python
class Usuario:
    def calcular_limite_prestamos(self):
        return 3

class Estudiante(Usuario):
    def calcular_limite_prestamos(self):
        return 3
```

**Respuesta:**
```
_________________________________________________________________

_________________________________________________________________
```

**b) (5 pts)** Da un ejemplo que VIOLE LSP y explica por qué:

```python
# Tu código aquí




# Explicación:
_________________________________________________________________
```

---

### Pregunta 2: ISP (5 pts)

**a) (5 pts)** ¿Por qué esta interfaz VIOLA ISP?

```python
class IGestionBiblioteca:
    def agregar_libro(self): pass
    def buscar_libro(self): pass
    def realizar_prestamo(self): pass
    def generar_reporte(self): pass
    def hacer_backup(self): pass
```

**Respuesta:**
```
_________________________________________________________________

_________________________________________________________________
```

**b) (5 pts)** Propón cómo segregar esta interfaz:

```
Interface 1: _____________ - Métodos: _________________________

Interface 2: _____________ - Métodos: _________________________

Interface 3: _____________ - Métodos: _________________________
```

---

## 📦 ENTREGA

### Archivos a entregar:
1. Repositorio en GIT
2. Respuestas del examen teorico en un folder aparte on en el README principal
3. Puedes separar los archivos de cada ejercicio en carpetas si así lo deseas
4.PAra puntos extra, puedes generar los archivos de clase y ponerlos en la carpeta llamada "templates"
4. Considera el checklist de abajo como una Guia de entrega

### Checklist:
- [ ] Todos los archivos ejecutan sin errores
- [ ] Funcionalidad original mantenida
- [ ] Código comentado
- [ ] Preguntas respondidas
- [ ] Nombre en primera página

---

## 💡 CONSEJOS

1. Administra tu tiempo
2. Prueba tu código
3. Comenta tus decisiones
4. Si te atoras, pasa al siguiente

---

**¡MUCHO ÉXITO! 🚀**

'''

crear_archivo("EXAMEN_SOLID_POO/EXAMEN_SOLID_POO.md", INSTRUCCIONES)

# =============================================================================
# ARCHIVO 3: GUIA DE EVALUACIÓN
# =============================================================================

RUBRICA = '''# 📊 Rúbrica de Evaluación - Examen SOLID 2 Horas



## 🟢 EJERCICIO 1: OCP (30 pts)

### Clase Abstracta (10 pts)
- [ ] 10 pts: Perfecta con método abstracto
- [ ] 7 pts: Funcional con detalles menores
- [ ] 4 pts: Incompleta
- [ ] 0-2 pts: Incorrecta

**Puntos:** _____

### Estrategias Concretas (10 pts)
- [ ] 10 pts: 4 estrategias correctas
- [ ] 6 pts: 3 estrategias correctas
- [ ] 2 pts: 2 estrategias
- [ ] 0 pts: <2 estrategias

**Puntos:** _____

### Refactorización (5 pts)
- [ ] 5 pts: Sin if/elif
- [ ] 3 pts: Funcional
- [ ] 2 pts: Intento válido
- [ ] 0 pts: No refactorizó

**Puntos:** _____

### Extensibilidad (5 pts)
- [ ] 5 pts: Nueva estrategia sin modificar
- [ ] 0 pts: No demostró

**Puntos:** _____

**SUBTOTAL EJERCICIO 1:** _____ / 20

---

## 🟡 EJERCICIO 2: SRP (30 pts)

### ValidadorBiblioteca (10 pts)
- [ ] 10 pts: Completa y bien diseñada
- [ ] 7-8 pts: Funcional
- [ ] 4-6 pts: Incompleta
- [ ] 0-3 pts: Ausente/incorrecta

**Puntos:** _____

### RepositorioBiblioteca (10 pts)
- [ ] 10 pts: Completa
- [ ] 7-8 pts: Funcional
- [ ] 4-6 pts: Incompleta
- [ ] 0-3 pts: Ausente

**Puntos:** _____

### ServicioNotificaciones (5 pts)
- [ ] 5 pts: Completa
- [ ] 3-4 pts: Funcional
- [ ] 2 pts: Básica
- [ ] 0 pts: Ausente

**Puntos:** _____

### Refactorización SistemaBiblioteca (5 pts)
- [ ] 5 pts: Usa todas las clases
- [ ] 3-4 pts: Usa 2 clases
- [ ] 2 pts: Usa 1 clase
- [ ] 0 pts: No refactorizó

**Puntos:** _____

**SUBTOTAL EJERCICIO 2:** _____ / 30

---

## 🔴 EJERCICIO 3: DIP (30 pts)

### Interfaz IRepositorio (8 pts)
- [ ] 8 pts: Perfecta
- [ ] 6 pts: Funcional
- [ ] 4 pts: Incompleta
- [ ] 0-2 pts: Incorrecta

**Puntos:** _____

### RepositorioArchivo (8 pts)
- [ ] 8 pts: Completa y funcional
- [ ] 6 pts: Funcional
- [ ] 4 pts: Básica
- [ ] 0-2 pts: No funciona

**Puntos:** _____

### Inyección de Dependencias (8 pts)
- [ ] 8 pts: Perfecta
- [ ] 6 pts: Funcional
- [ ] 4 pts: Intento
- [ ] 0-2 pts: No aplicó DI

**Puntos:** _____

### Demostración (4 pts)
- [ ] 4 pts: Clara
- [ ] 3 pts: Implícita
- [ ] 2 pts: Mencionada
- [ ] 0 pts: No demostró

**Puntos:** _____

### BONUS: Segunda Implementación (2 pts)
- [ ] 2 pts: Sí
- [ ] 0 pts: No

**Puntos:** _____

**SUBTOTAL EJERCICIO 3:** _____ / 30 (+___ bonus)

---

## 📝 PREGUNTAS TEÓRICAS (10 pts)

### LSP - Parte a (5 pts)
- [ ] 5 pts: Explicación completa
- [ ] 3-4 pts: Correcta básica
- [ ] 2 pts: Incompleta
- [ ] 0 pts: Incorrecta

**Puntos:** _____

### ISP - Parte b (5 pts)
- [ ] 5 pts: Excelente diseño
- [ ] 3-4 pts: Diseño válido
- [ ] 2 pts: Intento
- [ ] 0 pts: Incorrecto

**Puntos:** _____

**SUBTOTAL TEÓRICO:** _____ / 10

---

## 📊 RESUMEN FINAL

| Sección | Puntos | Máximo |
|---------|--------|--------|
| Ejercicio 1 (OCP) | _____ | 30 |
| Ejercicio 2 (SRP) | _____ | 30 |
| Ejercicio 3 (DIP) | _____ | 30 |
| Teórico (LSP+ISP) | _____ | 10 |
| **TOTAL** | _____ | **100** |
| Bonus | _____ | +2 |

**CALIFICACIÓN FINAL:** _____ / 100

'''

crear_archivo("EXAMEN_SOLID_POO/RUBRICA_EXAMEN_SOLID_POO.md", RUBRICA)

print("\n" + "="*70)
print("✅ ARCHIVOS GENERADOS EXITOSAMENTE")
print("="*70)
print("\nArchivos creados en la carpeta: EXAMEN_SOLID_POO/")
print("\nArchivos generados:")
print("  1. biblioteca_examen.py (código base)")
print("  2. EXAMEN_2_HORAS.md (instrucciones)")
print("  3. RUBRICA_EXAMEN_2_HORAS.md (evaluación)")
print("\n¡Listo para usar!")
print("="*70)