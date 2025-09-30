# UserPreferences.py

class UserPreferences:
    def __init__(self):
        # Tamaño de fuente
        self.font_size = 14
        
        # Horarios de trabajo
        self.work_hours = {
            'start': '08:00',
            'end': '18:00'
        }
        
        # Bloques de tiempo
        self.time_blocks = {
            'morning': {'start': '08:00', 'end': '12:00'},
            'afternoon': {'start': '14:00', 'end': '18:00'},
            'evening': {'start': '18:00', 'end': '22:00'}
        }
        
        # Pausas y descansos
        self.breaks = {
            'duration': 15,  # minutos
            'frequency': 120  # cada 120 minutos
        }
        
        # Comidas
        self.meal_times = {
            'lunch': {'time': '12:00', 'duration': 60},
            'dinner': {'time': '19:00', 'duration': 60}
        }
        
        # Preferencias de productividad
        self.productivity_preferences = {
            'high_focus_times': [],  # Usuario define sus mejores horas
            'preferred_task_times': {
                'high_priority': 'morning',
                'medium_priority': 'afternoon',
                'low_priority': 'evening'
            }
        }

        # Días no laborables (0 = Lunes, 6 = Domingo)
        self.non_working_days = [5, 6]  # Por defecto, fin de semana

    def to_dict(self):
        """Convierte las preferencias a un diccionario para guardar"""
        return {
            'font_size': self.font_size,
            'work_hours': self.work_hours,
            'time_blocks': self.time_blocks,
            'breaks': self.breaks,
            'meal_times': self.meal_times,
            'productivity_preferences': self.productivity_preferences,
            'non_working_days': self.non_working_days
        }

    @staticmethod
    def from_dict(data):
        """Crea un objeto UserPreferences desde un diccionario"""
        prefs = UserPreferences()
        prefs.font_size = data.get('font_size', prefs.font_size)
        prefs.work_hours = data.get('work_hours', prefs.work_hours)
        prefs.time_blocks = data.get('time_blocks', prefs.time_blocks)
        prefs.breaks = data.get('breaks', prefs.breaks)
        prefs.meal_times = data.get('meal_times', prefs.meal_times)
        prefs.productivity_preferences = data.get('productivity_preferences', 
                                                prefs.productivity_preferences)
        prefs.non_working_days = data.get('non_working_days', prefs.non_working_days)
        return prefs

    def is_working_time(self, time_str):
        """Verifica si una hora está dentro del horario de trabajo"""
        return (self.work_hours['start'] <= time_str <= self.work_hours['end'])

    def get_available_block(self, start_time, duration):
        """
        Verifica si un bloque de tiempo está disponible
        considerando horarios de comida y descansos
        """
        end_time = self._add_minutes_to_time(start_time, duration)
        
        # Verificar si está en horario de trabajo
        if not self.is_working_time(start_time) or not self.is_working_time(end_time):
            return False
            
        # Verificar si interfiere con horarios de comida
        for meal in self.meal_times.values():
            meal_start = meal['time']
            meal_end = self._add_minutes_to_time(meal_start, meal['duration'])
            if self._times_overlap(start_time, end_time, meal_start, meal_end):
                return False
                
        return True

    @staticmethod
    def _add_minutes_to_time(time_str, minutes):
        """Añade minutos a una hora en formato string 'HH:MM'"""
        hours, mins = map(int, time_str.split(':'))
        total_mins = hours * 60 + mins + minutes
        new_hours = total_mins // 60
        new_mins = total_mins % 60
        return f"{new_hours:02d}:{new_mins:02d}"

    @staticmethod
    def _times_overlap(start1, end1, start2, end2):
        """Verifica si dos rangos de tiempo se solapan"""
        return start1 < end2 and start2 < end1