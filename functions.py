import json
import os



path_file = "base_local.json"

class Task:
    def __init__(self, title, status, due_date):
        self.title = title
        self.status = status
        self.due_date = due_date

    def to_dict(self):
        return {'title': self.title, 'status': self.status, 'due_date': self.due_date}
    
class Event:
    def __init__(self, title, description, due_date, time):
        self.title = title
        self.description = description
        self.due_date = due_date
        self.time = time

    def to_dict(self):
        return {'title': self.title, 'description': self.due_date, 'due_date': self.due_date, 'time': self.time}

class Lesson:
    def __init__(self, title, notes, due_date, subject):
        self.title = title
        self.notes = notes
        self.subject = subject
        self.due_date = due_date

    def to_dict(self):
        return {'title': self.title, 'notes': self.notes, 'due_date': self.due_date, 'subject': self.subject}
    
    @staticmethod
    def from_dict(data):
        """
        Crea una instancia de Lesson a partir de un diccionario 'data'.
        Espera que 'data' tenga las claves: 'title', 'notes', 'date', 'subject'.
        """
        # Validación mínima para dar errores claros si faltan claves:
        missing = [k for k in ('title', 'notes', 'due_date', 'subject') if k not in data]
        if missing:
            raise KeyError(f"Faltan claves requeridas en data: {missing}")
        
        # Construcción del objeto usando los valores del diccionario
        return Lesson(
            title=data['title'],
            notes=data['notes'],
            due_date=data['due_date'],
            subject=data['subject']
        )


 

class DataManager:
    def __init__(self, data):
        self.data = data

    def loadData(self):
        if os.path.exists(path_file):
           return {'task': [], 'events': [], 'lessons': []} 
        try:
            with open(path_file, "r") as f:
                raw_data = json.load(f)

                return {
                    "tasks" : [Task.from_dict(data) for data in path_file.get('tasks', [])],
                    "events": [Event.from_dict(data) for data in path_file.get('events', [])],
                    "lessons": [Lesson.from_dict(data) for data in path_file.get('lessons', [])]
                }

        except (json.JSONDecodeError, IOError):
            return {
                "tasks": [], "events": [], "lessons": []
            }            
    def saveData(self):
        with open(path_file, "w") as pepito:
            json.dump(self.data, pepito, indent=4)



    def addTask(self, title, status, due_date):
        new_task = Task(title, status, due_date)
        self.data["tasks"].append(new_task.to_dict())  # Agregar como dict para guardar en JSON
        self.saveData()  # Guardar cambios

    def showTasks(self):
        if not self.data['tasks']:
            print("¡Felicidades, no tienes tareas pendientes!.")
        else:
            for t in self.data['tasks']:
                print(t)

    def deleteTask(self, index):
        if 0 <= index < len(self.data['tasks']):
            del self.data['tasks'][index]
            self.saveData()
            print("Tarea eliminada exitosamente.")
        else:
            print("Índice de tarea no válido.")

    # --- Funciones de Eventos ---
    def addEvent(self, title, description, due_date, time):
        new_event = Event(title, description, due_date, time)
        self.data["events"].append(new_event)
        self.saveData()

    def showEvents(self):
        if not self.data['events']:
            print("No hay eventos registrados.")
        else:
            print("\n--- Eventos Registrados ---")
            for i, event in enumerate(self.data['events']):
                print(f"{i+1}. {event}")

    def deleteEvent(self, index):
        if 0 <= index < len(self.data['events']):
            del self.data['events'][index]
            self.saveData()
            print("Evento eliminado exitosamente.")
        else:
            print("Índice de evento no válido.")

    # --- Funciones de Clases ---
    def addLesson(self, title, notes, due_date, subject):
        new_lesson = Lesson(title, notes, due_date, subject)
        self.data["lessons"].append(new_lesson)
        self.saveData()

    def showLessons(self):
        if not self.data['lessons']:
            print("No hay clases registradas.")
        else:
            print("\n--- Clases Registradas ---")
            for i, lesson in enumerate(self.data['lessons']):
                print(f"{i+1}. {lesson}")

    def deleteLesson(self, index):
        if 0 <= index < len(self.data['lessons']):
            del self.data['lessons'][index]
            self.saveData()
            print("Clase eliminada exitosamente.")
        else:
            print("Índice de clase no válido.")

    

