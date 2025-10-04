# PreferencesDialog.py

import customtkinter as ctk
from datetime import datetime
from UserPreferences import UserPreferences

class PreferencesDialog(ctk.CTkToplevel):
    def __init__(self, parent, user_preferences=None):
        super().__init__(parent)
        
        self.title("Preferencias de Usuario")
        self.geometry("600x800")
        
        # Si no se proporcionan preferencias, crear nuevas
        self.preferences = user_preferences if user_preferences else UserPreferences()
        
        # Crear frame con scroll
        self.main_frame = ctk.CTkScrollableFrame(self)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        self._create_font_section()
        self._create_work_hours_section()
        self._create_time_blocks_section()
        self._create_breaks_section()
        self._create_meal_times_section()
        self._create_productivity_section()
        self._create_non_working_days_section()
        
        # Botones
        self.button_frame = ctk.CTkFrame(self)
        self.button_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkButton(
            self.button_frame,
            text="Guardar",
            command=self._save_preferences
        ).pack(side="right", padx=5)
        
        ctk.CTkButton(
            self.button_frame,
            text="Cancelar",
            command=self.destroy
        ).pack(side="right", padx=5)

    def _create_section_header(self, title):
        """Crea un encabezado de sección"""
        frame = ctk.CTkFrame(self.main_frame)
        frame.pack(fill="x", pady=(10, 5))
        
        ctk.CTkLabel(
            frame,
            text=title,
            font=("", 16, "bold")
        ).pack(anchor="w", padx=5, pady=5)
        
        return frame

    def _create_font_section(self):
        """Crea la sección de configuración de fuente"""
        section = self._create_section_header("Configuración de Fuente")
        
        frame = ctk.CTkFrame(self.main_frame)
        frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(frame, text="Tamaño de fuente:").pack(side="left", padx=5)
        
        self.font_size = ctk.CTkEntry(frame, width=50)
        self.font_size.insert(0, str(self.preferences.font_size))
        self.font_size.pack(side="left", padx=5)
        
        ctk.CTkLabel(frame, text="(Recomendado: 12-18)").pack(side="left", padx=5)

    def _create_work_hours_section(self):
        """Crea la sección de horarios de trabajo"""
        section = self._create_section_header("Horario de Trabajo")
        
        frame = ctk.CTkFrame(self.main_frame)
        frame.pack(fill="x", pady=5)
        
        # Inicio
        ctk.CTkLabel(frame, text="Hora de inicio:").pack(side="left", padx=5)
        self.work_start = ctk.CTkEntry(frame, width=100)
        self.work_start.insert(0, self.preferences.work_hours['start'])
        self.work_start.pack(side="left", padx=5)
        
        # Fin
        ctk.CTkLabel(frame, text="Hora de fin:").pack(side="left", padx=5)
        self.work_end = ctk.CTkEntry(frame, width=100)
        self.work_end.insert(0, self.preferences.work_hours['end'])
        self.work_end.pack(side="left", padx=5)

    def _create_time_blocks_section(self):
        """Crea la sección de bloques de tiempo"""
        section = self._create_section_header("Bloques de Tiempo")
        
        # Mañana
        morning_frame = ctk.CTkFrame(self.main_frame)
        morning_frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(morning_frame, text="Mañana:").pack(side="left", padx=5)
        self.morning_start = ctk.CTkEntry(morning_frame, width=100)
        self.morning_start.insert(0, self.preferences.time_blocks['morning']['start'])
        self.morning_start.pack(side="left", padx=5)
        
        ctk.CTkLabel(morning_frame, text="a").pack(side="left", padx=5)
        self.morning_end = ctk.CTkEntry(morning_frame, width=100)
        self.morning_end.insert(0, self.preferences.time_blocks['morning']['end'])
        self.morning_end.pack(side="left", padx=5)
        
        # Tarde
        afternoon_frame = ctk.CTkFrame(self.main_frame)
        afternoon_frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(afternoon_frame, text="Tarde:").pack(side="left", padx=5)
        self.afternoon_start = ctk.CTkEntry(afternoon_frame, width=100)
        self.afternoon_start.insert(0, self.preferences.time_blocks['afternoon']['start'])
        self.afternoon_start.pack(side="left", padx=5)
        
        ctk.CTkLabel(afternoon_frame, text="a").pack(side="left", padx=5)
        self.afternoon_end = ctk.CTkEntry(afternoon_frame, width=100)
        self.afternoon_end.insert(0, self.preferences.time_blocks['afternoon']['end'])
        self.afternoon_end.pack(side="left", padx=5)
        
        # Noche
        evening_frame = ctk.CTkFrame(self.main_frame)
        evening_frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(evening_frame, text="Noche:").pack(side="left", padx=5)
        self.evening_start = ctk.CTkEntry(evening_frame, width=100)
        self.evening_start.insert(0, self.preferences.time_blocks['evening']['start'])
        self.evening_start.pack(side="left", padx=5)
        
        ctk.CTkLabel(evening_frame, text="a").pack(side="left", padx=5)
        self.evening_end = ctk.CTkEntry(evening_frame, width=100)
        self.evening_end.insert(0, self.preferences.time_blocks['evening']['end'])
        self.evening_end.pack(side="left", padx=5)

    def _create_breaks_section(self):
        """Crea la sección de configuración de pausas"""
        section = self._create_section_header("Pausas y Descansos")
        
        frame = ctk.CTkFrame(self.main_frame)
        frame.pack(fill="x", pady=5)
        
        # Duración de la pausa
        ctk.CTkLabel(frame, text="Duración (min):").pack(side="left", padx=5)
        self.break_duration = ctk.CTkEntry(frame, width=50)
        self.break_duration.insert(0, str(self.preferences.breaks['duration']))
        self.break_duration.pack(side="left", padx=5)
        
        # Frecuencia
        ctk.CTkLabel(frame, text="Cada (min):").pack(side="left", padx=5)
        self.break_frequency = ctk.CTkEntry(frame, width=50)
        self.break_frequency.insert(0, str(self.preferences.breaks['frequency']))
        self.break_frequency.pack(side="left", padx=5)

    def _create_meal_times_section(self):
        """Crea la sección de horarios de comida"""
        section = self._create_section_header("Horarios de Comida")
        
        # Almuerzo
        lunch_frame = ctk.CTkFrame(self.main_frame)
        lunch_frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(lunch_frame, text="Almuerzo:").pack(side="left", padx=5)
        self.lunch_time = ctk.CTkEntry(lunch_frame, width=100)
        self.lunch_time.insert(0, self.preferences.meal_times['lunch']['time'])
        self.lunch_time.pack(side="left", padx=5)
        
        ctk.CTkLabel(lunch_frame, text="Duración (min):").pack(side="left", padx=5)
        self.lunch_duration = ctk.CTkEntry(lunch_frame, width=50)
        self.lunch_duration.insert(0, str(self.preferences.meal_times['lunch']['duration']))
        self.lunch_duration.pack(side="left", padx=5)
        
        # Cena
        dinner_frame = ctk.CTkFrame(self.main_frame)
        dinner_frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(dinner_frame, text="Cena:").pack(side="left", padx=5)
        self.dinner_time = ctk.CTkEntry(dinner_frame, width=100)
        self.dinner_time.insert(0, self.preferences.meal_times['dinner']['time'])
        self.dinner_time.pack(side="left", padx=5)
        
        ctk.CTkLabel(dinner_frame, text="Duración (min):").pack(side="left", padx=5)
        self.dinner_duration = ctk.CTkEntry(dinner_frame, width=50)
        self.dinner_duration.insert(0, str(self.preferences.meal_times['dinner']['duration']))
        self.dinner_duration.pack(side="left", padx=5)

    def _create_productivity_section(self):
        """Crea la sección de preferencias de productividad"""
        section = self._create_section_header("Preferencias de Productividad")
        
        frame = ctk.CTkFrame(self.main_frame)
        frame.pack(fill="x", pady=5)
        
        # Preferencias por prioridad
        priorities = ['high_priority', 'medium_priority', 'low_priority']
        blocks = ['morning', 'afternoon', 'evening']
        
        for priority in priorities:
            pref_frame = ctk.CTkFrame(frame)
            pref_frame.pack(fill="x", pady=2)
            
            ctk.CTkLabel(
                pref_frame,
                text=f"Tareas de prioridad {priority.split('_')[0]}:"
            ).pack(side="left", padx=5)
            
            var = ctk.StringVar(value=self.preferences.productivity_preferences['preferred_task_times'][priority])
            
            for block in blocks:
                ctk.CTkRadioButton(
                    pref_frame,
                    text=block.capitalize(),
                    variable=var,
                    value=block
                ).pack(side="left", padx=10)
                
            setattr(self, f"{priority}_var", var)

    def _create_non_working_days_section(self):
        """Crea la sección de días no laborables"""
        section = self._create_section_header("Días No Laborables")
        
        frame = ctk.CTkFrame(self.main_frame)
        frame.pack(fill="x", pady=5)
        
        days = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
        self.day_vars = []
        
        for i, day in enumerate(days):
            var = ctk.BooleanVar(value=i in self.preferences.non_working_days)
            self.day_vars.append(var)
            
            ctk.CTkCheckBox(
                frame,
                text=day,
                variable=var
            ).pack(side="left", padx=5)

    def _save_preferences(self):
        """Guarda las preferencias y cierra el diálogo"""
        # Actualizar tamaño de fuente
        try:
            self.preferences.font_size = int(self.font_size.get())
        except ValueError:
            self.preferences.font_size = 14  # Valor por defecto si hay error
        
        # Actualizar horarios de trabajo
        self.preferences.work_hours['start'] = self.work_start.get()
        self.preferences.work_hours['end'] = self.work_end.get()
        
        # Actualizar bloques de tiempo
        self.preferences.time_blocks['morning']['start'] = self.morning_start.get()
        self.preferences.time_blocks['morning']['end'] = self.morning_end.get()
        self.preferences.time_blocks['afternoon']['start'] = self.afternoon_start.get()
        self.preferences.time_blocks['afternoon']['end'] = self.afternoon_end.get()
        self.preferences.time_blocks['evening']['start'] = self.evening_start.get()
        self.preferences.time_blocks['evening']['end'] = self.evening_end.get()
        
        # Actualizar pausas
        self.preferences.breaks['duration'] = int(self.break_duration.get())
        self.preferences.breaks['frequency'] = int(self.break_frequency.get())
        
        # Actualizar comidas
        self.preferences.meal_times['lunch']['time'] = self.lunch_time.get()
        self.preferences.meal_times['lunch']['duration'] = int(self.lunch_duration.get())
        self.preferences.meal_times['dinner']['time'] = self.dinner_time.get()
        self.preferences.meal_times['dinner']['duration'] = int(self.dinner_duration.get())
        
        # Actualizar preferencias de productividad
        for priority in ['high_priority', 'medium_priority', 'low_priority']:
            var = getattr(self, f"{priority}_var")
            self.preferences.productivity_preferences['preferred_task_times'][priority] = var.get()
        
        # Actualizar días no laborables
        self.preferences.non_working_days = [
            i for i, var in enumerate(self.day_vars) if var.get()
        ]
        
        self.destroy()

    def get_preferences(self):
        """Retorna las preferencias actualizadas"""
        return self.preferences