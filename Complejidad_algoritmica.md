# datamanager.py

import json
import os
from Task import Task
from Event import Event
from Lesson import Lesson
from Status import Status
from datetime import date, timedelta

path_file = "base_local.json"

class DataManager:
   
    def __init__(self, file_path=path_file):    
        self.file_path = file_path       # -> c1 (Asignacion)  /  O(1)
        self.data = self.loadData()      # -> c1 (Asignacion) + T(loadData) / O(loadData(n))  

        # T(init) = 2*c1 + T(loadData)
        # Tinit​(n)=O(1)+O(loadData(n)) ->    Tinit(n)= O(n+m)


    def loadData(self):

        # Acceso a variable self.file_path -> c1
        # Llamada a función os.path.exists() -> constante (cf)
        # Comparación del "if con " "not" -> 2*c2

        if not os.path.exists(self.file_path):  
           
           # Creación de un diccionario con 3 claves vacías → 3c1 (asignaciones constantes)
            
            return {"tasks": [], "events": [], "lessons": []}
            
            #  c1 + cf + 2*c2 + 3*c1  = 4*c1 + cf + 2*c2
            #  O(1 + cf)  =   O(c1)
        
        
        try:
        
        with open(self.file_path, "r", encoding="utf-8") as f:
            # Acceso a self.file_path -> c1
            # Llamada al sistema open() -> cf_open
            # Asignación del descriptor a f -> c1
            # (Cuando termina el with, también se ejecuta cierre automático) -> cf_close

        
            raw_data = json.load(f)
            
            # Asignación a raw_data → c1
            # Llamada a json.load(f) (depende del tamaño del archivo(m)) → cf_json(m) 

        
            return {
                
                "tasks": [Task.from_dict(task) for task in raw_data.get('tasks', [])],

                # Acceso a diccionario raw_data.get('tasks', []) -> c1
                # Supongamos que hay 'k' tareas:
                #   - Por cada tarea:
                #       Acceso a elemento de la lista -> c1
                #       Asignación de variable de iteración -> c1
                #       Llamada a Task.from_dict(task) -> cf_task
                #       Inserción en la lista resultado -> c1
                #       Comparación de fin de bucle -> c2
                #   Costo por tarea ≈ (3c1 + c2 + cf_task)
                #   Total tasks = c1 + k*(3c1 + c2 + cf_task) + c2 (chequeo final)

                
                "events": [Event.from_dict(e) for e in raw_data.get('events', [])],
                
                # Acceso a diccionario -> c1
                # Si hay 'i' eventos:
                #   Total events = c1 + i*(3c1 + c2 + cf_event) + c2

                
                "lessons": [Lesson.from_dict(l) for l in raw_data.get('lessons', [])]
                
                # Acceso a diccionario -> c1
                # Si hay 'o' lecciones:
                #   Total lessons = c1 + o*(3c1 + c2 + cf_lesson) + c2
            }
            # Construcción del diccionario final con 3 claves → 3c1
            # Return del diccionario → c1

        except (json.JSONDecodeError, IOError) as e:

            # Asignación del error a 'e' → c1

            print(f"Error al cargar el archivo JSON: {e}. Se creará uno nuevo.")
            # Llamada a print (formateo + salida) → cf_print

            return {"tasks": [], "events": [], "lessons": []}
            # Construcción de diccionario con 3 claves vacías -> 3c1
            # Return -> c1


    # Notación final =  𝑇(loadData) = 10*𝑐1 + 3*𝑐2 + 𝑐𝑓_open + 𝑐𝑓_close + 𝑐𝑓_json(𝑚) + ∑(𝑡=1, 𝑘) (3*𝑐1 + 𝑐2 + 𝑐𝑓_task ) + ∑ (𝑒=1, 𝑖) (3*𝑐1 + 𝑐2 + 𝑐𝑓_event) + ∑ (𝑙=1, 𝑜) (3*𝑐1 + 𝑐2 + 𝑐𝑓_lesson ) 
   
    # n = (número de tareas, eventos y lecciones (k + i + o))
    # m = (tamaño del archivo en bytes (para json.load))
    
    # T(loadData)=O(n+m)





