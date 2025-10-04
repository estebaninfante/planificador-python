# task.py

from datetime import date, time
from Status import Status
from PrioritizedItem import PrioritizedItem

class Task(PrioritizedItem):
    """Clase para representar una tarea."""
    def __init__(self, title, due_date: date, status: Status = Status.PENDIENTE, estimated_minutes: int | None = None):
        super().__init__()  # Llamar al constructor de PrioritizedItem
        self.title = title
        self.due_date = due_date
        self.status = status
        if estimated_minutes:
            self.duration = int(estimated_minutes)
        self.estimated_minutes = int(estimated_minutes) if estimated_minutes else None

    def __str__(self):
        return f"Tarea: {self.title} | Estado: {self.status.value} | Fecha Límite: {self.due_date}"

    def get_priority_date(self) -> date:
        """Implementa el método abstracto de PrioritizedItem."""
        # Normalizar a date si vino como string
        return date.fromisoformat(self.due_date) if isinstance(self.due_date, str) else self.due_date

    def get_priority_time(self) -> str:
        """Implementa el método abstracto de PrioritizedItem."""
        return ""  # Las tareas no tienen hora específica

    def get_type(self) -> str:
        """Implementa el método abstracto de PrioritizedItem."""
        return "Tarea"

    def to_dict(self):
        """Convierte el objeto Task a un diccionario para guardarlo."""
        return {
            'title': self.title,
            'due_date': str(self.due_date),
            'status': self.status.value,
            'start_time': self.start_time.strftime('%H:%M') if self.start_time else None,
            'end_time': self.end_time.strftime('%H:%M') if self.end_time else None,
            'duration': self.duration,
            'estimated_minutes': self.estimated_minutes
        }

    @staticmethod
    def from_dict(data):
        """Crea un objeto Task a partir de un diccionario."""
        try:
            status = Status(data.get('status', 'Pendiente'))
            # due_date puede llegar como str o date
            raw_due = data['due_date']
            due_date = date.fromisoformat(raw_due) if isinstance(raw_due, str) else raw_due
            estimated = data.get('estimated_minutes')
            task = Task(data['title'], due_date, status, estimated_minutes=estimated)
            
            # Recuperar información de tiempo si existe
            if data.get('start_time'):
                h, m = map(int, data['start_time'].split(':'))
                task.start_time = time(h, m)
            if data.get('end_time'):
                h, m = map(int, data['end_time'].split(':'))
                task.end_time = time(h, m)
            if data.get('duration'):
                task.duration = int(data['duration'])
                
            return task
        except (ValueError, KeyError) as e:
            raise ValueError(f"Datos inválidos para la tarea: {data}. Error: {e}")

