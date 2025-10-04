# Implementación de Min-Heap para Priorización de Actividades

## 1. Contexto: ¿Qué es su algoritmo?

### Nombre del Algoritmo
Min-Heap (Montículo Mínimo)

### Explicación Teórica
El Min-Heap es una estructura de datos de árbol binario que mantiene dos propiedades fundamentales:
1. Es un árbol binario completo (todos los niveles están llenos excepto posiblemente el último, que se llena de izquierda a derecha)
2. Para cada nodo, su valor es menor o igual que los valores de sus hijos

Esta estructura garantiza que el elemento más pequeño (en nuestro caso, la actividad más próxima) siempre esté en la raíz del árbol.

Ejemplo visual:
```
       [1 Oct]
      /       \
 [3 Oct]    [5 Oct]
   /  \       /
[8 Oct][7 Oct][6 Oct]
```

### Complejidad

#### Complejidad Temporal
- Inserción: O(log n)
- Extracción del mínimo: O(log n)
- Búsqueda del mínimo: O(1)
- Construcción inicial (heapify): O(n)
- Ordenamiento completo: O(n log n)

#### Complejidad Espacial
- O(n) para almacenar n elementos
- No requiere espacio adicional significativo para las operaciones (in-place)

## 2. ¿Qué hago con este algoritmo y dónde se clasifica?

### Clasificación
- **Tipo**: Estructura de datos y algoritmo de ordenamiento
- **Categoría**: Algoritmo voraz (greedy)
- El Min-Heap pertenece a la familia de algoritmos voraces porque siempre mantiene el elemento más prioritario en la raíz, tomando decisiones localmente óptimas en cada paso.

### Uso General
- Implementación de colas de prioridad
- Ordenamiento de elementos (Heapsort)
- Scheduling y planificación de tareas
- Algoritmos de grafos (como Dijkstra)
- Sistemas de gestión de eventos en tiempo real

## 3. ¿Cómo lo aplico en mi proyecto?

### Contexto del Proyecto
El Proyecto 1 es un planificador personal que gestiona tres tipos de elementos:
- Tareas con fechas límite
- Eventos programados
- Lecciones con sistema de repetición espaciada

El desafío principal es mantener estos elementos ordenados por prioridad temporal y permitir su rápida recuperación.

### Solución mediante Min-Heap

Implementamos una jerarquía de clases basada en `PrioritizedItem`:

```python
class PrioritizedItem(ABC):
    def __init__(self):
        self.title = ""
        self.due_date = None
        self.start_time = None
        self.end_time = None
        self.duration = None

    def __lt__(self, other):
        # Primero comparamos por fecha
        if self.get_priority_date() != other.get_priority_date():
            return self.get_priority_date() < other.get_priority_date()
        
        # Si las fechas son iguales, comparamos por hora
        if self.get_priority_time() and other.get_priority_time():
            return self.get_priority_time() < other.get_priority_time()
        
        # Si todo es igual, priorizamos por tipo
        return self.get_type_priority() < other.get_type_priority()
```

### Justificación de la Elección

1. **Eficiencia Óptima**: 
   - Inserción y extracción en O(log n)
   - Consulta del elemento más prioritario en O(1)
   - Ideal para una aplicación interactiva

2. **Alineación Natural**:
   - La propiedad de Min-Heap coincide perfectamente con nuestra necesidad de priorización temporal
   - La estructura jerárquica se adapta a nuestros diferentes tipos de elementos

3. **Escalabilidad**:
   - Mantiene buen rendimiento incluso con muchos elementos
   - Permite gestionar múltiples tipos de elementos sin degradación

4. **Flexibilidad**:
   - Fácil extensión para nuevos tipos de elementos
   - Soporte natural para diferentes criterios de priorización

## 4. Aplicación Práctica - POC

### Implementación Básica en Python

```python
import heapq
from datetime import datetime, timedelta

class Actividad:
    def __init__(self, titulo, fecha, tipo):
        self.titulo = titulo
        self.fecha = fecha
        self.tipo = tipo
    
    def __lt__(self, other):
        return self.fecha < other.fecha

def demostrar_planificador():
    # Crear heap vacío
    actividades = []
    
    # Insertar actividades (O(log n) cada una)
    fechas = [
        datetime.now() + timedelta(days=i)
        for i in [2, 0, 5, 1, 3]
    ]
    
    for i, fecha in enumerate(fechas):
        actividad = Actividad(f"Actividad {i}", fecha, "Tarea")
        heapq.heappush(actividades, actividad)
    
    # Extraer en orden (O(log n) cada una)
    print("Actividades ordenadas por fecha:")
    while actividades:
        act = heapq.heappop(actividades)
        print(f"{act.titulo}: {act.fecha.strftime('%Y-%m-%d')}")

# Caso de prueba
"""
Entrada:
- 5 actividades con fechas desordenadas

Salida:
Actividades ordenadas por fecha:
Actividad 1: 2025-09-30
Actividad 3: 2025-10-01
Actividad 0: 2025-10-02
Actividad 4: 2025-10-03
Actividad 2: 2025-10-05
"""
```

