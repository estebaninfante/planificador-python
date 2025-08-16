# lesson.py

from datetime import timedelta, date
import math

class Lesson:
    """Clase para representar una lección o clase."""
    def __init__(self, title, notes, due_date, subject, interval=0, repetitions=0, efactor=2.5, next_review_date=None):
        
        self.title = title
        self.notes = notes
        self.due_date = due_date # Fecha de creación
        self.subject = subject
        self.repetitions = int(repetitions) 
        self.efactor = float(efactor)
        self.interval = int(interval)
        self.next_review_date = next_review_date       

        # Si es una lección nueva, calcula la primera fecha de repaso
        if next_review_date is None:
            creation_date = date.fromisoformat(self.due_date)
            self.next_review_date = creation_date + timedelta(days=1)

        else:
            # Carga la fecha desde el archivo JSON
            self.next_review_date = date.fromisoformat(next_review_date) if isinstance(next_review_date, str) else next_review_date

    def review_lesson(self, score):
        if score <= 1.3:
            self.efactor = 1.3
        
        elif score < 3:
            self.repetitions = 0
            self.interval = 1
        
        elif score >= 3:    
            if self.repetitions == 0:
                self.interval = 1
            elif self.repetitions == 1:
                self.interval = 6
            else:
                self.interval = self.interval * self.efactor

        if self.repetitions >= 2:
            self.efactor = self.newEaseFactor(score)
        
        self.repetitions += 1

        if self.repetitions >= 3:
            self.interval = math.ceil(self.interval * self.efactor)

        self.next_review_date = date.today() + timedelta(days=self.interval)

    def newEaseFactor(self, score):
        new_efactor = self.efactor + (0.1 - (5- score)*(0.08 + (5 - score) * 0.02))
        return new_efactor



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
            'interval': self.interval
        }
    
    @staticmethod
    def from_dict(data):
        """Crea un objeto Lesson a partir de un diccionario."""
        return Lesson(
                data['title'], 
            data['notes'], 
            data['due_date'], 
            data['subject'],
            interval=data.get('interval', 0),
            repetitions=data.get('repetitions', 0),
            efactor=data.get('efactor', 2.5),
            next_review_date=data.get('next_review_date')
        )