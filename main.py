from gui import App

if __name__ == "__main__":
    app = App()
    app.mainloop()# dialogs.py

import customtkinter as ctk
from tkinter import messagebox, ttk
from tkcalendar import DateEntry

class BaseDialog(ctk.CTkToplevel):
    """Clase base para las ventanas de diálogo modales con validación y botones."""
    def __init__(self, parent, title=""):
        super().__init__(parent)
        self.title(title)
        self.result = None
        self.parent = parent
        self.initial_focus = None

        # --- Configuración Modal ---
        self.transient(parent) # Mantener por encima de la ventana principal
        self.grab_set()        # Capturar todo el input
        self.protocol("WM_DELETE_WINDOW", self._cancel_event) # Manejar cierre con 'X'

        # --- Contenedor Principal ---
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(padx=20, pady=20, expand=True, fill="both")

        # --- Crear el cuerpo y los botones ---
        self.body_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.body_frame.pack(pady=(0, 20))
        
        self.button_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.button_frame.pack()
        
        self.create_body()
        self.create_buttons()

        if self.initial_focus:
            self.initial_focus.focus_set()
        
        self.parent.wait_window(self)

    def create_body(self):
        """Método para ser sobrescrito por las clases hijas para crear el contenido."""
        pass

    def create_buttons(self):
        """Crea los botones Aceptar y Cancelar."""
        ok_button = ctk.CTkButton(self.button_frame, text="Aceptar", width=110, command=self._ok_event)
        ok_button.pack(side="left", padx=(0, 10))
        
        cancel_button = ctk.CTkButton(self.button_frame, text="Cancelar", width=110, command=self._cancel_event, fg_color="#757575", hover_color="#616161")
        cancel_button.pack(side="left")

    def _ok_event(self, event=None):
        if not self.validate():
            return
        self.apply()
        self.destroy()
        
    def _cancel_event(self, event=None):
        self.result = None
        self.destroy()

    def validate(self):
        return True

    def apply(self):
        pass
        
    def get_input(self):
        return self.result

