# lesson.py

from datetime import timedelta, date, time
import math
from PrioritizedItem import PrioritizedItem

class Lesson(PrioritizedItem):
    """Clase para representar una lección o clase."""
    def __init__(self, title, notes, due_date, subject, interval=0, repetitions=0, efactor=2.5, next_review_date=None):
        super().__init__()  # Llamar al constructor de PrioritizedItem
        self.title = title
        self.notes = notes
        self.due_date = due_date  # Fecha de creación
        self.subject = subject
        self.repetitions = int(repetitions) 
        self.efactor = float(efactor)
        self.interval = int(interval)
        self.next_review_date = next_review_date       

        # Si es una lección nueva, calcula la primera fecha de repaso
        if next_review_date is None:
            creation_date = date.fromisoformat(self.due_date) if isinstance(self.due_date, str) else self.due_date
            self.next_review_date = creation_date + timedelta(days=1)
        else:
            self.next_review_date = date.fromisoformat(next_review_date) if isinstance(next_review_date, str) else next_review_date

    def get_priority_date(self) -> date:
        """Implementa el método abstracto de PrioritizedItem."""
        return self.next_review_date

    def get_priority_time(self) -> str:
        """Implementa el método abstracto de PrioritizedItem."""
        return ""  # Las lecciones no tienen hora específica

    def get_type(self) -> str:
        """Implementa el método abstracto de PrioritizedItem."""
        return "Lección"

    def review_lesson(self, score):
        if score < 3:
            self.repetitions = 0
            self.interval = 1
        else:
            if self.repetitions == 0:
                self.interval = 1
            elif self.repetitions == 1:
                self.interval = 6
            else:
                self.interval = math.ceil(self.interval * self.efactor)

            self.repetitions += 1
            
            self.efactor += (0.1 - (5 - score) * (0.08 + (5 - score) * 0.02))
            if self.efactor < 1.3:
                self.efactor = 1.3

        if score <= 1.3 and self.efactor < 1.3:
            self.efactor = 1.3

        self.next_review_date = date.today() + timedelta(days=self.interval)
        return {
            "efactor": self.efactor,
            "interval": self.interval,
            "repetitions": self.repetitions,
            "next_review_date": self.next_review_date
        }



    def __str__(self):
        return f"Clase: {self.title} | Materia: {self.subject} | Fecha: {self.due_date}"

    def to_dict(self):
        """Convierte el objeto Lesson a un diccionario para guardarlo."""
        return {
            'title': self.title,
            'notes': self.notes,
            'due_date': str(self.due_date),
            'subject': self.subject,
            'efactor': self.efactor,        
            'repetitions': self.repetitions,
            'next_review_date': str(self.next_review_date),
            'interval': self.interval,
            'start_time': self.start_time.strftime('%H:%M') if self.start_time else None,
            'end_time': self.end_time.strftime('%H:%M') if self.end_time else None,
            'duration': self.duration
        }
    
    @staticmethod
    def from_dict(data):
        """Crea un objeto Lesson a partir de un diccionario."""
        lesson = Lesson(
            data['title'], 
            data['notes'], 
            data['due_date'], 
            data['subject'],
            interval=data.get('interval', 0),
            repetitions=data.get('repetitions', 0),
            efactor=data.get('efactor', 2.5),
            next_review_date=data.get('next_review_date')
        )
        
        # Recuperar información de tiempo si existe
        if data.get('start_time'):
            h, m = map(int, data['start_time'].split(':'))
            lesson.start_time = time(h, m)
        if data.get('end_time'):
            h, m = map(int, data['end_time'].split(':'))
            lesson.end_time = time(h, m)
        if data.get('duration'):
            lesson.duration = int(data['duration'])
            
        return lesson