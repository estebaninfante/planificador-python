import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from enum import Enum

# --- Clase Enum para el estado de las tareas ---
class Status(Enum):
    PENDIENTE = "Pendiente"
    EN_PROGRESO = "En Progreso"
    COMPLETADA = "Completada"

# --- Clases de modelos de datos ---
class Task:
    def __init__(self, title, status: Status, due_date):
        self.title = title
        self.status = status
        self.due_date = due_date

    def __str__(self):
        return f"Tarea: {self.title} | Estado: {self.status.value} | Fecha Límite: {self.due_date}"

    def to_dict(self):
        return {'title': self.title, 'status': self.status.value, 'due_date': self.due_date}

    @staticmethod
    def from_dict(data):
        # Asegurarse de que el estado del JSON es válido para la Enum
        try:
            status = Status(data['status'])
        except ValueError:
            status = Status.PENDIENTE # Usar un valor predeterminado si es inválido
        return Task(data['title'], status, data['due_date'])
    
class Event:
    def __init__(self, title, description, due_date, time):
        self.title = title
        self.description = description
        self.due_date = due_date
        self.time = time

    def __str__(self):
        return f"Evento: {self.title} | Descripción: {self.description} | Fecha: {self.due_date} | Hora: {self.time}"

    def to_dict(self):
        return {'title': self.title, 'description': self.description, 'due_date': self.due_date, 'time': self.time}

    @staticmethod
    def from_dict(data):
        return Event(data['title'], data['description'], data['due_date'], data['time'])

class Lesson:
    def __init__(self, title, notes, due_date, subject):
        self.title = title
        self.notes = notes
        self.subject = subject
        self.due_date = due_date

    def __str__(self):
        return f"Clase: {self.title} | Materia: {self.subject} | Fecha: {self.due_date}"

    def to_dict(self):
        return {'title': self.title, 'notes': self.notes, 'due_date': self.due_date, 'subject': self.subject}
    
    @staticmethod
    def from_dict(data):
        missing = [k for k in ('title', 'notes', 'due_date', 'subject') if k not in data]
        if missing:
            raise KeyError(f"Faltan claves requeridas en data: {missing}")
        return Lesson(
            title=data['title'],
            notes=data['notes'],
            due_date=data['due_date'],
            subject=data['subject']
        )

# --- Gestor de Datos ---
path_file = "base_local.json"
class DataManager:
    def __init__(self, file_path=path_file):
        self.file_path = file_path
        self.data = self.loadData()

    def loadData(self):
        if not os.path.exists(self.file_path):
            return {"tasks": [], "events": [], "lessons": []}
        
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                raw_data = json.load(f)
                return {
                    "tasks": [Task.from_dict(d) for d in raw_data.get('tasks', [])],
                    "events": [Event.from_dict(d) for d in raw_data.get('events', [])],
                    "lessons": [Lesson.from_dict(d) for d in raw_data.get('lessons', [])]
                }
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error al cargar el archivo JSON: {e}. Se creará un archivo nuevo.")
            return {"tasks": [], "events": [], "lessons": []}

    def saveData(self):
        try:
            with open(self.file_path, "w", encoding="utf-8") as f:
                serializable_data = {
                    "tasks": [t.to_dict() for t in self.data["tasks"]],
                    "events": [e.to_dict() for e in self.data["events"]],
                    "lessons": [l.to_dict() for l in self.data["lessons"]]
                }
                json.dump(serializable_data, f, indent=4, ensure_ascii=False)
        except IOError as e:
            print(f"Error al guardar los datos: {e}")

    def addTask(self, title, status, due_date):
        new_task = Task(title, status, due_date)
        self.data["tasks"].append(new_task)
        self.saveData()

    def deleteTask(self, index):
        if 0 <= index < len(self.data['tasks']):
            del self.data['tasks'][index]
            self.saveData()
            print("Tarea eliminada exitosamente.")
        else:
            print("Índice de tarea no válido.")

    # ... (Aquí irían los métodos addEvent, showEvents, etc., no mostrados para simplificar)

# --- Clases de la Interfaz Gráfica ---
class MainApp(tk.Tk):
    def __init__(self, data_manager):
        super().__init__()
        self.title("Mi Agenda Personal")
        self.geometry("600x400")
        self.data_manager = data_manager

        self.container = ttk.Frame(self)
        self.container.pack(fill="both", expand=True)

        self.frames = {}
        self.frames["MainMenu"] = MainMenu(self.container, self)
        self.frames["TasksMenu"] = TasksMenu(self.container, self)
        
        self.frames["MainMenu"].grid(row=0, column=0, sticky="nsew")
        self.frames["TasksMenu"].grid(row=0, column=0, sticky="nsew")

        self.show_frame("MainMenu")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

