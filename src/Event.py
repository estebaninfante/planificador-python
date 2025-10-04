# event.py

from datetime import date, time
from PrioritizedItem import PrioritizedItem

class Event(PrioritizedItem):
    """Clase para representar un evento."""
    def __init__(self, title, description, due_date, time):
        super().__init__()  # Llamar al constructor de PrioritizedItem
        self.title = title
        self.description = description
        self.due_date = due_date
        self.time = time
        self.is_fixed = True  # Los eventos son fijos por defecto

    def __str__(self):
        return f"Evento: {self.title} | Descripción: {self.description} | Fecha: {self.due_date} | Hora: {self.time}"

    def get_priority_date(self) -> date:
        """Implementa el método abstracto de PrioritizedItem."""
        return date.fromisoformat(self.due_date) if isinstance(self.due_date, str) else self.due_date

    def get_priority_time(self) -> str:
        """Implementa el método abstracto de PrioritizedItem."""
        return self.time

    def get_type(self) -> str:
        """Implementa el método abstracto de PrioritizedItem."""
        return "Evento"
    
    def to_dict(self):
        """Convierte el objeto Event a un diccionario para guardarlo."""
        return {
            'title': self.title,
            'description': self.description,
            'due_date': self.due_date,
            'time': self.time,
            'start_time': self.start_time.strftime('%H:%M') if self.start_time else None,
            'end_time': self.end_time.strftime('%H:%M') if self.end_time else None,
            'duration': self.duration,
            'is_fixed': self.is_fixed
        }

    @staticmethod
    def from_dict(data):
        """Crea un objeto Event a partir de un diccionario."""
        event = Event(data['title'], data['description'], data['due_date'], data['time'])
        
        # Recuperar información de tiempo si existe
        if data.get('start_time'):
            h, m = map(int, data['start_time'].split(':'))
            event.start_time = time(h, m)
        if data.get('end_time'):
            h, m = map(int, data['end_time'].split(':'))
            event.end_time = time(h, m)
        if data.get('duration'):
            event.duration = int(data['duration'])
            
        return event

