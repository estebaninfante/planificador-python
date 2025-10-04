# lesson.py

from datetime import timedelta, date
import math

class Lesson:
    
    def __init__(self, title, notes, due_date, subject, interval=0, repetitions=0, efactor=2.5, next_review_date=None):
        
       
        self.title = title        # c1
        self.notes = notes        # c1
        self.due_date = due_date  # c1
        self.subject = subject    # c1
        self.repetitions = int(repetitions)  # c1 + cf_int
        self.efactor = float(efactor)        # c1 + cf_float
        self.interval = int(interval)        # c1 + cf_int
        self.next_review_date = next_review_date  # c1

       
        if next_review_date is None:          # comparación -> c2
            creation_date = date.fromisoformat(self.due_date)           # c1 + cf_date_parse
            self.next_review_date = creation_date + timedelta(days=1)   # c1 + cf_timedelta

        else:

            # Convierte string a fecha si es necesario
            self.next_review_date = date.fromisoformat(next_review_date) if isinstance(next_review_date, str) else next_review_date
            
            # c1 + cf_date_parse (si string) + c2   


    # T(__init__) ≈ 8*c1 + 3*cf_conversion + c2 + cf_date_parse + cf_timedelta
    # Complejidad: O(1) 


    def review_lesson(self, score):

        # Comparación inicial -> c2
        if score < 3:
            # Asignaciones constantes -> 2*c1
            self.repetitions = 0
            self.interval = 1
        else:

            # Condicional -> c2
            if self.repetitions == 0:   # c2
                self.interval = 1       # c1
            elif self.repetitions == 1: # c2
                self.interval = 6       # c1
            else:
               
                self.interval = math.ceil(self.interval * self.efactor)   # -> c1 + cf_math


            self.repetitions += 1       # -> c1 + cf_int
            
            # Cálculo de efactor -> c1 + 6*c3
            self.efactor += (0.1 - (5 - score) * (0.08 + (5 - score) * 0.02))
            
            # Condicional -> c2
            if self.efactor < 1.3:
                self.efactor = 1.3   # c1

        # Condicional final -> c2
        if score <= 1.3 and self.efactor < 1.3:
            self.efactor = 1.3       # c1

        # Cálculo de la siguiente fecha de repaso
        # date.today() -> cf_date
        # timedelta -> cf_timedelta

        self.next_review_date = date.today() + timedelta(days=self.interval)  # c1 + cf_date + cf_timedelta

        # Retorno -> 4*c1
        return {
            "efactor": self.efactor,
            "interval": self.interval,
            "repetitions": self.repetitions,
            "next_review_date": self.next_review_date
        }

    # T(review_lesson) ≈ 6*c3 + 10*c1 + 5*c2 + cf_math + cf_int + cf_date + cf_timedelta
    # Complejidad: O(1) 

        



    def __str__(self):
       
        # Acceso a atributos -> 3*c1 (title, subject, due_date)
        # Formateo de string -> cf_format

        return f"Clase: {self.title} | Materia: {self.subject} | Fecha: {self.due_date}"

    # T(__str__) ≈ 3*c1 + cf_format
    # Complejidad: O(1) 

    def to_dict(self):
        """Convierte el objeto Lesson a un diccionario para guardarlo."""
        
        
        # Conversión de fechas a string -> 2*cf_str (due_date y next_review_date)
        return {
            'title': self.title,                     # c1
            'notes': self.notes,                     # c1
            'due_date': str(self.due_date),          # c1 + cf_str
            'subject': self.subject,                 # c1
            'efactor': self.efactor,                 # c1
            'repetitions': self.repetitions,         # c1
            'next_review_date': str(self.next_review_date),  # c1 + cf_str
            'interval': self.interval                # c1
        }

    # T(to_dict) = 8*c1 + 2*cf_str
    # Complejidad: O(1)
    
    @staticmethod

    def from_dict(data):
        """Crea un objeto Lesson a partir de un diccionario."""

        # Acceso a claves del diccionario -> 4*c1 (title, notes, due_date, subject)
        # Acceso a claves con get() -> 4*c1 (interval, repetitions, efactor, next_review_date)
        # Llamada al constructor Lesson(...) -> cf_lesson_init + c1

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

    # T(from_dict) = 8*c1 + cf_lesson_init
    # Complejidad: O(1) 