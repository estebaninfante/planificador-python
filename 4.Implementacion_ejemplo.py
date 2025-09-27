import heapq  # Librería estándar que maneja Min-Heap en Python

# Creamos una lista vacía para el heap
min_heap = []

# Insertamos tareas (nombre, fecha límite en días)
heapq.heappush(min_heap, (3, "Matemáticas"))  
heapq.heappush(min_heap, (1, "Inglés"))  
heapq.heappush(min_heap, (2, "Historia"))  

print("Tareas en el planificador (ordenadas por deadline):")

# Sacamos las tareas en orden de prioridad (menor deadline primero)
while min_heap:
    deadline, tarea = heapq.heappop(min_heap)
    print(f"Tarea: {tarea}, vence en {deadline} día(s)")
