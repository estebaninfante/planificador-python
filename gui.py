# gui.py

import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
from DataManager import DataManager
from dialogs import AddTaskDialog, AddEventDialog, AddLessonDialog, ReviewScoreDialog
from TimeRangeDialog import TimeRangeDialog
from ImportDialog import ImportDialog
from PreferencesDialog import PreferencesDialog

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
        
        # Obtener tamaño de fuente de las preferencias
        font_size = getattr(self.dm.user_preferences, 'font_size', 14)
        
        # Estilo para el contenido de las filas
        style.configure("Treeview",
                        background=bg_color,
                        foreground=text_color,
                        fieldbackground=bg_color,
                        borderwidth=0,
                        rowheight=max(35, font_size + 10),  # Altura ajustada al tamaño de fuente
                        font=("", font_size)) # Fuente del contenido
                        
        style.map('Treeview', background=[('selected', ctk.ThemeManager.theme["CTkButton"]["fg_color"])])

        # Estilo para el encabezado
        style.configure("Treeview.Heading",
                        background=header_bg,
                        foreground=text_color,
                        relief="flat",
                        font=("", font_size + 2, "bold")) # Fuente del encabezado

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
        # Frame principal para la barra superior (Importar y Preferencias juntos)
        top_frame = ctk.CTkFrame(self)
        top_frame.pack(fill="x", padx=10, pady=5)

        # Botón de preferencias (a la derecha del de importar)
        preferences_button = ctk.CTkButton(
            top_frame,
            text="Preferencias",
            command=self.show_preferences_dialog,
            width=120
        )
        preferences_button.pack(side="right")

        # Botón de importación
        import_button = ctk.CTkButton(
            top_frame,
            text="Importar desde JSON",
            command=self.show_import_dialog,
            width=150
        )
        import_button.pack(side="right", padx=5)

        # Pestañas
        self.tab_view = ctk.CTkTabview(self, anchor="w")
        self.tab_view.pack(pady=(5,10), padx=10, expand=True, fill="both")
        
        # Añadir todas las pestañas
        self.tab_view.add("Planificador")  # Renombrado
        self.tab_view.add("Tareas")
        self.tab_view.add("Eventos")
        self.tab_view.add("Lecciones")
        
        # Crear todas las pestañas
        self.create_your_day_tab(self.tab_view.tab("Planificador"))
        self.create_task_tab(self.tab_view.tab("Tareas"))
        self.create_event_tab(self.tab_view.tab("Eventos"))
        self.create_lesson_tab(self.tab_view.tab("Lecciones"))
        
        # Establecer "Tu Día" como pestaña por defecto
        self.tab_view.set("Planificador")
        
    def create_your_day_tab(self, tab):
        """Crea la pestaña 'Tu Día' con tabla como las demás."""
        # Frame para la tabla
        tree_frame = ctk.CTkFrame(tab)
        tree_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Definir columnas para la tabla
        tree_columns = ("tipo", "titulo", "detalles", "horario", "prioridad")
        self.your_day_tree = ttk.Treeview(tree_frame, columns=tree_columns, show="headings")
        
        # Configurar encabezados
        self.your_day_tree.heading("tipo", text="Tipo")
        self.your_day_tree.heading("titulo", text="Título")
        self.your_day_tree.heading("detalles", text="Detalles")
        self.your_day_tree.heading("horario", text="Horario")
        self.your_day_tree.heading("prioridad", text="Prioridad")
        
        # Configurar anchos de columnas
        self.your_day_tree.column("tipo", width=80, anchor=tk.CENTER)
        self.your_day_tree.column("titulo", width=250)
        self.your_day_tree.column("detalles", width=200)
        self.your_day_tree.column("horario", width=120, anchor=tk.CENTER)
        self.your_day_tree.column("prioridad", width=120, anchor=tk.CENTER)
        
        self.your_day_tree.pack(fill="both", expand=True)

        # Diferenciar encabezados de sección con tags (para que no parezcan filas normales)
        # Estética de Tu Día
        self.your_day_tree.tag_configure(
            "section_header",
            background="#0f172a",  # azul gris oscuro
            foreground="#e2e8f0",
            font=("", getattr(self.dm.user_preferences, 'font_size', 14) + 3, "bold")
        )
        self.your_day_tree.tag_configure("section_item", background="", foreground="#e0e0e0")
        
        # Frame para botones
        button_frame = ctk.CTkFrame(tab, fg_color="transparent")
        button_frame.pack(pady=10, fill="x")
        
        # Botón para actualizar
        refresh_button = ctk.CTkButton(
            button_frame, 
            text="Actualizar", 
            command=self.refresh_your_day_tab,
            width=100
        )
        refresh_button.pack(side="left", padx=10)
        
        # Poblar el contenido inicial
        self.populate_your_day_tree()
        
        # Evitar que se puedan seleccionar los encabezados (para que se perciban como títulos, no filas)
        def on_select(event):
            selected = self.your_day_tree.selection()
            for iid in selected:
                if "section_header" in self.your_day_tree.item(iid, "tags"):
                    self.your_day_tree.selection_remove(iid)
        self.your_day_tree.bind("<<TreeviewSelect>>", on_select)
        
    def populate_your_day_tree(self):
        """Pobla la tabla de 'Tu Día' con todos los elementos organizados."""
        # Limpiar la tabla
        for item in self.your_day_tree.get_children():
            self.your_day_tree.delete(item)
        
        # Obtener plan exclusivo para HOY
        today_items = self.dm.get_today_plan()
        
        # Diccionario para títulos más atractivos y colores
        period_styles = {
            "Para Hoy (Urgente)": {"icon": "🔥", "color": "#FF4444"},
            "Mañana": {"icon": "🌅", "color": "#FF8800"},
            "Próximos 7 días": {"icon": "📅", "color": "#4488FF"},
            "Más adelante": {"icon": "⏰", "color": "#888888"}
        }
        
        # Título general del día
        header = self.your_day_tree.insert("", "end", values=(
            "🗓️", "  Tu día planificado", f"({len(today_items)} elementos)", "", ""
        ), tags=("section_header",))
        self.your_day_tree.set(header, "tipo", "🗓️")
        self.your_day_tree.set(header, "titulo", "  TU DÍA PLANIFICADO")
        self.your_day_tree.set(header, "detalles", f"({len(today_items)} elementos)")

        for item in today_items:
                    # Preparar detalles según el tipo
                    details = ""
                    if item.get_type() == "Tarea":
                        details = f"Estado: {item.status.value}"
                    elif item.get_type() == "Evento":
                        details = f"Hora: {item.time}"
                    elif item.get_type() == "Lección":
                        details = f"Materia: {item.subject}"
                    
                    # Preparar horario
                    horario = ""
                    if item.start_time and item.end_time:
                        horario = f"{item.start_time.strftime('%H:%M')}-{item.end_time.strftime('%H:%M')}"
                    
                    # Insertar fila en la tabla
                    self.your_day_tree.insert("", "end", values=(
                        f"  {item.get_type()}",  # Tipo con indentación
                        f"    {item.title}",     # Título con indentación
                        details,
                        horario,
                        item.get_priority_text()
                    ), tags=("section_item",))

    def create_task_tab(self, tab):
        # --- (Sin cambios en esta sección) ---
        tree_frame = ctk.CTkFrame(tab)
        tree_frame.pack(fill="both", expand=True, padx=5, pady=5)
        tree_columns = ("titulo", "estado", "fecha_limite", "prioridad")
        self.tasks_tree = ttk.Treeview(tree_frame, columns=tree_columns, show="headings")
        self.tasks_tree.heading("titulo", text="Título")
        self.tasks_tree.heading("estado", text="Estado")
        self.tasks_tree.heading("fecha_limite", text="Fecha Límite")
        self.tasks_tree.heading("prioridad", text="Prioridad / Días Restantes")
        self.tasks_tree.column("titulo", width=300)
        self.tasks_tree.column("estado", anchor=tk.CENTER)
        self.tasks_tree.column("fecha_limite", anchor=tk.CENTER)
        self.tasks_tree.column("prioridad", anchor=tk.CENTER, width=150)
        self.tasks_tree.pack(fill="both", expand=True)
        button_frame = ctk.CTkFrame(tab, fg_color="transparent")
        button_frame.pack(pady=10, fill="x")
        
        # Botón para añadir tarea
        add_button = ctk.CTkButton(button_frame, text="Agregar Tarea", command=self.add_task)
        add_button.pack(side="left", padx=10)
        # Marcar tarea como completada
        complete_button = ctk.CTkButton(button_frame, text="Marcar Completada", command=self.complete_task, fg_color="#2E7D32", hover_color="#1B5E20")
        complete_button.pack(side="left", padx=10)
        
        # Botón para importar
        import_button = ctk.CTkButton(button_frame, text="Importar", command=self.show_import_dialog, fg_color="#2196F3", hover_color="#1976D2")
        import_button.pack(side="left", padx=10)
        
        # Botón para eliminar tarea
        delete_button = ctk.CTkButton(button_frame, text="Eliminar Tarea", command=self.delete_task, fg_color="#D32F2F", hover_color="#B71C1C")
        delete_button.pack(side="left", padx=10)
        
        self.populate_tasks_tree()

    def edit_time_range(self, item):
        """Abre el diálogo para editar el rango de hora de un item."""
        dialog = TimeRangeDialog(
            self,
            title=f"Editar horario - {item.title}",
            current_start=item.start_time,
            current_end=item.end_time,
            current_duration=item.duration
        )
        result = dialog.get_result()
        
        if result:
            start_time, end_time, duration = result
            item.set_duration(duration)
            item.set_time_range(start_time, end_time)
            self.dm.saveData()  # Guardar cambios
            self.refresh_your_day_tab()  # Actualizar la vista

    def show_import_dialog(self):
        """Muestra el diálogo de importación."""
        dialog = ImportDialog(self, self.dm)
        self.wait_window(dialog)
        # Actualizar todas las vistas después de la importación
        self.refresh_all_views()

    def refresh_your_day_tab(self):
        """Actualiza la pestaña 'Tu Día'."""
        if hasattr(self, 'your_day_tree'):
            # Simplemente repoblar la tabla
            self.populate_your_day_tree()
        else:
            # Si no existe la tabla, recrear la pestaña
            tab = self.tab_view.tab("Planificador")
            self.create_your_day_tab(tab)

    def show_preferences_dialog(self):
        """Muestra el diálogo de preferencias del usuario"""
        dialog = PreferencesDialog(self, self.dm.user_preferences)
        self.wait_window(dialog)
        # Actualizar las preferencias en el DataManager
        self.dm.user_preferences = dialog.get_preferences()
        self.dm.savePreferences()
        # Actualizar los tamaños de fuente y las vistas
        self.update_font_sizes()

    def refresh_all_views(self):
        """Actualiza todas las vistas después de una importación."""
        self.refresh_your_day_tab()
        self.populate_tasks_tree()
        self.populate_events_tree()
        self.populate_lessons_tree()
    
    def update_font_sizes(self):
        """Actualiza los tamaños de fuente en toda la aplicación."""
        # Reconfigurar estilos de Treeview
        self._setup_treeview_style()
        
        # Actualizar todas las vistas para aplicar los nuevos estilos
        self.refresh_all_views()

    def populate_tasks_tree(self):
        """Actualiza la vista de tareas con priorización."""
        for item in self.tasks_tree.get_children():
            self.tasks_tree.delete(item)
        for task in self.dm.get_all_tasks():
            priority_text = task.get_priority_text()
            self.tasks_tree.insert("", "end", values=(
                task.title,
                task.status.value,
                task.due_date,
                priority_text
            ))

    def add_task(self):
        # --- (Sin cambios en esta sección) ---
        dialog = AddTaskDialog(self)
        result = dialog.get_input()
        if result:
            title, due_date, est = result
            self.dm.addTask(title, due_date, estimated_minutes=est)
            self.populate_tasks_tree()
            self.refresh_your_day_tab()

    def complete_task(self):
        selected_item = self.tasks_tree.focus()
        if not selected_item:
            messagebox.showwarning("Selección inválida", "Seleccione una tarea para completar.")
            return
        item_index = self.tasks_tree.index(selected_item)
        if self.dm.mark_task_completed(item_index):
            self.populate_tasks_tree()
            self.refresh_your_day_tab()

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
                self.refresh_your_day_tab()
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
        # Marcar lección como completada
        complete_lesson_button = ctk.CTkButton(button_frame, text="Marcar Completada", command=self.complete_lesson, fg_color="#2E7D32", hover_color="#1B5E20")
        complete_lesson_button.pack(side="left", padx=10)
        
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
            title, notes, due_date, subject, est, notes_file = result
            self.dm.addLesson(title, notes, due_date, subject, estimated_minutes=est, notes_file=notes_file)
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

    def complete_lesson(self):
        selected_item = self.lessons_tree.focus()
        if not selected_item:
            messagebox.showwarning("Selección inválida", "Seleccione una lección para completar.")
            return
        item_index = self.lessons_tree.index(selected_item)
        if self.dm.mark_lesson_completed(item_index):
            self.populate_lessons_tree()
            self.refresh_your_day_tab()