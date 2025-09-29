# datamanager.py

import json
import os
import heapq
from typing import List, Dict, Any, Union
from Task import Task
from Event import Event
from Lesson import Lesson
from Status import Status
from datetime import date, datetime, time, timedelta
from PrioritizedItem import PrioritizedItem

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

    def get_all_prioritized_items(self, days_range: int = None) -> List[PrioritizedItem]:
        """
        Retorna una lista combinada de tareas, eventos y lecciones, ordenada por prioridad.
        
        Args:
            days_range: Si se especifica, solo retorna items dentro de los próximos N días
        """
        min_heap = []
        today = date.today()
        
        # Añadir todos los items al heap
        for item in self.data['tasks'] + self.data['events'] + self.data['lessons']:
            if days_range is not None:
                days_until = (item.get_priority_date() - today).days
                if days_until < 0 or days_until > days_range:
                    continue
            heapq.heappush(min_heap, item)
        
        # Extraer items del heap en orden de prioridad
        prioritized_items = []
        while min_heap:
            prioritized_items.append(heapq.heappop(min_heap))
        return prioritized_items

    def suggest_time_slots(self, items: List[PrioritizedItem]) -> None:
        """Sugiere horarios para una lista de items basados en su prioridad."""
        # Horario laboral típico
        WORK_START = time(8, 0)  # 8:00 AM
        WORK_END = time(22, 0)   # 10:00 PM
        
        current_time = datetime.now().time()
        current_slot = current_time
        
        if current_time < WORK_START:
            current_slot = WORK_START
        elif current_time > WORK_END:
            current_slot = WORK_START  # Comenzar mañana
            
        for item in items:
            if not item.start_time:  # Solo si no tiene horario asignado
                start_time = current_slot
                
                # Calcular hora de finalización basada en la duración
                start_dt = datetime.combine(date.today(), start_time)
                end_dt = start_dt + timedelta(minutes=item.duration)
                
                # Si el final excede el horario laboral, mover al siguiente día
                if end_dt.time() > WORK_END:
                    start_time = WORK_START
                    end_dt = datetime.combine(date.today(), WORK_START) + timedelta(minutes=item.duration)
                
                item.set_time_range(start_time, end_dt.time())
                
                # Actualizar el siguiente slot disponible
                current_slot = end_dt.time()

    def get_items_by_day(self) -> Dict[str, List[PrioritizedItem]]:
        """
        Organiza los items por día (hoy, mañana, próximos días, etc.)
        """
        items_by_day = {
            "Para Hoy (Urgente)": [],  # Vencidos y de hoy
            "Mañana": [],
            "Próximos 7 días": [],
            "Más adelante": []
        }
        
        today = date.today()
        tomorrow = today + timedelta(days=1)
        week_later = today + timedelta(days=7)
        
        # Obtener todos los items
        all_items = self.get_all_prioritized_items()
        urgent_items = []
        
        for item in all_items:
            priority_date = item.get_priority_date()
            
            if priority_date < today or priority_date == today:
                urgent_items.append(item)
            elif priority_date == tomorrow:
                items_by_day["Mañana"].append(item)
            elif priority_date <= week_later:
                items_by_day["Próximos 7 días"].append(item)
            else:
                items_by_day["Más adelante"].append(item)
        
        # Sugerir horarios para items urgentes
        self.suggest_time_slots(urgent_items)
        items_by_day["Para Hoy (Urgente)"] = sorted(
            urgent_items,
            key=lambda x: (x.start_time if x.start_time else time(23, 59))
        )
                
        return items_by_day

    def get_prioritized_tasks(self):
        """Retorna una lista de tareas ordenadas por prioridad usando Min-Heap."""
        min_heap = []
        for task in self.data['tasks']:
            heapq.heappush(min_heap, task)
        return [heapq.heappop(min_heap) for _ in range(len(min_heap))]

    def get_prioritized_events(self):
        """Retorna una lista de eventos ordenados por prioridad usando Min-Heap."""
        min_heap = []
        for event in self.data['events']:
            heapq.heappush(min_heap, event)
        return [heapq.heappop(min_heap) for _ in range(len(min_heap))]

    def get_prioritized_lessons(self):
        """Retorna una lista de lecciones ordenadas por prioridad usando Min-Heap."""
        min_heap = []
        for lesson in self.data['lessons']:
            heapq.heappush(min_heap, lesson)
        return [heapq.heappop(min_heap) for _ in range(len(min_heap))]

    def get_all_tasks(self):
        """Retorna la lista de todas las tareas ordenadas por prioridad."""
        return self.get_prioritized_tasks()

    def get_all_events(self):
        """Retorna la lista de todos los eventos ordenados por prioridad."""
        return self.get_prioritized_events()

    def get_all_lessons(self):
        """Retorna la lista de todas las lecciones ordenadas por prioridad."""
        return self.get_prioritized_lessons()

    def import_from_json(self, json_data):
        """
        Importa elementos desde datos JSON.
        
        El JSON debe tener el siguiente formato:
        {
            "tasks": [
                {
                    "title": "Tarea 1",
                    "due_date": "2025-10-01",
                    "status": "Pendiente"
                },
                ...
            ],
            "events": [
                {
                    "title": "Evento 1",
                    "description": "Descripción",
                    "due_date": "2025-10-01",
                    "time": "10:00"
                },
                ...
            ],
            "lessons": [
                {
                    "title": "Lección 1",
                    "notes": "Notas",
                    "due_date": "2025-10-01",
                    "subject": "Matemáticas"
                },
                ...
            ]
        }
        """
        try:
            # Importar tareas
            if 'tasks' in json_data:
                for task_data in json_data['tasks']:
                    try:
                        task = Task.from_dict(task_data)
                        self.data['tasks'].append(task)
                    except ValueError as e:
                        print(f"Error importando tarea: {e}")

            # Importar eventos
            if 'events' in json_data:
                for event_data in json_data['events']:
                    try:
                        event = Event.from_dict(event_data)
                        self.data['events'].append(event)
                    except ValueError as e:
                        print(f"Error importando evento: {e}")

            # Importar lecciones
            if 'lessons' in json_data:
                for lesson_data in json_data['lessons']:
                    try:
                        lesson = Lesson.from_dict(lesson_data)
                        self.data['lessons'].append(lesson)
                    except ValueError as e:
                        print(f"Error importando lección: {e}")

            # Guardar los cambios
            self.saveData()
            return True, "Importación completada con éxito"
            
        except Exception as e:
            return False, f"Error durante la importación: {str(e)}"

    def import_from_file(self, file_path):
        """
        Importa elementos desde un archivo JSON.
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                json_data = json.load(f)
                return self.import_from_json(json_data)
        except json.JSONDecodeError:
            return False, "El archivo no contiene JSON válido"
        except Exception as e:
            return False, f"Error al leer el archivo: {str(e)}"

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