class MainMenu(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, padding="20")
        self.controller = controller
        
        ttk.Label(self, text="Menú Principal", font=("Helvetica", 16, "bold")).pack(pady=20)
        
        task_button = ttk.Button(self, text="Gestionar Tareas", command=lambda: controller.show_frame("TasksMenu"))
        task_button.pack(fill="x", pady=5)
        
        events_button = ttk.Button(self, text="Gestionar Eventos", command=lambda: messagebox.showinfo("Información", "Menú de Eventos no implementado."))
        events_button.pack(fill="x", pady=5)
        
        lessons_button = ttk.Button(self, text="Gestionar Clases", command=lambda: messagebox.showinfo("Información", "Menú de Clases no implementado."))
        lessons_button.pack(fill="x", pady=5)

        exit_button = ttk.Button(self, text="Salir", command=controller.destroy)
        exit_button.pack(fill="x", pady=10)

class TasksMenu(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, padding="15")
        self.controller = controller
        
        ttk.Label(self, text="Menú de Tareas", font=("Helvetica", 16, "bold")).pack(pady=10)
        
        # --- Formulario para crear tareas ---
        form_frame = ttk.LabelFrame(self, text="Crear Nueva Tarea", padding="10")
        form_frame.pack(pady=10, fill="x")

        # Configurar grid para el formulario
        form_frame.columnconfigure(1, weight=1)

        ttk.Label(form_frame, text="Título:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.title_entry = ttk.Entry(form_frame)
        self.title_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=5)

        ttk.Label(form_frame, text="Estado:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.status_combobox = ttk.Combobox(form_frame, values=[s.value for s in Status], state="readonly")
        self.status_combobox.grid(row=1, column=1, sticky="ew", padx=5, pady=5)
        self.status_combobox.set(Status.PENDIENTE.value)

        ttk.Label(form_frame, text="Fecha Límite:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.due_date_entry = ttk.Entry(form_frame)
        self.due_date_entry.grid(row=2, column=1, sticky="ew", padx=5, pady=5)

        create_button = ttk.Button(form_frame, text="Crear Tarea", command=self.create_task)
        create_button.grid(row=3, column=1, pady=10, sticky="e")
        
        # --- Visualizador de tareas ---
        display_frame = ttk.LabelFrame(self, text="Tareas Pendientes", padding="10")
        display_frame.pack(pady=10, fill="both", expand=True)

        self.task_listbox = tk.Listbox(display_frame, height=10, font=("Consolas", 10), bd=0)
        self.task_listbox.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(display_frame, orient="vertical", command=self.task_listbox.yview)
        scrollbar.pack(side="right", fill="y")
        self.task_listbox.config(yscrollcommand=scrollbar.set)
        
        self.refresh_task_list()

        # --- Botones de acción ---
        button_frame = ttk.Frame(self)
        button_frame.pack(pady=10)
        
        delete_button = ttk.Button(button_frame, text="Eliminar Tarea", command=self.delete_task)
        delete_button.pack(side="left", padx=10)
        
        back_button = ttk.Button(button_frame, text="Volver", command=lambda: controller.show_frame("MainMenu"))
        back_button.pack(side="left", padx=10)

    def create_task(self):
        title = self.title_entry.get().strip()
        status_value = self.status_combobox.get()
        due_date = self.due_date_entry.get().strip()

        if not title or not due_date:
            messagebox.showwarning("Entrada Incompleta", "El título y la fecha límite son obligatorios.")
            return

        status = Status(status_value)
        self.controller.data_manager.addTask(title, status, due_date)
        messagebox.showinfo("Éxito", "Tarea agregada.")
        self.refresh_task_list()
        self.clear_entries()

    def delete_task(self):
        try:
            index = self.task_listbox.curselection()[0]
            self.controller.data_manager.deleteTask(index)
            self.refresh_task_list()
            messagebox.showinfo("Éxito", "Tarea eliminada.")
        except IndexError:
            messagebox.showwarning("Selección inválida", "Por favor, selecciona una tarea para eliminar.")

    def refresh_task_list(self):
        self.task_listbox.delete(0, tk.END)
        for i, task in enumerate(self.controller.data_manager.data['tasks']):
            self.task_listbox.insert(tk.END, f"{i+1}. {task}")
            
    def clear_entries(self):
        self.title_entry.delete(0, tk.END)
        self.due_date_entry.delete(0, tk.END)
        self.status_combobox.set(Status.PENDIENTE.value)

if __name__ == "__main__":
    dm = DataManager()
    app = MainApp(dm)
    app.mainloop()
