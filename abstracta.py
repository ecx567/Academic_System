from abc import ABC, abstractmethod

class Alumno(ABC):
    """Clase abstracta que representa a un alumno."""

    def __init__(self, nombre, edad, grado, escuela):
        self._nombre = nombre
        self._edad = edad
        self._grado = grado
        self._escuela = escuela

    @property
    def nombre(self):
        """Obtiene el nombre del alumno."""
        return self._nombre

    @property
    def edad(self):
        """Obtiene la edad del alumno."""
        return self._edad

    @property
    def grado(self):
        """Obtiene la edad del alumno."""
        return self._grado
    
    @property
    def escuela(self):
        """Obtiene la edad del alumno."""
        return self._escuela

    @abstractmethod
    def notas(self):
        """Devuelve las notas del alumno."""
        pass

    def mostrar(self):
        """Imprime el nombre del alumno."""
        print(self.nombre)

class Estudiante(Alumno):
    """Subclase concreta que representa a un estudiante."""

    def __init__(self, nombre, edad, grado, escuela, promedio):
        super().__init__(nombre, edad, grado, escuela)
        self._promedio = promedio

    @property
    def promedio(self):
        """Obtiene el promedio del estudiante."""
        return self._promedio

    def notas(self):
        """Devuelve el promedio del estudiante como sus notas."""
        return self.promedio

    def presentar_datos(self):
        """Devuelve una cadena con la información del estudiante."""
        return f'Nombre: {self.nombre}, Edad: {self.edad}, Grado: {self.grado}, Escuela: {self.escuela}, Promedio: {self.promedio}'

if __name__ == '__main__':
    estudiante = Estudiante('Snayder', 20, 'Tercero', 'Educando Futuro', 85)
    print(estudiante.notas())
    print(estudiante.presentar_datos())