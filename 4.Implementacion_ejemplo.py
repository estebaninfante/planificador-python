
# 4. Aplicación práctica del algoritmo – POC (Proof of Concept)
# Algoritmo: Min-Heap Scheduling (Planificación de tareas)


import heapq  # Librería estándar que maneja Min-Heap en Python

# Creamos una lista vacía para el heap
min_heap = []


# Caso de prueba
# Entrada:
#     Tareas con sus fechas límite (en días):
#     (3, "Matemáticas"), (1, "Inglés"), (2, "Historia")


heapq.heappush(min_heap, (3, "Matemáticas"))
heapq.heappush(min_heap, (1, "Inglés"))
heapq.heappush(min_heap, (2, "Historia"))

print("Tareas en el planificador (ordenadas por urgencia):")

# Proceso:
# - Se insertan las tareas en el Min-Heap
# - El heap mantiene siempre en la raíz la tarea más urgente
# - Se extraen las tareas en orden de prioridad con heappop()

while min_heap:
    deadline, tarea = heapq.heappop(min_heap)
    print(f"Tarea: {tarea}, vence en {deadline} días")


# Salida esperada:
#     Tarea: Inglés, vence en 1 días
#     Tarea: Historia, vence en 2 días
#     Tarea: Matemáticas, vence en 3 días




# Análisis de complejidad en este caso

# - Inserciones (3 tareas): cada heappush tarda O(log n).
#   Con 3 elementos, es muy rápido -> O(log 3).
#
# - Consulta de la tarea más próxima (min_heap[0]): O(1).
#
# - Extracciones (3 tareas): cada heappop tarda O(log n).
#   Con 3 elementos → O(log 3).
#
#  Complejidad total para n tareas:
#    O(n log n) en el peor caso.
#
# Esto es muy eficiente incluso con 1000 tareas, ya que
# O(log 1000) ≈ 10 operaciones por inserción/extracción.

