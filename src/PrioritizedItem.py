from abc import ABC, abstractmethod
from datetime import date, datetime, time, timedelta

class PrioritizedItem(ABC):
    """Clase base abstracta para elementos priorizables."""
    
    def __init__(self):
        self.start_time = None  # Hora de inicio sugerida
        self.end_time = None    # Hora de finalización sugerida
        self.duration = 60      # Duración predeterminada en minutos
        self.planned_date = None  # Fecha planificada (no persistente)
    
    @abstractmethod
    def get_priority_date(self) -> date:
        """Retorna la fecha que se usará para la priorización."""
        pass
    
    @abstractmethod
    def get_priority_time(self) -> str:
        """Retorna la hora del elemento (si aplica)."""
        if self.start_time and self.end_time:
            return f"{self.start_time.strftime('%H:%M')} - {self.end_time.strftime('%H:%M')}"
        return ""

    @abstractmethod
    def get_type(self) -> str:
        """Retorna el tipo de elemento (Tarea, Evento, Lección)."""
        pass

    def set_time_range(self, start_time: time, end_time: time = None):
        """Establece el rango de tiempo para el elemento."""
        self.start_time = start_time
        if end_time:
            self.end_time = end_time
        else:
            # Si no se proporciona end_time, calcular basado en la duración
            start_dt = datetime.combine(date.today(), start_time)
            end_dt = start_dt + timedelta(minutes=self.duration)
            self.end_time = end_dt.time()

    def set_duration(self, minutes: int):
        """Establece la duración estimada de la actividad."""
        self.duration = minutes
        if self.start_time:
            # Actualizar end_time basado en la nueva duración
            start_dt = datetime.combine(date.today(), self.start_time)
            end_dt = start_dt + timedelta(minutes=minutes)
            self.end_time = end_dt.time()

    def get_suggested_time_slot(self) -> tuple:
        """Retorna una sugerencia de horario basada en el tipo y estado."""
        today = date.today()
        priority_date = self.get_priority_date()
        
        if priority_date < today:
            # Para elementos vencidos, sugerir el siguiente horario disponible
            now = datetime.now().time()
            if now.hour < 22:  # Si aún hay tiempo hoy
                start = time(now.hour + 1, 0)
            else:  # Si es muy tarde, programar para mañana temprano
                start = time(8, 0)
            
            # Calcular hora de finalización
            start_dt = datetime.combine(date.today(), start)
            end_dt = start_dt + timedelta(minutes=self.duration)
            return start, end_dt.time()
            
        return None, None  # Para elementos futuros, no sugerir horario automáticamente

    def get_days_remaining(self) -> int:
        """Calcula los días restantes hasta la fecha de prioridad."""
        priority_date = self.get_priority_date()
        # Normalizar a date si viene como string
        if isinstance(priority_date, str):
            try:
                priority_date = date.fromisoformat(priority_date)
            except Exception:
                return 0
        return (priority_date - date.today()).days if priority_date else 0

    def get_priority_text(self) -> str:
        """Retorna un texto descriptivo de la prioridad."""
        days = self.get_days_remaining()
        if days < 0:
            return "¡VENCIDO!"
        elif days == 0:
            return "¡HOY!"
        elif days == 1:
            return "¡MAÑANA!"
        else:
            return f"{days} DÍAS"

    def __lt__(self, other):
        """Permite comparación para el heap basada en fecha y hora."""
        if not isinstance(other, PrioritizedItem):
            return NotImplemented
        
        self_date = self.get_priority_date()
        other_date = other.get_priority_date()
        
        if self_date != other_date:
            return self_date < other_date
        
        # Si las fechas son iguales, comparar por hora
        self_time = self.get_priority_time()
        other_time = other.get_priority_time()
        
        if self_time and other_time:
            return self_time < other_time
        elif self_time:
            return True  # Items con hora tienen prioridad sobre los que no la tienen
        elif other_time:
            return False
        return False  # Si ninguno tiene hora, mantener el orden actual