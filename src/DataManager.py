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
from UserPreferences import UserPreferences
from Status import Status

path_file = "base_local.json"
preferences_file = "user_preferences.json"

class DataManager:
    """
    Gestor de datos para cargar, guardar y manipular la información.
    Se encarga de la persistencia de los datos en un archivo JSON.
    """
    def __init__(self, file_path=path_file):
        self.file_path = file_path
        self.preferences_path = preferences_file
        self.data = self.loadData()
        self.user_preferences = self.loadPreferences()

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

    def loadPreferences(self):
        """Carga las preferencias del usuario desde un archivo JSON."""
        if not os.path.exists(self.preferences_path):
            return UserPreferences()
            
        try:
            with open(self.preferences_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                return UserPreferences.from_dict(data)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error al cargar preferencias: {e}. Se usarán las predeterminadas.")
            return UserPreferences()

    def savePreferences(self):
        """Guarda las preferencias del usuario en un archivo JSON."""
        try:
            with open(self.preferences_path, "w", encoding="utf-8") as f:
                json.dump(self.user_preferences.to_dict(), f, indent=4)
        except IOError as e:
            print(f"Error al guardar preferencias: {e}")

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
    def addTask(self, title, due_date, estimated_minutes: int | None = None):
        """Agrega una nueva tarea a la lista."""
        # Acepta tanto date como str ISO (YYYY-MM-DD)
        if isinstance(due_date, str):
            try:
                due_date = date.fromisoformat(due_date)
            except ValueError:
                # Si el formato no es ISO, intentar parseo laxo (dd/mm/yyyy)
                try:
                    parts = due_date.replace("/", "-").split("-")
                    if len(parts[0]) == 2:  # dd-mm-YYYY
                        d, m, y = map(int, parts)
                        due_date = date(y, m, d)
                    else:
                        due_date = date.fromisoformat(due_date)
                except Exception:
                    due_date = date.today()
        new_task = Task(title, due_date, estimated_minutes=estimated_minutes)
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
        
        # Añadir todos los items al heap, ignorando completados
        for item in self.data['tasks'] + self.data['events'] + self.data['lessons']:
            if hasattr(item, 'status') and item.status == Status.COMPLETADO:
                continue
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
        """Asigna horarios sin sobrescribir eventos fijos ni solapar con ellos.

        - Los Eventos se consideran fijos y conservan su `time` (1h por defecto si no hay duración).
        - Tareas y Lecciones se colocan en los huecos libres de la jornada (08:00–22:00),
          empezando desde la hora actual.
        - Si no hay espacio, continúa al día siguiente.
        """
        WORK_START = time(8, 0)
        WORK_END = time(22, 0)

        now = datetime.now()
        today = now.date()

        def parse_hhmm(value: str) -> time:
            try:
                h, m = map(int, value.split(":"))
                return time(h, m)
            except Exception:
                return WORK_START

        # 1) Preparar intervalos ocupados por día (eventos hoy) y acumulados de tareas
        occupied_by_day: Dict[date, List[tuple[time, time]]] = {}
        occupied_by_day[today] = []
        for item in items:
            if getattr(item, 'get_type', lambda: '')() == 'Evento':
                event_date = item.get_priority_date()
                if event_date == today and hasattr(item, 'time') and item.time:
                    start_t = parse_hhmm(item.time)
                    start_dt = datetime.combine(today, start_t)
                    end_dt = start_dt + timedelta(minutes=item.duration)
                    # Establecer hora en el evento y agregar a bloque ocupado
                    item.set_time_range(start_dt.time(), end_dt.time())
                    item.planned_date = today
                    occupied_by_day[today].append((start_dt.time(), end_dt.time()))

        # Ordenar intervalos por inicio del día actual
        occupied_by_day[today].sort(key=lambda x: x[0])

        # 2) Construir bloques libres por día
        def get_free_blocks_for_day(day: date) -> List[tuple[time, time]]:
            # Obtener ocupados de ese día; si no hay, inicializar
            if day not in occupied_by_day:
                occupied_by_day[day] = []
            day_occupied = sorted(occupied_by_day[day], key=lambda x: x[0])
            # Si es hoy, no empezar antes de ahora
            start_limit = max(now.time(), WORK_START) if day == today else WORK_START
            blocks = []
            cursor = start_limit
            for s, e in day_occupied:
                if e <= cursor:
                    continue
                if s > cursor:
                    blocks.append((cursor, min(s, WORK_END)))
                cursor = max(cursor, e)
                if cursor >= WORK_END:
                    break
            if cursor < WORK_END:
                blocks.append((cursor, WORK_END))
            return [(s, e) for s, e in blocks if s < e]

        # 3) Asignar Tareas/Lecciones en huecos libres
        schedulables = [it for it in items if getattr(it, 'get_type', lambda: '')() != 'Evento']
        current_day = today
        i = 0
        while i < len(schedulables):
            free_blocks = get_free_blocks_for_day(current_day)
            if not free_blocks:
                current_day = current_day + timedelta(days=1)
                continue
            placed_any = False
            for block_start, block_end in free_blocks:
                # Mientras quede espacio en este bloque, colocar items
                cursor_dt = datetime.combine(current_day, block_start)
                end_block_dt = datetime.combine(current_day, block_end)
                while i < len(schedulables) and cursor_dt + timedelta(minutes=schedulables[i].duration) <= end_block_dt:
                    it = schedulables[i]
                    it.set_time_range(cursor_dt.time(), (cursor_dt + timedelta(minutes=it.duration)).time())
                    it.planned_date = current_day
                    # Marcar el intervalo como ocupado para este día
                    if current_day not in occupied_by_day:
                        occupied_by_day[current_day] = []
                    occupied_by_day[current_day].append((it.start_time, it.end_time))
                    occupied_by_day[current_day].sort(key=lambda x: x[0])
                    cursor_dt += timedelta(minutes=it.duration)
                    i += 1
                    placed_any = True
                if i >= len(schedulables):
                    break
            if not placed_any:
                # No hubo espacio hoy; pasar al siguiente día completo
                current_day = current_day + timedelta(days=1)

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
        
        # Obtener todos los items, asignar horarios respetando eventos fijos
        all_items = self.get_all_prioritized_items()
        self.suggest_time_slots(all_items)

        for item in all_items:
            priority_date = item.get_priority_date()
            
            if priority_date < today or priority_date == today:
                items_by_day["Para Hoy (Urgente)"].append(item)
            elif priority_date == tomorrow:
                items_by_day["Mañana"].append(item)
            elif priority_date <= week_later:
                items_by_day["Próximos 7 días"].append(item)
            else:
                items_by_day["Más adelante"].append(item)
        
        # Ordenar cada grupo por hora sugerida si existe
        for key in items_by_day:
            items_by_day[key] = sorted(
                items_by_day[key],
                key=lambda x: (x.start_time if x.start_time else time(23, 59))
            )
                
        return items_by_day

    def get_today_plan(self) -> List[PrioritizedItem]:
        """Devuelve solo los elementos planificados explícitamente para HOY.

        - Incluye eventos cuyo `get_priority_date()` sea hoy.
        - Incluye tareas y lecciones con `planned_date == hoy`.
        - Ordenado por `start_time` si existe.
        """
        today = date.today()
        all_items = self.get_all_prioritized_items()
        self.suggest_time_slots(all_items)

        today_items: List[PrioritizedItem] = []
        for item in all_items:
            if getattr(item, 'get_type', lambda: '')() == 'Evento':
                if item.get_priority_date() == today:
                    today_items.append(item)
            else:
                if getattr(item, 'planned_date', None) == today:
                    today_items.append(item)

        today_items.sort(key=lambda x: (x.start_time if x.start_time else time(23, 59)))
        return today_items

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

    # --- Estados ---
    def mark_task_completed(self, index: int) -> bool:
        if 0 <= index < len(self.data['tasks']):
            self.data['tasks'][index].status = Status.COMPLETADO
            self.saveData()
            return True
        return False

    def mark_lesson_completed(self, index: int) -> bool:
        if 0 <= index < len(self.data['lessons']):
            self.data['lessons'][index].status = Status.COMPLETADO
            self.saveData()
            return True
        return False

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
                        # Si viene notes_file y existe en el sistema, copiar a lesson_notes
                        nf = lesson_data.get('notes_file')
                        if nf:
                            try:
                                import os, shutil
                                os.makedirs('lesson_notes', exist_ok=True)
                                base_name = os.path.basename(nf)
                                target_path = os.path.join('lesson_notes', base_name)
                                if os.path.abspath(nf) != os.path.abspath(target_path):
                                    shutil.copyfile(nf, target_path)
                                lesson.notes_file = target_path
                            except Exception as e:
                                print(f"No se pudo copiar el archivo de notas: {e}")
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
    def addLesson(self, title, notes, due_date, subject, estimated_minutes: int | None = None, notes_file: str | None = None):
        # Si se proporcionó un archivo markdown, copiarlo a lesson_notes/
        saved_notes_file = None
        if notes_file:
            try:
                import os, shutil
                os.makedirs('lesson_notes', exist_ok=True)
                base_name = os.path.basename(notes_file)
                target_path = os.path.join('lesson_notes', base_name)
                if os.path.abspath(notes_file) != os.path.abspath(target_path):
                    shutil.copyfile(notes_file, target_path)
                saved_notes_file = target_path
            except Exception as e:
                print(f"No se pudo copiar el archivo de notas: {e}")
        new_lesson = Lesson(title, notes, due_date, subject, estimated_minutes=estimated_minutes, notes_file=saved_notes_file)
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

