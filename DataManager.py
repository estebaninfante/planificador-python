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
    """
    Gestor de datos para cargar, guardar y manipular la información.
    Se encarga de la persistencia de los datos en un archivo JSON.
    """
    def __init__(self, file_path=path_file):
        self.file_path = file_path
        self.data = self.loadData()

    def loadData(self):
        """Carga los datos del archivo JSON y los convierte en objetos."""
        if not os.path.exists(self.file_path):
            return {"tasks": [], "events": [], "lessons": []}
        
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                raw_data = json.load(f)
                return {
                    "tasks": [Task.from_dict(task) for task in raw_data.get('tasks', [])],
                    "events": [Event.from_dict(events) for events in raw_data.get('events', [])],
                    "lessons": [Lesson.from_dict(lessons) for lessons in raw_data.get('lessons', [])]
                }
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error al cargar el archivo JSON: {e}. Se creará uno nuevo.")
            return {"tasks": [], "events": [], "lessons": []}

    def saveData(self):
        """Guarda los datos de los objetos en un archivo JSON."""
        try:
            with open(self.file_path, "w", encoding="utf-8") as f:
                serializable_data = {
                    "tasks": [t.to_dict() for t in self.data["tasks"]],
                    "events": [e.to_dict() for e in self.data["events"]],
                    "lessons": [l.to_dict() for l in self.data["lessons"]]
                }
                json.dump(serializable_data, f, indent=4)
        except IOError as e:
            print(f"Error al guardar los datos: {e}")

    # --- Métodos para Tareas ---
    def addTask(self, title, due_date):
        """Agrega una nueva tarea a la lista."""
        new_task = Task(title, due_date)
        self.data["tasks"].append(new_task)
        self.saveData()

    def deleteTask(self, index):
        """Elimina una tarea por su índice."""
        if 0 <= index < len(self.data['tasks']):
            del self.data['tasks'][index]
            self.saveData()
            return True
        return False

    def get_all_tasks(self):
        """Retorna la lista de todas las tareas."""
        return self.data['tasks']

    # --- Métodos para Eventos ---
    def addEvent(self, title, description, due_date, time):
        """Agrega un nuevo evento a la lista."""
        new_event = Event(title, description, due_date, time)
        self.data['events'].append(new_event)
        self.saveData()

    def deleteEvent(self, index):
        if 0 <= index < len(self.data['events']):
            del self.data['events'][index]
            self.saveData()
            return True
        return False

    def get_all_events(self):
        return self.data['events']

    # --- Métodos para Lecciones ---
    def addLesson(self, title, notes, due_date, subject):
        new_lesson = Lesson(title, notes, due_date, subject)
        self.data['lessons'].append(new_lesson)
        self.saveData()
    
    def deleteLesson(self, index):
        if 0 <= index < len(self.data['lessons']):
            del self.data['lessons'][index]
            self.saveData()
            return True
        return False
    
    def reviewLesson(self, score, index):
        if 0 <= index < len(self.data['lessons']):
            self.data['lessons'][index].review_lesson(score)
            self.saveData()
            return True
        else:
            print("Hubo un error, no se pudo actualizar.")



    def get_all_lessons(self):
        return self.data['lessons']