### Análisis de Complejidad del Caso Particular

En nuestro planificador:
1. **Inserción de nueva actividad**:
   - Complejidad: O(log n)
   - n = número total de actividades
   - Ejemplo: Con 1000 actividades, solo ~10 comparaciones

2. **Obtener próxima actividad**:
   - Complejidad: O(1) para consulta
   - O(log n) para extracción
   - Ejemplo: Mostrar "Tu Día" es instantáneo

3. **Ordenar todas las actividades**:
   - Complejidad: O(n log n)
   - Solo necesario para vistas completas
   - Ejemplo: Ver calendario mensual

4. **Espacio**:
   - O(n) para n actividades
   - Tres heaps separados (tareas, eventos, lecciones)
   - Ejemplo: 1000 actividades ≈ 1000 objetos en memoria

## Operaciones del Min-Heap

### 1. Inserción (O(log n))

Cuando añadimos un nuevo elemento:

```python
def addTask(self, title, due_date):
    task = Task(title, due_date)
    heapq.heappush(self.tasks, task)  # O(log n)
```

El proceso es:
1. Crear el nuevo elemento
2. Añadirlo al final del heap
3. "Flotar" el elemento hacia arriba hasta su posición correcta

Ejemplo visual:
```
Añadir tarea para Oct 2
Antes:        Después:
  [Oct 1]      [Oct 1]
    /           /    \
[Oct 4]     [Oct 2] [Oct 4]
```

### 2. Extracción del Mínimo (O(log n))

Para obtener el elemento más prioritario:

```python
def get_next_task(self):
    if self.tasks:
        return heapq.heappop(self.tasks)  # O(log n)
```

El proceso es:
1. Tomar el elemento raíz (el más prioritario)
2. Mover el último elemento del heap a la raíz
3. "Hundir" el elemento hasta su posición correcta

### 3. Ordenamiento por Períodos (O(n log n))

```python
def _organize_by_period(self, items):
    periods = {
        "Hoy": [],
        "Mañana": [],
        "Esta Semana": [],
        "Próxima Semana": [],
        "Más Adelante": []
    }
    
    for item in items:  # items ya está ordenado por el heap
        period = self._get_period(item.get_priority_date())
        periods[period].append(item)
    
    return periods
```

## Complejidad Algorítmica

1. **Operaciones Básicas**:
   - Inserción (heappush): O(log n)
   - Extracción del mínimo (heappop): O(log n)
   - Consulta del mínimo: O(1)
   - Construcción inicial (heapify): O(n)

2. **Operaciones Compuestas**:
   - Obtener todos los elementos ordenados: O(n log n)
   - Organizar por períodos: O(n)
   - Actualizar prioridad: O(log n)

## Ventajas de Nuestra Implementación

1. **Eficiencia Óptima**:
   - Las operaciones más comunes (inserción y extracción) son logarítmicas
   - La consulta del elemento más prioritario es constante
   - El ordenamiento completo solo se hace cuando es necesario

2. **Diseño Orientado a Objetos**:
   - La clase abstracta `PrioritizedItem` garantiza consistencia
   - Cada tipo de elemento puede tener su propia lógica de priorización
   - Fácil de extender para nuevos tipos de elementos

3. **Manejo Inteligente del Tiempo**:
   - Priorización automática por fechas y horas
   - Agrupación intuitiva por períodos temporales
   - Soporte para horarios flexibles y programados

## Ejemplo de Uso Real

```python
# 1. Crear tareas con diferentes fechas
dm.addTask("Estudiar Matemáticas", "2025-10-01")
dm.addTask("Proyecto Final", "2025-09-30")
dm.addEvent("Reunión de Grupo", "2025-09-29", "14:00")

# 2. El heap mantiene todo ordenado automáticamente
items = dm.get_items_by_day()

# 3. Los elementos aparecen en orden correcto:
# - Primero: Reunión (29 Sept)
# - Segundo: Proyecto (30 Sept)
# - Tercero: Estudiar (1 Oct)
```

## Optimizaciones Implementadas

1. **Heaps Separados**:
   - Cada tipo de elemento tiene su propio heap
   - Evita comparaciones innecesarias entre tipos diferentes
   - Permite operaciones específicas por tipo

2. **Comparación Inteligente**:
   - Primero por fecha (más importante)
   - Luego por hora (si está disponible)
   - Finalmente por tipo (para desempatar)

3. **Actualización Eficiente**:
   - Los cambios de prioridad reorganizan solo lo necesario
   - La vista "Tu Día" se actualiza de manera incremental
   - Se mantiene la consistencia en todas las vistas

## Beneficios para el Usuario

1. **Organización Automática**:
   - No necesita ordenar manualmente sus actividades
   - Siempre ve primero lo más urgente
   - Puede planificar con anticipación

2. **Flexibilidad**:
   - Puede añadir elementos en cualquier orden
   - La priorización se ajusta automáticamente
   - Funciona con o sin horas específicas

3. **Visualización Clara**:
   - Agrupación intuitiva por períodos
   - Fácil identificación de prioridades
   - Vista unificada de todas las actividades