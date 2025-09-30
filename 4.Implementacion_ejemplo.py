## Ejemplo de implementación de Min-Heap en Python para un planificador de tareas

import heapq  # Librería estándar que maneja Min-Heap en Python

# Creamos una lista vacía para el heap
min_heap = []

# Insertamos tareas (nombre, fecha límite en días)
heapq.heappush(min_heap, (3, "Matemáticas"))  
heapq.heappush(min_heap, (1, "Inglés"))  
heapq.heappush(min_heap, (2, "Historia"))  

print("Tareas en el planificador :")

# Sacamos las tareas en orden de prioridad (menor deadline primero)
while min_heap:
    deadline, tarea = heapq.heappop(min_heap)
    print(f"Tarea: {tarea}, vence en {deadline} día(s)")

## Análisis de complejidad en este casoAnálisis de complejidad en este caso EJEMPLO:

# Inserciones (3 tareas): cada heappush tarda O(log n). Con 3 elementos, es muy rápido
# Consulta de la tarea más próxima: si se usara min_heap[0], sería O(1).
# Extracciones (3 tareas): cada heappop también tarda O(log n). Nuevamente, con 3 elementos, es muy rápido
# En total, para 3 tareas, el tiempo es insignificante. Pero si tuviéramos 1000 tareas, cada inserción y extracción seguiría siendo O(log 1000) = O(10), lo cual es eficiente.