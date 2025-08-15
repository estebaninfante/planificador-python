# dialogs.py (Versión Corregida y con Estilo)

import customtkinter as ctk
from tkinter import messagebox, ttk
from tkcalendar import DateEntry

class BaseDialog(ctk.CTkToplevel):
    # (El código de BaseDialog no cambia, lo incluyo para que el archivo esté completo)
    def __init__(self, parent, title=""):
        super().__init__(parent)
        self.title(title)
        self.result = None
        self.parent = parent
        self.initial_focus = None
        self.transient(parent)
        self.grab_set()
        self.protocol("WM_DELETE_WINDOW", self._cancel_event)
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(padx=20, pady=20, expand=True, fill="both")
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
        pass

    def create_buttons(self):
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
                                        style="Custom.TCombobox", # <-- Aplicar estilo
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
                                        style="Custom.TCombobox", # <-- Aplicar estilo
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
                                        style="Custom.TCombobox", # <-- Aplicar estilo
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