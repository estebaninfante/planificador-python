import customtkinter as ctk
from datetime import time, datetime, timedelta

class TimeRangeDialog(ctk.CTkToplevel):
    """Diálogo para editar el rango de hora de una actividad."""
    def __init__(self, parent, title="Editar Horario", current_start=None, current_end=None, current_duration=60):
        super().__init__(parent)
        self.title(title)
        self.result = None
        
        # Configuración de la ventana
        self.geometry("400x300")
        self.resizable(False, False)
        
        # Valores actuales
        self.current_start = current_start or time(8, 0)
        self.current_end = current_end
        self.current_duration = current_duration

        self.setup_ui()
        
        # Hacer modal
        self.transient(parent)
        self.grab_set()
        self.protocol("WM_DELETE_WINDOW", self.cancel)

    def setup_ui(self):
        # Frame principal
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(padx=20, pady=20, fill="both", expand=True)

        # Hora de inicio
        start_label = ctk.CTkLabel(main_frame, text="Hora de inicio:")
        start_label.pack(pady=(0, 5))
        
        # Frame para hora y minutos de inicio
        start_frame = ctk.CTkFrame(main_frame)
        start_frame.pack(fill="x", pady=(0, 15))
        
        self.start_hour = ctk.CTkComboBox(
            start_frame,
            values=[f"{i:02d}" for i in range(24)],
            width=70
        )
        self.start_hour.set(f"{self.current_start.hour:02d}")
        self.start_hour.pack(side="left", padx=5)
        
        ctk.CTkLabel(start_frame, text=":").pack(side="left")
        
        self.start_minute = ctk.CTkComboBox(
            start_frame,
            values=[f"{i:02d}" for i in range(0, 60, 15)],
            width=70
        )
        self.start_minute.set(f"{self.current_start.minute:02d}")
        self.start_minute.pack(side="left", padx=5)

        # Duración
        duration_label = ctk.CTkLabel(main_frame, text="Duración (minutos):")
        duration_label.pack(pady=(0, 5))
        
        self.duration_entry = ctk.CTkComboBox(
            main_frame,
            values=["15", "30", "45", "60", "90", "120", "180", "240"]
        )
        self.duration_entry.set(str(self.current_duration))
        self.duration_entry.pack(pady=(0, 15))

        # Hora de finalización (calculada automáticamente)
        end_label = ctk.CTkLabel(main_frame, text="Hora de finalización (calculada):")
        end_label.pack(pady=(0, 5))
        
        self.end_time_label = ctk.CTkLabel(main_frame, text="")
        self.end_time_label.pack()
        
        # Actualizar la hora de finalización inicial
        self.update_end_time()
        
        # Botones
        button_frame = ctk.CTkFrame(main_frame)
        button_frame.pack(pady=20, fill="x")
        
        ctk.CTkButton(
            button_frame,
            text="Aceptar",
            command=self.ok
        ).pack(side="left", padx=10, expand=True)
        
        ctk.CTkButton(
            button_frame,
            text="Cancelar",
            command=self.cancel
        ).pack(side="left", padx=10, expand=True)

        # Vincular eventos
        self.start_hour.configure(command=self.update_end_time)
        self.start_minute.configure(command=self.update_end_time)
        self.duration_entry.configure(command=self.update_end_time)

    def update_end_time(self, *args):
        try:
            # Obtener hora de inicio
            start_hour = int(self.start_hour.get())
            start_minute = int(self.start_minute.get())
            duration = int(self.duration_entry.get())
            
            # Calcular hora de finalización
            start_dt = datetime.combine(datetime.today(), time(start_hour, start_minute))
            end_dt = start_dt + timedelta(minutes=duration)
            
            # Actualizar etiqueta
            self.end_time_label.configure(
                text=f"{end_dt.hour:02d}:{end_dt.minute:02d}"
            )
        except ValueError:
            self.end_time_label.configure(text="Error en los datos")

    def ok(self):
        try:
            # Crear objetos time para inicio y fin
            start_time = time(
                int(self.start_hour.get()),
                int(self.start_minute.get())
            )
            
            duration = int(self.duration_entry.get())
            
            # Calcular tiempo de finalización
            start_dt = datetime.combine(datetime.today(), start_time)
            end_dt = start_dt + timedelta(minutes=duration)
            end_time = end_dt.time()
            
            self.result = (start_time, end_time, duration)
            self.destroy()
        except ValueError:
            self.end_time_label.configure(text="Error en los datos")

    def cancel(self):
        self.result = None
        self.destroy()

    def get_result(self):
        self.wait_window()
        return self.result