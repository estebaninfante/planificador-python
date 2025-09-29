# Implementación de Min-Heap para Priorización de Actividades

## ¿Qué es un Min-Heap?

Un Min-Heap es una estructura de datos de árbol binario que cumple dos propiedades fundamentales:

1. **Propiedad de Estructura**: Es un árbol binario completo, lo que significa que todos los niveles del árbol están llenos, excepto posiblemente el último nivel, que se llena de izquierda a derecha.

2. **Propiedad de Heap**: Para cualquier nodo padre, su valor es menor o igual que los valores de sus nodos hijos. En nuestro planificador, esto significa que el elemento con la fecha más próxima siempre estará en la raíz del árbol.

### Visualización de un Min-Heap

```
       [1 Oct]
      /       \
 [3 Oct]    [5 Oct]
   /  \       /
[8 Oct][7 Oct][6 Oct]
```

En este ejemplo, cada nodo contiene una fecha y mantiene la propiedad de que la fecha del padre es siempre anterior o igual a las fechas de sus hijos.

## ¿Por qué usamos Min-Heap?

1. **Eficiencia**: Proporciona operaciones muy eficientes para mantener elementos ordenados
2. **Priorización Natural**: La estructura del heap coincide perfectamente con nuestra necesidad de priorizar por fechas
3. **Flexibilidad**: Permite manejar diferentes tipos de elementos (tareas, eventos, lecciones) de manera uniforme

## Diseño del Sistema

### 1. Clase Base Abstracta (PrioritizedItem)

La base de nuestra implementación es la clase abstracta `PrioritizedItem`:

```python
class PrioritizedItem(ABC):
    def __init__(self):
        self.title = ""
        self.due_date = None
        self.start_time = None
        self.end_time = None
        self.duration = None

    @abstractmethod
    def get_priority_date(self) -> date:
        """Retorna la fecha que se usará para priorización"""
        pass

    @abstractmethod
    def get_priority_time(self) -> time:
        """Retorna la hora que se usará para priorización"""
        pass

    @abstractmethod
    def get_type(self) -> str:
        """Retorna el tipo de elemento (Tarea, Evento o Lección)"""
        pass

    def __lt__(self, other):
        """
        Define cómo se comparan dos elementos para el heap.
        Retorna True si este elemento tiene mayor prioridad que 'other'.
        """
        # Primero comparamos por fecha
        if self.get_priority_date() != other.get_priority_date():
            return self.get_priority_date() < other.get_priority_date()
        
        # Si las fechas son iguales, comparamos por hora
        if self.get_priority_time() and other.get_priority_time():
            return self.get_priority_time() < other.get_priority_time()
        
        # Si todo es igual, priorizamos por tipo
        return self.get_type_priority() < other.get_type_priority()
```

### 2. Implementación en las Entidades

Cada tipo de elemento hereda de `PrioritizedItem` e implementa su propia lógica:

#### Tareas (Task)
```python
class Task(PrioritizedItem):
    def get_priority_date(self):
        return self.due_date  # Prioriza por fecha límite

    def get_priority_time(self):
        return self.start_time  # Usa hora de inicio si está programada

    def get_type(self):
        return "Tarea"  # Prioridad más alta
```

#### Eventos (Event)
```python
class Event(PrioritizedItem):
    def get_priority_date(self):
        return self.event_date  # Prioriza por fecha del evento

    def get_priority_time(self):
        return self.event_time  # Usa hora del evento

    def get_type(self):
        return "Evento"  # Prioridad media
```

#### Lecciones (Lesson)
```python
class Lesson(PrioritizedItem):
    def get_priority_date(self):
        return self.next_review_date  # Prioriza por fecha de repaso

    def get_priority_time(self):
        return self.preferred_time  # Usa hora preferida de estudio

    def get_type(self):
        return "Lección"  # Prioridad más baja
```

### 3. Sistema de Priorización en DataManager

El DataManager mantiene tres heaps separados y los combina cuando es necesario:

```python
class DataManager:
    def __init__(self):
        self.tasks = []  # Heap de tareas
        self.events = []  # Heap de eventos
        self.lessons = []  # Heap de lecciones
        heapq.heapify(self.tasks)
        heapq.heapify(self.events)
        heapq.heapify(self.lessons)

    def get_items_by_day(self):
        """
        Combina y ordena todos los elementos de todos los heaps
        y los organiza por períodos temporales.
        """
        all_items = []
        all_items.extend(self._get_heap_items(self.tasks))
        all_items.extend(self._get_heap_items(self.events))
        all_items.extend(self._get_heap_items(self.lessons))
        
        # El heap garantiza que esto sea eficiente
        all_items.sort()  
        return self._organize_by_period(all_items)
```

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