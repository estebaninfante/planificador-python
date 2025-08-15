# task.py

from datetime import date
from Status import Status

class Task:
    """Clase para representar una tarea."""
    def __init__(self, title, due_date: date, status: Status = Status.PENDIENTE):
        self.title = title
        self.due_date = due_date
        self.status = status

    def __str__(self):
        return f"Tarea: {self.title} | Estado: {self.status.value} | Fecha Límite: {self.due_date}"

    def to_dict(self):
        """Convierte el objeto Task a un diccionario para guardarlo."""
        return {
            'title': self.title,
            'due_date': str(self.due_date),
            'status': self.status.value
        }

    @staticmethod
    def from_dict(data):
        """Crea un objeto Task a partir de un diccionario."""
        try:
            status = Status(data.get('status', 'Pendiente'))
            due_date = date.fromisoformat(data['due_date'])
            return Task(data['title'], due_date, status)
        except (ValueError, KeyError) as e:
            raise ValueError(f"Datos inválidos para la tarea: {data}. Error: {e}")

