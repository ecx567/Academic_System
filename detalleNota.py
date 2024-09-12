from actions import Estudiante

class DetalleNota:
    """Representa los detalles de una nota para un estudiante específico."""

    def __init__(self, id, estudiante, nota1, nota2, recuperacion=None, observacion=None):
        self._id = id
        self._estudiante = estudiante
        self._nota1 = nota1
        self._nota2 = nota2
        self._recuperacion = recuperacion
        self._observacion = observacion

    @property
    def id(self):
        """Obtiene el identificador único del detalle de la nota."""
        return self._id

    @property
    def estudiante(self):
        """Obtiene el estudiante al que se le asigna la nota."""
        return self._estudiante
    
    @property
    def nota1(self):
        """Obtiene la primera nota del estudiante."""
        return self._nota1
    
    @property
    def nota2(self):
        """Obtiene la segunda nota del estudiante."""
        return self._nota2
    
    @property
    def recuperacion(self):
        """Obtiene la nota de recuperación del estudiante, si aplica."""
        return self._recuperacion

    def calcular_promedio(self):
        """Calcula el promedio de las notas, considerando la recuperación si existe."""
        if self.recuperacion is not None and self.recuperacion != 0:  
            try:
                recuperacion_float = float(self.recuperacion)
                nota = self.nota1 + self.nota2
                return (nota + recuperacion_float)/2
            except ValueError:
                print(f"Error: La nota de recuperación '{self.recuperacion}' no es un número válido.")
                return None
        else:
            return self.nota1 + self.nota2