def saveData(self):
    try:
        # Abrir archivo para escritura
        # Acceso a self.file_path -> c1
        # open() -> cf_open
        # Asignación del descriptor a f -> c1
        # Cierre automático del with -> cf_close
        with open(self.file_path, "w", encoding="utf-8") as f:

            # Construcción del diccionario serializable
            # Asignación del diccionario -> c1
            serializable_data = {
                
        
                # Acceso a self.data["tasks"] -> c1
                # Si hay k tareas:
                #   Por cada tarea:
                #       Acceso elemento -> c1
                #       Asignación iteración -> c1
                #       Llamada t.to_dict() -> cf_task
                #       Inserción en lista -> c1
                #       Comparación fin de bucle -> c2
                # Total tasks = c1 + sum_{t=1}^{k} (3c1 + c2 + cf_task) + c2
                
                
                "tasks": [t.to_dict() for t in self.data["tasks"]],

                
                # Acceso a self.data["events"] -> c1
                # Si hay i eventos:
                #   Total events = c1 + sum_{e=1}^{i} (3c1 + c2 + cf_event) + c2
                
                "events": [e.to_dict() for e in self.data["events"]],

                
                # Acceso a self.data["lessons"] -> c1
                # Si hay o lecciones:
                #   Total lessons = c1 + sum_{l=1}^{o} (3c1 + c2 + cf_lesson) + c2
                
                "lessons": [l.to_dict() for l in self.data["lessons"]]
            }
            # Construcción final del diccionario -> 4c1

            # Guardar JSON en archivo
            # Llamada a json.dump -> cf_json_dump(n)
            # Escritura en archivo -> cf_write(n)
            
            json.dump(serializable_data, f, indent=4)

    except IOError as e:
        # Asignación del error -> c1
        # Llamada a print -> cf_print

        print(f"Error al guardar los datos: {e}")


    # T(saveData) ​= 10*c1​ +3*c2 ​ +cf_open ​+cf_close +  ∑ (t=1, k) ​(3c 1 ​ +c 2 ​ +cf_task) + ∑ (e=1, i)(3c 1 ​ +c 2 ​ +cf_event ) + ∑(l=1, o) ​(3c 1 ​ +c 2 ​ +cf_lesson ) +cf_json_dump (n) + cf_write ​(n) ​

    # n = k + i + o (total de elementos)
    # T(saveData) = O(n)


    
    def addTask(self, title, due_date):
        
        # Llamada al constructor Task(title, due_date) -> cf_task_construct
        # Asignación a new_task -> c1
        new_task = Task(title, due_date)

        # Agregar la tarea a la lista
        # Acceso a self.data["tasks"] -> c1
        # Append en lista -> c1

        self.data["tasks"].append(new_task)

        
        # T(saveData)
        self.saveData()

    # T(addTask)= 3*c1 ​+ cf_task_construct​ ​+ T(saveData)
    # T(addTask)= O(n)


    def deleteTask(self, index):

        # Comparar índice con rango de la lista
        # 0 <= index < len(self.data['tasks']) -> c2 + c1 + c1
        if 0 <= index < len(self.data['tasks']):
            
            # Eliminar elemento de la lista
            # Del self.data['tasks'][index] -> c1 + cf_delete
            del self.data['tasks'][index]

            
            # T(saveData)
            self.saveData()

            
            # Asignación / retorno -> c1
            return True

        
        # Asignación / retorno -> c1
        return False

    # T(deleteTask)= c2 + 2*c1 + (c1 +cf_delete​) + T(saveData) + c1
    # T(deleteTask)= O(n)

    def get_all_tasks(self):
       
        # Acceso a la lista de tareas dentro del diccionario self.data -> c1        
        tasks_list = self.data['tasks']

        # Retorno de la lista -> c1
        return tasks_list

    
    # T(get_all_tasks) = c1 (acceso) + c1 (retorno) = 2c1
    # O(1) -> (no depende del número de tareas)


    
    def addEvent(self, title, description, due_date, time):
        
        
        # Llamada al constructor Event(title, description, due_date, time) -> cf_event_construct
        # Asignación a new_event -> c1

        new_event = Event(title, description, due_date, time)

        # Agregar el evento a la lista
        # Acceso a self.data["events"] -> c1
        # Append en lista -> c1

        self.data['events'].append(new_event)

        # Guardar todos los datos en el archivo
        # Representamos todo el costo de guardar como T(saveData)

        self.saveData()

     
    T(addEvent) = 3c1 + cf_event_construct + T(saveData)
    Complejidad: O(n) por el saveData



    def deleteEvent(self, index):

        # Comparar índice con rango de la lista -> c2 + 2*c1
        if 0 <= index < len(self.data['events']):
            
            # Eliminar elemento de la lista -> c1 + cf_delete
            del self.data['events'][index]

            #T(saveData)
            self.saveData()

            # Retornar True
            # Asignación / retorno -> c1
            return True

        # Retornar False si el índice no es válido
        # Asignación / retorno -> c1
        return False

    
    # T(deleteEvent) = 4c1 + c2 + cf_delete + T(saveData)
    # O(n) por saveData



    def get_all_events(self):
        
       
        # Operación de acceso -> c1
        events_list = self.data['events']

        # Retorno de la lista -> c1
        return events_list

    # T(get_all_events) = 2*c1
    # Complejidad: O(1) 



    
    def addLesson(self, title, notes, due_date, subject):

        # Llamada al constructor Lesson(title, notes, due_date, subject)
        # Asignación a new_lesson -> c1
        # Tiempo del constructor -> cf_lesson_construct
        new_lesson = Lesson(title, notes, due_date, subject)

        
        # Acceso a self.data['lessons'] -> c1
        # Append en lista -> c1
        self.data['lessons'].append(new_lesson)

        # Guardar todos los datos en el archivo
        # Representamos todo el costo de guardar como T(saveData)
        self.saveData()

    # T(addLesson) = 3*c1 + cf_lesson_construct + T(saveData)
    # Complejidad: O(n) 

    
    def deleteLesson(self, index):

        # Comparar índice con rango de la lista -> c2 + 2*c1

        if 0 <= index < len(self.data['lessons']):
            
            # Eliminar elemento de la lista -> c1 + cf_delete
            del self.data['lessons'][index]

            # T(saveData)
            self.saveData()

            # Retorno -> c1
            return True

        # Retorno si el índice no es válido -> c1
        return False

    # T(deleteLesson) = 4*c1 + c2 + cf_delete + T(saveData)
    # Complejidad: O(n) 

    
    def reviewLesson(self, score, index):
        
        # Comparar índice con rango de la lista -> c2 + 2*c1

        if 0 <= index < len(self.data['lessons']):
            

            # self.data['lessons'][index] -> c1
            # review_lesson(score) -> cf_review (dependiendo de la implementación de review_lesson)
            self.data['lessons'][index].review_lesson(score)

            # T(saveData)
            self.saveData()

            # Retorno -> c1
            return True
        else:
            
            # Llamada a print -> cf_print
            print("Hubo un error, no se pudo actualizar.")

    # T(reviewLesson) = 3*c1 + c2 + cf_review + T(saveData) + cf_print (en caso de error)
    # Complejidad: O(n) 



    def get_all_lessons(self):

        # Operación de acceso -> c1
        lessons_list = self.data['lessons']

        # Retorno de la lista -> c1
        return lessons_list

    # T(get_all_lessons) = 2*c1
    # Complejidad: O(1) 


