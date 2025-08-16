# gui.py

import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
from DataManager import DataManager
# --- 1. IMPORTA EL DIÁLOGO DE CALIFICACIÓN ---
from dialogs import AddTaskDialog, AddEventDialog, AddLessonDialog, ReviewScoreDialog

class App(ctk.CTk):
    """
    Clase principal de la aplicación con customtkinter.
    """
    def __init__(self):
        super().__init__()
        self.title("Gestor de Tareas y Agenda")
        self.geometry("1100x700") # Aumentado para mejor visibilidad

        # Configurar tema de customtkinter
        ctk.set_appearance_mode("dark")  # Opciones: "dark", "light", "system"
        ctk.set_default_color_theme("blue")  # Opciones: "blue", "green", "dark-blue"
        
        self.dm = DataManager()
        
        self._setup_treeview_style()
        self.setup_ui()


    def _setup_treeview_style(self):
        """Aplica un estilo al ttk.Treeview y DateEntry para que coincida con el tema."""
        # --- Obtener colores del tema actual de customtkinter ---
        bg_color = self._apply_appearance_mode(ctk.ThemeManager.theme["CTkFrame"]["fg_color"])
        text_color = self._apply_appearance_mode(ctk.ThemeManager.theme["CTkLabel"]["text_color"])
        header_bg = self._apply_appearance_mode(ctk.ThemeManager.theme["CTkButton"]["fg_color"])
        entry_bg = self._apply_appearance_mode(ctk.ThemeManager.theme["CTkEntry"]["fg_color"])
        entry_border = self._apply_appearance_mode(ctk.ThemeManager.theme["CTkEntry"]["border_color"])
        
        # --- Estilo del Treeview ---
        style = ttk.Style()
        style.theme_use("default")
        
        # Estilo para el contenido de las filas
        style.configure("Treeview",
                        background=bg_color,
                        foreground=text_color,
                        fieldbackground=bg_color,
                        borderwidth=0,
                        rowheight=35,  # Aumenta la altura para el nuevo tamaño de fuente
                        font=("", 14)) # Fuente del contenido
                        
        style.map('Treeview', background=[('selected', ctk.ThemeManager.theme["CTkButton"]["fg_color"])])

        # Estilo para el encabezado
        style.configure("Treeview.Heading",
                        background=header_bg,
                        foreground=text_color,
                        relief="flat",
                        font=("", 16, "bold")) # Fuente del encabezado

        style.map("Treeview.Heading", background=[('active', ctk.ThemeManager.theme["CTkButton"]["hover_color"])])

        # --- Estilo para DateEntry ---
        style.configure("Custom.TCombobox",
                        selectbackground=entry_bg,
                        fieldbackground=entry_bg,
                        background=entry_bg,
                        foreground=text_color,
                        arrowcolor=text_color,
                        bordercolor=entry_border,
                        lightcolor=bg_color,
                        darkcolor=bg_color,
                        insertcolor=text_color,
                        padding=10)
        style.map("Custom.TCombobox",
                  fieldbackground=[("readonly", entry_bg)],
                  selectbackground=[("readonly", entry_bg)],
                  foreground=[("readonly", text_color)])


    def setup_ui(self):
        """Configura la interfaz de usuario principal con pestañas."""
        self.tab_view = ctk.CTkTabview(self, anchor="w")
        self.tab_view.pack(pady=10, padx=10, expand=True, fill="both")
        
        self.tab_view.add("Tareas")
        self.tab_view.add("Eventos")
        self.tab_view.add("Lecciones")
        
        self.create_task_tab(self.tab_view.tab("Tareas"))
        self.create_event_tab(self.tab_view.tab("Eventos"))
        self.create_lesson_tab(self.tab_view.tab("Lecciones"))
        
    def create_task_tab(self, tab):
        # --- (Sin cambios en esta sección) ---
        tree_frame = ctk.CTkFrame(tab)
        tree_frame.pack(fill="both", expand=True, padx=5, pady=5)
        tree_columns = ("titulo", "estado", "fecha_limite")
        self.tasks_tree = ttk.Treeview(tree_frame, columns=tree_columns, show="headings")
        self.tasks_tree.heading("titulo", text="Título")
        self.tasks_tree.heading("estado", text="Estado")
        self.tasks_tree.heading("fecha_limite", text="Fecha Límite")
        self.tasks_tree.column("titulo", width=300)
        self.tasks_tree.column("estado", anchor=tk.CENTER)
        self.tasks_tree.column("fecha_limite", anchor=tk.CENTER)
        self.tasks_tree.pack(fill="both", expand=True)
        button_frame = ctk.CTkFrame(tab, fg_color="transparent")
        button_frame.pack(pady=10, fill="x")
        add_button = ctk.CTkButton(button_frame, text="Agregar Tarea", command=self.add_task)
        add_button.pack(side="left", padx=10)
        delete_button = ctk.CTkButton(button_frame, text="Eliminar Tarea", command=self.delete_task, fg_color="#D32F2F", hover_color="#B71C1C")
        delete_button.pack(side="left", padx=10)
        self.populate_tasks_tree()

    def populate_tasks_tree(self):
        # --- (Sin cambios en esta sección) ---
        for item in self.tasks_tree.get_children():
            self.tasks_tree.delete(item)
        for task in self.dm.get_all_tasks():
            self.tasks_tree.insert("", "end", values=(task.title, task.status.value, task.due_date))

    def add_task(self):
        # --- (Sin cambios en esta sección) ---
        dialog = AddTaskDialog(self)
        result = dialog.get_input()
        if result:
            title, due_date = result
            self.dm.addTask(title, due_date)
            self.populate_tasks_tree()

    def delete_task(self):
        # --- (Sin cambios en esta sección) ---
        selected_item = self.tasks_tree.focus()
        if not selected_item:
            messagebox.showwarning("Selección inválida", "Por favor, seleccione una tarea para eliminar.")
            return
        if messagebox.askyesno("Confirmar", "¿Está seguro que desea eliminar la tarea seleccionada?"):
            item_index = self.tasks_tree.index(selected_item)
            if self.dm.deleteTask(item_index):
                self.populate_tasks_tree()
            else:
                messagebox.showerror("Error", "No se pudo eliminar la tarea.")

    def create_event_tab(self, tab):
        # --- (Sin cambios en esta sección) ---
        tree_frame = ctk.CTkFrame(tab)
        tree_frame.pack(fill="both", expand=True, padx=5, pady=5)
        tree_columns = ("titulo", "descripcion", "fecha", "hora")
        self.events_tree = ttk.Treeview(tree_frame, columns=tree_columns, show="headings")
        self.events_tree.heading("titulo", text="Título")
        self.events_tree.heading("descripcion", text="Descripción")
        self.events_tree.heading("fecha", text="Fecha")
        self.events_tree.heading("hora", text="Hora")
        self.events_tree.pack(fill="both", expand=True)
        button_frame = ctk.CTkFrame(tab, fg_color="transparent")
        button_frame.pack(pady=10, fill="x")
        add_button = ctk.CTkButton(button_frame, text="Agregar Evento", command=self.add_event)
        add_button.pack(side="left", padx=10)
        delete_button = ctk.CTkButton(button_frame, text="Eliminar Evento", command=self.delete_event, fg_color="#D32F2F", hover_color="#B71C1C")
        delete_button.pack(side="left", padx=10)
        self.populate_events_tree()

    def populate_events_tree(self):
        # --- (Sin cambios en esta sección) ---
        for item in self.events_tree.get_children():
            self.events_tree.delete(item)
        for event in self.dm.get_all_events():
            self.events_tree.insert("", "end", values=(event.title, event.description, event.due_date, event.time))

    def add_event(self):
        # --- (Sin cambios en esta sección) ---
        dialog = AddEventDialog(self)
        result = dialog.get_input()
        if result:
            self.dm.addEvent(*result)
            self.populate_events_tree()

    def delete_event(self):
        # --- (Sin cambios en esta sección) ---
        selected_item = self.events_tree.focus()
        if not selected_item:
            messagebox.showwarning("Selección inválida", "Por favor, seleccione un evento para eliminar.")
            return
        if messagebox.askyesno("Confirmar", "¿Está seguro que desea eliminar el evento seleccionado?"):
            item_index = self.events_tree.index(selected_item)
            if self.dm.deleteEvent(item_index):
                self.populate_events_tree()

    def create_lesson_tab(self, tab):
        """Crea y configura la pestaña de Lecciones."""
        tree_frame = ctk.CTkFrame(tab)
        tree_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # --- 1. DEFINE LAS COLUMNAS, INCLUYENDO REPETICIONES Y EFACTOR ---
        tree_columns = ("titulo", "asignatura", "fecha", "proximo_repaso", "repeticiones", "efactor")
        self.lessons_tree = ttk.Treeview(tree_frame, columns=tree_columns, show="headings")
        
        # --- Configuración de Encabezados ---
        self.lessons_tree.heading("titulo", text="Título")
        self.lessons_tree.heading("asignatura", text="Asignatura")
        self.lessons_tree.heading("fecha", text="Fecha Creación")
        self.lessons_tree.heading("proximo_repaso", text="Próximo Repaso")
        self.lessons_tree.heading("repeticiones", text="Repeticiones")
        self.lessons_tree.heading("efactor", text="Factor Facilidad")
        
        # --- Configuración del ancho y alineación de las columnas ---
        self.lessons_tree.column("titulo", width=250)
        self.lessons_tree.column("asignatura", width=150)
        self.lessons_tree.column("fecha", anchor=tk.CENTER, width=120)
        self.lessons_tree.column("proximo_repaso", anchor=tk.CENTER, width=120)
        self.lessons_tree.column("repeticiones", anchor=tk.CENTER, width=100)
        self.lessons_tree.column("efactor", anchor=tk.CENTER, width=120)
        
        self.lessons_tree.pack(fill="both", expand=True)

        # --- Frame para los botones ---
        button_frame = ctk.CTkFrame(tab, fg_color="transparent")
        button_frame.pack(pady=10, fill="x")
        
        add_button = ctk.CTkButton(button_frame, text="Agregar Lección", command=self.add_lesson)
        add_button.pack(side="left", padx=10)
        
        review_button = ctk.CTkButton(button_frame, text="Repasar Lección", command=self.review_lesson, fg_color="#00796B", hover_color="#004D40")
        review_button.pack(side="left", padx=10)
        
        delete_button = ctk.CTkButton(button_frame, text="Eliminar Lección", command=self.delete_lesson, fg_color="#D32F2F", hover_color="#B71C1C")
        delete_button.pack(side="left", padx=10)
        
        self.populate_lessons_tree()

    def populate_lessons_tree(self):
        """Limpia y rellena la tabla de lecciones con datos actualizados."""
        # Limpiar la tabla antes de rellenarla
        for item in self.lessons_tree.get_children():
            self.lessons_tree.delete(item)
            
        # --- 2. MUESTRA LOS NUEVOS DATOS: REPETICIONES Y EFACTOR ---
        for lesson in self.dm.get_all_lessons():
            # Formateamos el efactor para mostrar solo 2 decimales
            formatted_efactor = f"{lesson.efactor:.2f}"
            
            # Insertamos la fila con todos los datos
            self.lessons_tree.insert("", "end", values=(
                lesson.title, 
                lesson.subject, 
                lesson.due_date, 
                lesson.next_review_date,
                lesson.repetitions,
                formatted_efactor
            ))

    def add_lesson(self):
        """Abre un diálogo para agregar una nueva lección."""
        dialog = AddLessonDialog(self)
        result = dialog.get_input()
        if result:
            self.dm.addLesson(*result)
            self.populate_lessons_tree()

    def delete_lesson(self):
        """Elimina la lección seleccionada de la tabla."""
        selected_item = self.lessons_tree.focus()
        if not selected_item:
            messagebox.showwarning("Selección inválida", "Por favor, seleccione una lección para eliminar.")
            return
            
        if messagebox.askyesno("Confirmar", "¿Está seguro que desea eliminar la lección seleccionada?"):
            item_index = self.lessons_tree.index(selected_item)
            if self.dm.deleteLesson(item_index):
                self.populate_lessons_tree()

    def review_lesson(self):
        """Abre un diálogo para calificar y luego actualiza la lección."""
        selected_item = self.lessons_tree.focus()
        if not selected_item:
            messagebox.showwarning("Selección inválida", "Por favor, seleccione una lección para repasar.")
            return

        # Abre el diálogo para obtener la calificación del repaso
        dialog = ReviewScoreDialog(self)
        score = dialog.get_input()

        # Si el usuario proporcionó una calificación
        if score is not None: # Se comprueba con 'is not None' por si el score fuera 0
            item_index = self.lessons_tree.index(selected_item)
            
            # Llama al DataManager para que aplique el algoritmo SM-2
            if self.dm.reviewLesson(score, item_index):
                self.populate_lessons_tree() # Refresca la tabla con los nuevos datos
                messagebox.showinfo("¡Éxito!", "Se ha programado el próximo repaso.")
            else:
                messagebox.showerror("Error", "No se pudo actualizar la lección.")