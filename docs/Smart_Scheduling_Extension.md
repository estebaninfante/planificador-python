# Extensión del Min-Heap: Planificación Inteligente

## 1. Mejoras al Sistema Base

### Nuevos Atributos para Eventos
```python
class Event(PrioritizedItem):
    def __init__(self, title, date, time, description=""):
        super().__init__()
        self.title = title
        self.event_date = date
        self.event_time = time
        self.description = description
        self.is_fixed = False  # Nuevo: indica si el evento tiene horario fijo
```

### Clase de Preferencias de Usuario
```python
class UserPreferences:
    def __init__(self):
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

        # Días no laborables
        self.non_working_days = []  # Lista de días de la semana (0-6)
```

## 2. Interfaz de Configuración

### Nueva Pestaña de Preferencias
```python
def create_preferences_tab(self, tab):
    """Crea la pestaña de preferencias del usuario"""
    
    # Frame principal con scroll
    main_frame = ctk.CTkScrollableFrame(tab)
    main_frame.pack(fill="both", expand=True, padx=10, pady=10)
    
    # 1. Horarios de Trabajo
    self._create_work_hours_section(main_frame)
    
    # 2. Bloques de Tiempo Preferidos
    self._create_time_blocks_section(main_frame)
    
    # 3. Configuración de Pausas
    self._create_breaks_section(main_frame)
    
    # 4. Horarios de Comidas
    self._create_meal_times_section(main_frame)
    
    # 5. Preferencias de Productividad
    self._create_productivity_section(main_frame)
    
    # 6. Días No Laborables
    self._create_non_working_days_section(main_frame)
    
    # Botón de Guardar
    save_button = ctk.CTkButton(
        main_frame,
        text="Guardar Preferencias",
        command=self._save_preferences
    )
    save_button.pack(pady=20)
```

## 3. Algoritmo de Planificación Inteligente

### Proceso de Asignación de Horarios

1. **Recopilación de Eventos Fijos**:
```python
def get_fixed_events(self):
    """Obtiene todos los eventos con horario fijo"""
    return [event for event in self.events if event.is_fixed]
```

2. **Identificación de Bloques Disponibles**:
```python
def get_available_blocks(self, date, fixed_events):
    """
    Calcula los bloques de tiempo disponibles en un día,
    considerando eventos fijos y preferencias del usuario
    """
    # Iniciar con bloques de trabajo del usuario
    blocks = self._init_work_blocks(date)
    
    # Remover bloques de tiempo no disponibles
    blocks = self._remove_fixed_events(blocks, fixed_events)
    blocks = self._remove_break_times(blocks)
    blocks = self._remove_meal_times(blocks)
    
    return blocks
```

3. **Asignación de Horarios**:
```python
def assign_time_slots(self, items, date):
    """
    Asigna horarios a los elementos priorizados
    considerando preferencias y restricciones
    """
    # 1. Obtener bloques disponibles
    available_blocks = self.get_available_blocks(date)
    
    # 2. Ordenar items por prioridad (ya hecho por el Min-Heap)
    
    # 3. Asignar horarios según preferencias
    for item in items:
        if not item.is_fixed:  # Solo para items sin horario fijo
            best_block = self._find_best_time_block(item, available_blocks)
            if best_block:
                self._assign_time_to_item(item, best_block)
                self._update_available_blocks(available_blocks, best_block)
```

### Criterios de Asignación

1. **Prioridad Temporal** (del Min-Heap base)
   - Fecha límite
   - Tipo de elemento
   - Urgencia

2. **Preferencias de Usuario**
   - Horarios de alta productividad
   - Bloques de tiempo preferidos
   - Patrones de trabajo

3. **Restricciones**
   - Eventos fijos
   - Horarios de comida
   - Pausas programadas

## 4. Integración con el Sistema Existente

### Modificaciones al DataManager

```python
class DataManager:
    def __init__(self):
        # ... código existente ...
        self.user_preferences = UserPreferences()
    
    def schedule_day(self, date):
        """Planifica un día completo"""
        # 1. Obtener elementos del día
        items = self.get_items_by_day()[date]
        
        # 2. Separar eventos fijos
        fixed_events = [i for i in items if 
                       isinstance(i, Event) and i.is_fixed]
        
        # 3. Obtener bloques disponibles
        available_blocks = self.get_available_blocks(date, fixed_events)
        
        # 4. Asignar horarios al resto de elementos
        non_fixed_items = [i for i in items if not (
            isinstance(i, Event) and i.is_fixed)]
        
        self.assign_time_slots(non_fixed_items, available_blocks)
```

## 5. Ejemplo de Uso

```python
# 1. Usuario configura sus preferencias
dm.user_preferences.work_hours = {'start': '09:00', 'end': '17:00'}
dm.user_preferences.meal_times['lunch'] = {'time': '13:00', 'duration': 60}

# 2. Crear eventos (algunos fijos, otros flexibles)
evento_fijo = Event("Reunión importante", "2025-10-01", "10:00")
evento_fijo.is_fixed = True
dm.addEvent(evento_fijo)

tarea_flexible = Task("Preparar presentación", "2025-10-01")
dm.addTask(tarea_flexible)

# 3. El sistema asigna automáticamente horarios
dm.schedule_day("2025-10-01")
```

### Resultado
```
09:00 - 10:00: Preparar presentación
10:00 - 11:00: Reunión importante (fijo)
11:15 - 12:30: Continuar presentación
13:00 - 14:00: Almuerzo
14:00 - 15:30: Otras tareas
```

El sistema respeta:
- Eventos fijos
- Horarios de comida
- Pausas necesarias
- Preferencias de productividad