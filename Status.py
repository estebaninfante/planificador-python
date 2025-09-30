from enum import Enum

class Status(Enum):
    PENDIENTE = "Pendiente"
    EN_PROGRESO = "En progreso"
    SIN_COMENZAR = "Sin comenzar"
    COMPLETADO = "Completado"