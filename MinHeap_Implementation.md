# Implementación de Min-Heap para Priorización de Actividades

## Descripción del Algoritmo

El Min-Heap es una estructura de datos de árbol binario que mantiene la propiedad de que cada nodo padre tiene un valor menor o igual que sus hijos. En nuestro caso, lo utilizamos para mantener una cola de prioridad donde los elementos con fechas más próximas tienen mayor prioridad.

## Diseño del Sistema

### 1. Clase Base Abstracta (PrioritizedItem)

```python
class PrioritizedItem(ABC):
    @abstractmethod
    def get_priority_date(self) -> date
    @abstractmethod
    def get_priority_time(self) -> str
    @abstractmethod
    def get_type(self) -> str
```

Esta clase define la interfaz común para todos los elementos priorizables (tareas, eventos y lecciones).

### 2. Implementación en las Entidades

Cada tipo de elemento (Task, Event, Lesson) hereda de PrioritizedItem e implementa su propia lógica de priorización:

- **Tareas**: Priorizadas por fecha límite
- **Eventos**: Priorizados por fecha y hora del evento
- **Lecciones**: Priorizadas por fecha de próxima revisión

### 3. Sistema de Priorización Unificado

El DataManager implementa métodos para manejar la priorización:

```python
def get_all_prioritized_items(self, days_range: int = None)
def get_items_by_day(self)
```

## Complejidad Algorítmica

- **Inserción**: O(log n)
- **Extracción del mínimo**: O(log n)
- **Construcción inicial del heap**: O(n)
- **Obtener todos los elementos ordenados**: O(n log n)

## Ventajas de la Implementación

1. **Unificación**: Un solo sistema maneja la priorización de todos los tipos de elementos
2. **Flexibilidad**: Fácil de extender para nuevos tipos de elementos
3. **Eficiencia**: Mantiene los elementos ordenados con un costo logarítmico
4. **Organización Temporal**: Agrupa elementos por períodos (hoy, mañana, próxima semana)

## Casos de Uso

1. **Vista "Tu Día"**: Muestra actividades organizadas por proximidad temporal
2. **Priorización Individual**: Cada tipo de elemento mantiene su propia cola de prioridad
3. **Planificación Futura**: Permite ver actividades agrupadas por períodos de tiempo

## Ejemplo de Funcionamiento

```python
# Crear el heap
min_heap = []
heapq.heappush(min_heap, task1)  # Tarea para mañana
heapq.heappush(min_heap, event1) # Evento para hoy
heapq.heappush(min_heap, lesson1) # Lección para la próxima semana

# Extraer elementos en orden de prioridad
while min_heap:
    next_item = heapq.heappop(min_heap)
    # El item más próximo saldrá primero
```

## Mejoras y Extensiones Futuras

1. **Priorización Ponderada**: Añadir pesos adicionales basados en:
   - Importancia del evento
   - Dificultad de la tarea
   - Progreso en las lecciones

2. **Adaptabilidad**: Ajustar prioridades basándose en:
   - Patrones de comportamiento del usuario
   - Tiempo estimado de completitud
   - Dependencias entre actividades