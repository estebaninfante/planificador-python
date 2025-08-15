# lesson.py

class Lesson:
    """Clase para representar una lección o clase."""
    def __init__(self, title, notes, due_date, subject):
        self.title = title
        self.notes = notes
        self.due_date = due_date
        self.subject = subject

    def __str__(self):
        return f"Clase: {self.title} | Materia: {self.subject} | Fecha: {self.due_date}"

    def to_dict(self):
        """Convierte el objeto Lesson a un diccionario para guardarlo."""
        return {
            'title': self.title,
            'notes': self.notes,
            'due_date': self.due_date,
            'subject': self.subject
        }
    
    @staticmethod
    def from_dict(data):
        """Crea un objeto Lesson a partir de un diccionario."""
        return Lesson(data['title'], data['notes'], data['due_date'], data['subject'])
