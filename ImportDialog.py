import customtkinter as ctk
from tkinter import filedialog
import json
import os

class ImportDialog(ctk.CTkToplevel):
    """Diálogo para importar elementos desde JSON."""
    
    def __init__(self, parent, data_manager):
        super().__init__(parent)
        self.title("Importar elementos")
        self.dm = data_manager
        
        # Configuración de la ventana
        self.geometry("600x400")
        self.resizable(False, False)
        
        self.setup_ui()
        
        # Hacer modal
        self.transient(parent)
        self.grab_set()
        self.protocol("WM_DELETE_WINDOW", self.cancel)

    def setup_ui(self):
        # Frame principal
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(padx=20, pady=20, fill="both", expand=True)

        # Texto informativo
        info_text = """
        Seleccione un archivo JSON para importar elementos.
        
        Formato esperado:
        {
            "tasks": [
                {
                    "title": "Tarea 1",
                    "due_date": "2025-10-01",
                    "status": "Pendiente"
                }
            ],
            "events": [
                {
                    "title": "Evento 1",
                    "description": "Descripción",
                    "due_date": "2025-10-01",
                    "time": "10:00"
                }
            ],
            "lessons": [
                {
                    "title": "Lección 1",
                    "notes": "Notas",
                    "due_date": "2025-10-01",
                    "subject": "Matemáticas"
                }
            ]
        }
        """
        info_label = ctk.CTkTextbox(main_frame, height=200)
        info_label.pack(pady=10, padx=10, fill="both", expand=True)
        info_label.insert("1.0", info_text)
        info_label.configure(state="disabled")

        # Frame para archivo seleccionado
        file_frame = ctk.CTkFrame(main_frame)
        file_frame.pack(fill="x", padx=10, pady=10)

        self.file_label = ctk.CTkLabel(file_frame, text="Ningún archivo seleccionado")
        self.file_label.pack(side="left", padx=5)

        select_button = ctk.CTkButton(
            file_frame,
            text="Seleccionar archivo",
            command=self.select_file
        )
        select_button.pack(side="right", padx=5)

        # Frame para resultado
        self.result_label = ctk.CTkLabel(
            main_frame,
            text="",
            text_color="grey"
        )
        self.result_label.pack(pady=10)

        # Frame para botones
        button_frame = ctk.CTkFrame(main_frame)
        button_frame.pack(pady=10, fill="x")

        self.import_button = ctk.CTkButton(
            button_frame,
            text="Importar",
            command=self.import_file,
            state="disabled"
        )
        self.import_button.pack(side="left", padx=10, expand=True)

        cancel_button = ctk.CTkButton(
            button_frame,
            text="Cancelar",
            command=self.cancel
        )
        cancel_button.pack(side="left", padx=10, expand=True)

    def select_file(self):
        file_path = filedialog.askopenfilename(
            title="Seleccionar archivo JSON",
            filetypes=[("Archivos JSON", "*.json")]
        )
        
        if file_path:
            self.file_path = file_path
            self.file_label.configure(text=os.path.basename(file_path))
            self.import_button.configure(state="normal")
            self.result_label.configure(text="")

    def import_file(self):
        success, message = self.dm.import_from_file(self.file_path)
        
        if success:
            self.result_label.configure(
                text=message,
                text_color="green"
            )
            self.after(2000, self.destroy)  # Cerrar después de 2 segundos
        else:
            self.result_label.configure(
                text=message,
                text_color="red"
            )

    def cancel(self):
        self.destroy()