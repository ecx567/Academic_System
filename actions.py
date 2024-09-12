from datetime import date

class Asignatura:
    """Representa una asignatura o materia dentro de un nivel educativo."""

    def __init__(self, id, descripcion, nivel, active):
        self._id = id
        self._descripcion = descripcion
        self._nivel = nivel
        self._fecha_creacion = date.today()
        self._active = active

    @property
    def id(self):
        """Obtiene el identificador único de la asignatura."""
        return self._id

    @property
    def descripcion(self):
        """Obtiene la descripción de la asignatura."""
        return self._descripcion

    @property
    def nivel(self):
        """Obtiene el nivel educativo al que pertenece la asignatura."""
        return self._nivel
    
    @property
    def fecha_creacion(self):
        """Obtiene la fecha de creación del registro de la asignatura."""
        return self._fecha_creacion
    
    @property
    def active(self):
        """Obtiene el estado de actividad de la asignatura."""
        return self._active
    
    def activar(self):
        """Activa el nivel."""
        self._active = True

    def desactivar(self):
        """Desactiva el nivel."""
        self._active = False

##################################################################

class Estudiante:
    """Representa a un estudiante en el sistema académico."""

    def __init__(self, cedula, nombre, apellido, fecha_nacimiento, active=True):
        self._cedula = cedula
        self._nombre = nombre
        self._apellido = apellido
        self._fecha_nacimiento = fecha_nacimiento
        self._fecha_creacion = date.today()
        self._active = active

    @property
    def id(self):
        """Obtiene el identificador único del estudiante."""
        return self._id

    @property
    def nombre(self):
        """Obtendra el nombre del estudiante."""
        return self._nombre

    @property
    def apellido(self):
        """Obtendra el apellido del estudiante."""
        return self._apellido

    @property
    def fecha_nacimiento(self):
        """Obtendra la fecha de nacimiento del estudiante."""
        return self._fecha_nacimiento
    
    @property
    def fecha_creacion(self):
        """Obtendra la fecha de creación del registro del estudiante."""
        return self._fecha_creacion

    @property
    def active(self):
        """Obtendra el estado de actividad del estudiante."""
        return self._active
    
############################################################################

class Nivel:
    """Representa un nivel educativo en el sistema académico."""

    def __init__(self, id, nivel):
        self._id = id
        self._nivel = nivel
        self._fecha_creacion = date.today().strftime('%Y-%m-%d')
        self._active = True

    @property
    def id(self):
        """Obtendra el identificador único del nivel."""
        return self._id

    @property
    def nivel(self):
        """Obtendra el nombre o descripción del nivel."""
        return self._nivel
    
    @property
    def fecha_creacion(self):
        """Obtendra la fecha de creación del nivel."""
        return self._fecha_creacion

    @property
    def active(self):
        """Obtendra el estado de actividad del nivel."""
        return self._active

    def activar(self):
        """Activa el nivel."""
        self._active = True

    def desactivar(self):
        """Desactiva el nivel."""
        self._active = False

#############################################################################

class Periodo:
    """Representa un período académico en el sistema."""

    def __init__(self, id, periodo, active):
        if not periodo:
            raise ValueError("El nombre del período no puede estar vacío.")
        if not isinstance(active, bool):
            raise ValueError("El estado 'active' debe ser True o False.")

        self._id = id
        self._periodo = periodo
        self._fecha_creacion = date.today().strftime('%Y-%m-%d')
        self._active = active

    @property
    def id(self):
        """Obtendra el identificador único del período."""
        return self._id

    @property
    def periodo(self):
        """Obtendra el nombre o descripción del período."""
        return self._periodo

    @property
    def fecha_creacion(self):
        """Obtendra la fecha de creación del período."""
        return self._fecha_creacion
    
    @property
    def active(self):
        """Obtendra el estado de actividad del período."""
        return self._active

    def activar(self):
        """Activa el período."""
        self._active = True

    def desactivar(self):
        """Desactiva el período."""
        self._active = False


#############################################################################

# Clase que representa un profesor.
class Profesor:
    def __init__(self, cedula, nombre, active):
        self._cedula = cedula  # Identificador único para el profesor.
        self._nombre = nombre  # Nombre del profesor.
        self._fecha_creacion = date.today().strftime('%Y-%m-%d')  # Fecha de creación del registro del profesor, se asigna la fecha actual.
        self._active = active  # Estado de actividad del profesor (True o False).

    @property
    def cedula(self):
        """Obtendra el identificador único del profesor."""
        return self._cedula

    @property
    def nombre(self):
        """Obtendra el nombre del profesor."""
        return self._nombre
    
    @nombre.setter
    def nombre(self, nuevo_nombre):
        """Establece el nombre del profesor."""
        self._nombre = nuevo_nombre # Actualiza el nombre del profesor.
    
    @property
    def fecha_creacion(self):
        """Obtiene la fecha de creación del profesor."""
        return self._fecha_creacion
    
    @property
    def active(self):
        """Obtendra el estado de actividad del profesor."""
        return self._active
    
    