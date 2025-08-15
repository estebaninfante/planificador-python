# event.py

class Event:
    """Clase para representar un evento."""
    def __init__(self, title, description, due_date, time):
        self.title = title
        self.description = description
        self.due_date = due_date
        self.time = time

    def __str__(self):
        return f"Evento: {self.title} | Descripción: {self.description} | Fecha: {self.due_date} | Hora: {self.time}"

    def to_dict(self):
        """Convierte el objeto Event a un diccionario para guardarlo."""
        return {
            'title': self.title,
            'description': self.description,
            'due_date': self.due_date,
            'time': self.time
        }

    @staticmethod
    def from_dict(data):
        """Crea un objeto Event a partir de un diccionario."""
        return Event(data['title'], data['description'], data['due_date'], data['time'])