class AddTaskDialog(BaseDialog):
    def __init__(self, parent):
        super().__init__(parent, title="Agregar Nueva Tarea")
    
    def create_body(self):
        ctk.CTkLabel(self.body_frame, text="Título:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.title_entry = ctk.CTkEntry(self.body_frame, width=250)
        self.title_entry.grid(row=0, column=1, padx=5, pady=5)
        self.initial_focus = self.title_entry

        ctk.CTkLabel(self.body_frame, text="Fecha Límite:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.due_date_entry = DateEntry(self.body_frame, 
                                        date_pattern='y-mm-dd',
                                        style="Custom.TCombobox",
                                        borderwidth=0,
                                        font=("", 12))
        self.due_date_entry.grid(row=1, column=1, sticky="w", padx=5, pady=5)
    
    def validate(self):
        if not self.title_entry.get():
            messagebox.showwarning("Campo Vacío", "El campo 'Título' es obligatorio.", parent=self)
            return False
        return True

    def apply(self):
        self.result = (self.title_entry.get(), self.due_date_entry.get())

class AddEventDialog(BaseDialog):
    def __init__(self, parent):
        super().__init__(parent, title="Agregar Nuevo Evento")
    
    def create_body(self):
        self.entries = {}
        labels = ["Título:", "Descripción:", "Fecha:", "Hora:"]
        for i, text in enumerate(labels):
            ctk.CTkLabel(self.body_frame, text=text).grid(row=i, column=0, sticky="w", padx=5, pady=5)

        self.entries["Título"] = ctk.CTkEntry(self.body_frame, width=250)
        self.entries["Descripción"] = ctk.CTkEntry(self.body_frame, width=250)
        
        self.entries["Título"].grid(row=0, column=1, padx=5, pady=5)
        self.entries["Descripción"].grid(row=1, column=1, padx=5, pady=5)
        self.initial_focus = self.entries["Título"]

        self.due_date_entry = DateEntry(self.body_frame,
                                        date_pattern='y-mm-dd',
                                        style="Custom.TCombobox",
                                        borderwidth=0,
                                        font=("", 12))
        self.due_date_entry.grid(row=2, column=1, sticky="w", padx=5, pady=5)

        time_frame = ctk.CTkFrame(self.body_frame, fg_color="transparent")
        self.hour_spinbox = ttk.Spinbox(time_frame, from_=0, to=23, wrap=True, format="%02.0f", width=4)
        self.minute_spinbox = ttk.Spinbox(time_frame, from_=0, to=59, wrap=True, format="%02.0f", width=4)
        self.hour_spinbox.pack(side="left")
        ctk.CTkLabel(time_frame, text=":").pack(side="left", padx=2)
        self.minute_spinbox.pack(side="left")
        time_frame.grid(row=3, column=1, sticky="w", padx=5, pady=5)

    def validate(self):
        for name, entry in self.entries.items():
            if not entry.get():
                messagebox.showwarning("Campo Vacío", f"El campo '{name}' es obligatorio.", parent=self)
                return False
        return True
    
    def apply(self):
        time = f"{self.hour_spinbox.get()}:{self.minute_spinbox.get()}"
        self.result = (self.entries["Título"].get(), self.entries["Descripción"].get(), self.due_date_entry.get(), time)

class AddLessonDialog(BaseDialog):
    def __init__(self, parent):
        super().__init__(parent, title="Agregar Nueva Lección")
    
    def create_body(self):
        self.entries = {}
        labels = ["Título:", "Notas:", "Asignatura:"]
        for i, text in enumerate(labels):
            ctk.CTkLabel(self.body_frame, text=text).grid(row=i, column=0, sticky="w", padx=5, pady=5)
            entry = ctk.CTkEntry(self.body_frame, width=250)
            entry.grid(row=i, column=1, padx=5, pady=5)
            self.entries[text.replace(":", "")] = entry

        self.initial_focus = self.entries["Título"]

        ctk.CTkLabel(self.body_frame, text="Fecha:").grid(row=len(labels), column=0, sticky="w", padx=5, pady=5)
        self.due_date_entry = DateEntry(self.body_frame,
                                        date_pattern='y-mm-dd',
                                        style="Custom.TCombobox",
                                        borderwidth=0,
                                        font=("", 12))
        self.due_date_entry.grid(row=len(labels), column=1, sticky="w", padx=5, pady=5)

    def validate(self):
        for name, entry in self.entries.items():
            if not entry.get():
                messagebox.showwarning("Campo Vacío", f"El campo '{name}' es obligatorio.", parent=self)
                return False
        return True

    def apply(self):
        self.result = (self.entries["Título"].get(), self.entries["Notas"].get(), self.due_date_entry.get(), self.entries["Asignatura"].get())

# --- Esta es la clase que necesitas implementar ---
class ReviewScoreDialog(BaseDialog):
    """Diálogo para que el usuario califique su repaso."""
    def __init__(self, parent):
        super().__init__(parent, title="Calificar Repaso")

    def create_body(self):
        ctk.CTkLabel(self.body_frame, text="¿Qué tal te fue con esta lección?", font=("", 16)).pack(pady=(0, 20))

        scores_frame = ctk.CTkFrame(self.body_frame, fg_color="transparent")
        scores_frame.pack()
        
        scores = {
            1: ("Fallé", "#D32F2F"), 2: ("Difícil", "#F57C00"), 3: ("Normal", "#1976D2"),
            4: ("Fácil", "#388E3C"), 5: ("Muy Fácil", "#00796B")
        }

        for score, (text, color) in scores.items():
            btn = ctk.CTkButton(scores_frame, text=text, fg_color=color, hover_color=self.darken_color(color),
                                command=lambda s=score: self.set_score(s))
            btn.pack(side="left", padx=7, pady=5, ipady=5)

    def set_score(self, score):
        self.result = score
        self.destroy()

    def darken_color(self, hex_color, factor=0.8):
        r = int(hex_color[1:3], 16)
        g = int(hex_color[3:5], 16)
        b = int(hex_color[5:7], 16)
        return f"#{int(r*factor):02x}{int(g*factor):02x}{int(b*factor):02x}"

    def create_buttons(self):
        """Sobrescribimos para no mostrar los botones Aceptar/Cancelar."""
        pass