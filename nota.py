from datetime import date
from detalleNota import DetalleNota
from datetime import date
from actions import Periodo
from actions import Profesor
from actions import Asignatura

class Nota:
    """Representa una nota asociada a un periodo, profesor y asignatura."""

    def __init__(self, id, periodo, profesor, asignatura, active=True):
        self._id = id
        self._periodo = periodo
        self._profesor = profesor
        self._asignatura = asignatura
        self._detalleNota = []
        self._fecha_creacion = date.today()
        self._active = active

    def add_detalle_nota(self, detalle_nota: DetalleNota):
        estudiante_id = detalle_nota.estudiante._cedula
        if any(dn.estudiante._cedula == estudiante_id for dn in self._detalleNota):
            raise ValueError("El estudiante ya tiene una nota asignada y registrada para esta asignatura y periodo.")
        self._detalleNota.append(detalle_nota)