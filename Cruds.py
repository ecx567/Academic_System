from Icrud import Icrud
from clsJson import JsonFile
from components import Valida
from paths import path
from nota import Nota
from actions import Nivel
from detalleNota import DetalleNota
from actions import Estudiante,Periodo,Profesor,Asignatura
from utilities import borrarPantalla, gotoxy, purple_color, red_color, blue_color, reset_color, linea, green_color, yellow_color, cyan_color
import time
from datetime import datetime
from rich.console import Console
from rich.panel import Panel

# Crear consola rich
console = Console()

class CrudGrades(Icrud):
    def __init__(self):
        self.json_file = JsonFile(f'{path}/data/grades.json')
        self.valida = Valida()

    def create(self):
        """Esto creerea un nuevo registro de notas y lo guarda en el archivo JSON."""
        borrarPantalla()

        console.print(Panel("[bold purple] Crear Registro de Notas [/bold purple]", title="[bold cyan]Registro de Notas[/bold cyan]", border_style="green"))

        grades_data = self.json_file.read()
        if grades_data:
            id = max([grade['_id'] for grade in grades_data]) + 1
        else:
            id = 1

        # Obtener periodo, profesor y asignatura, asegúrate de validar que existan
        periodos_data = JsonFile(f'{path}/data/periods.json').read()
        profesores_data = JsonFile(f'{path}/data/teachers.json').read()
        asignaturas_data = JsonFile(f'{path}/data/subjects.json').read()

        # Mostrar periodos disponibles (solo los activos)
        borrarPantalla()
        console.print(Panel("[bold cyan]Periodos Disponibles:[/bold cyan]", border_style="green"))
        
        for periodo in periodos_data:
            if periodo.get('_active'):
                print(f"ID: {periodo['_id']}, Periodo: {periodo['_periodo']}")

        while True:
            periodo_id = self.valida.solo_numeros(f"{purple_color}Ingrese el ID correspondiente del periodo: {reset_color}", f"{red_color} El ID de periodo es inválido. Ingrese un número entero positivo.{reset_color}", 0, 5)
            periodo_seleccionado = next((p for p in periodos_data if p['_id'] == int(periodo_id) and p.get('_active')), None)
            if periodo_seleccionado:
                break
            else:
                console.print(f"{yellow_color}{' El Periodo no a sido encontrado o esta inactivo. Intentelo de nuevo. '}{reset_color}")

        # Mostrar profesores disponibles (solo los activos)
        borrarPantalla()

        console.print(Panel("[bold cyan]Profesores Disponibles:[/bold cyan]", border_style="green"))
        for profesor in profesores_data:
            if profesor.get('_active'):
                print(f"ID: {profesor['_cedula']}, Nombre: {profesor['_nombre']}")

        while True:
            profesor_cedula = self.valida.cedula(f"{purple_color}Ingrese el numero de la cédula del profesor: {reset_color}", 0, 5)
            profesor_seleccionado = next((p for p in profesores_data if p['_cedula'] == profesor_cedula and p.get('_active')), None)
            if profesor_seleccionado:
                break
            else:
                console.print(f"{yellow_color}{' El Profesor no a sido encontrado o esta inactivo. Intente de nuevo. '}{reset_color}")

        # Mostrar asignaturas disponibles (solo las activas)
        borrarPantalla()
        
        console.print(Panel("[bold cyan]Asignaturas Disponibles:[/bold cyan]", border_style="green"))
        for asignatura in asignaturas_data:
            if asignatura.get('_active'):
                print(f"ID: {asignatura['_id']}, Nombre: {asignatura['_descripcion']}")

        while True:
            asignatura_id = self.valida.solo_numeros("Ingrese el ID de la asignatura: ", "El ID de la asignatura es inválido. Ingrese un número entero positivo.", 0, 5)
            asignatura_seleccionada = next((a for a in asignaturas_data if a['_id'] == int(asignatura_id) and a.get('_active')), None)
            if asignatura_seleccionada:
                break
            else:
                console.print(f"{yellow_color}{' La Asignatura no a sido encontrada o esta inactiva. Intente de nuevo. '}{reset_color}")

        # Obtener todos los estudiantes desde el archivo students.json
        estudiantes_data = JsonFile(f'{path}/data/students.json').read()

        
        # Crear la instancia de Nota, almacenando solo los IDs
        nueva_nota = Nota(id, 
                        periodo_seleccionado['_periodo'], 
                        profesor_seleccionado['_nombre'],
                        asignatura_seleccionada['_descripcion']
                        )

        for estudiante_data in estudiantes_data:
            if estudiante_data.get('_active'): 
                estudiante = Estudiante(estudiante_data['_cedula'], estudiante_data['_nombre'], estudiante_data['_apellido'], estudiante_data['_fecha_nacimiento'], estudiante_data['_active'])
                while True:
                    try:
                        nota1 = self.valida.valida_nota(f"Ingrese la primera nota para {estudiante._nombre}: ", "Nota inválida. Ingrese un número decimal positivo.")
                        nota2 = self.valida.valida_nota(f"Ingrese la segunda nota para {estudiante._nombre}: ", "Nota inválida. Ingrese un número decimal positivo.")
                        recuperacion = input(f"Ingrese la nota de recuperación para {estudiante._nombre} (dejar en blanco si no aplica): ") or 0
                        observacion = input(f"Ingrese una observación para {estudiante._nombre} (opcional): ")

                        detalle = DetalleNota(None, estudiante, float(nota1), float(nota2),
                                            float(recuperacion) if recuperacion else None, observacion)
                        nueva_nota.add_detalle_nota(detalle) 
                        break
                    
                    except ValueError as e:
                        print(f"Error: {e}")


        grade_dict = {
            '_id': id,
            '_periodo_id': nueva_nota._periodo,
            '_profesor_id': nueva_nota._profesor,  # Asumiendo que el identificador del profesor es la cédula
            '_asignatura_id': nueva_nota._asignatura,
            '_fecha_creacion': nueva_nota._fecha_creacion.strftime('%Y-%m-%d'),  # Convertir la fecha a cadena
            '_active': nueva_nota._active,
            '_detalleNota': [detalle.__dict__ for detalle in nueva_nota._detalleNota]
}

        # Convertir los objetos DetalleNota dentro de _detalleNota a diccionarios
        grade_dict['_detalleNota'] = [detalle.__dict__ for detalle in nueva_nota._detalleNota] 

        grades_data.append(grade_dict)
        self.json_file.save(grades_data)
        console.print(f"{green_color}{' Registro de calificaciones a sido creado exitosamente. '}{reset_color}")
        time.sleep(2)

    def update(self):
        """Actualiza un registro de calificaciones existente en el archivo JSON."""
        borrarPantalla()
        console.print(Panel("[bold cyan] Actualizar Registro de Notas [/bold cyan]", title="[bold yellow]Actualizar Notas[/bold yellow]", border_style="blue"))


        grades_data = self.json_file.read()
        id = self.valida.solo_numeros("Ingrese el ID del registro de calificaciones a actualizar: ", "El ID es inválido. Ingrese un número entero positivo.", 0, 5)
        grade_dict = next((g for g in grades_data if g['_id'] == int(id)), None)

        if grade_dict:
            # Obtener periodo, profesor y asignatura, asegúrate de validar que existan
            periodos_data = JsonFile(f'{path}/data/periods.json').read()
            profesores_data = JsonFile(f'{path}/data/teachers.json').read()
            asignaturas_data = JsonFile(f'{path}/data/subjects.json').read()


            # Mostrar periodos disponibles (solo los activos)
            borrarPantalla()
            print(f"{cyan_color}\nPeriodos disponibles:{reset_color}")
            for periodo in periodos_data:
                if periodo.get('_active'):
                    print(f"ID: {periodo['_id']}, Periodo: {periodo['_periodo']}")

            while True:
                periodo_id = self.valida.solo_numeros(f"{purple_color}Ingrese el ID del periodo: {reset_color}", f"{red_color} El ID del periodo es inválido. Ingrese un número entero positivo.{reset_color}", 0, 5)
                periodo_seleccionado = next((p for p in periodos_data if p['_id'] == int(periodo_id) and p.get('_active')), None)
                if periodo_seleccionado:
                    break
                else:
                    print(f"{yellow_color}{' El Periodo no a sido encontrado o esta inactivo. Intente de nuevo. '.center(80)}{reset_color}")

            # Mostrar profesores disponibles (solo los activos)
            borrarPantalla()
            print(f"{cyan_color}\nProfesores disponibles:{reset_color}")
            for profesor in profesores_data:
                if profesor.get('_active'):
                    print(f"ID: {profesor['_cedula']}, Nombre: {profesor['_nombre']}")

            while True:
                profesor_cedula = self.valida.cedula(f"{purple_color}Ingrese el numero de la cédula del profesor: {reset_color}", 0, 5)
                profesor_seleccionado = next((p for p in profesores_data if p['_cedula'] == profesor_cedula and p.get('_active')), None)
                if profesor_seleccionado:
                    break
                else:
                    print(f"{yellow_color}{' El Profesor no a sido encontrado o esta inactivo. Intentelo de nuevo. '.center(80)}{reset_color}")

            # Mostrar asignaturas disponibles (solo las activas)
            borrarPantalla()
            print(f"{cyan_color}\nAsignaturas disponibles:{reset_color}")
            for asignatura in asignaturas_data:
                if asignatura.get('_active'):
                    print(f"ID: {asignatura['_id']}, Nombre: {asignatura['_descripcion']}")

            while True:
                asignatura_id = self.valida.solo_numeros("Ingrese el ID de la asignatura: ", "ID de asignatura inválido. Ingrese un número entero positivo.", 0, 5)
                asignatura_seleccionada = next((a for a in asignaturas_data if a['_id'] == int(asignatura_id) and a.get('_active')), None)
                if asignatura_seleccionada:
                    break
                else:
                    print(f"{yellow_color}{' La Asignatura no a sido encontrado o esta inactivo. Intente de nuevo. '.center(80)}{reset_color}")

            # Obtener todos los estudiantes desde el archivo students.json
            estudiantes_data = JsonFile(f'{path}/data/students.json').read()

            # Actualizar la instancia de Nota, almacenando solo los IDs
            nota_actualizada = Nota(grade_dict['_id'], 
                            periodo_seleccionado['_periodo'], 
                            profesor_seleccionado['_nombre'],
                            asignatura_seleccionada['_descripcion']
                            )

            # Limpiar los detalles de la nota anterior
            nota_actualizada._detalleNota = []

            for estudiante_data in estudiantes_data:
                if estudiante_data.get('_active'): 
                    estudiante = Estudiante(estudiante_data['_cedula'], estudiante_data['_nombre'], estudiante_data['_apellido'], estudiante_data['_fecha_nacimiento'], estudiante_data['_active'])
                    while True:
                        try:
                            nota1 = self.valida.valida_nota(f"Ingrese la primera nota para {estudiante._nombre}: ", "La Nota es inválida. Ingrese un número decimal positivo.")
                            nota2 = self.valida.valida_nota(f"Ingrese la segunda nota para {estudiante._nombre}: ", "La Nota es inválida. Ingrese un número decimal positivo.")
                            recuperacion = input(f"Ingrese la nota de recuperación para {estudiante._nombre} (dejar en blanco si no aplica): ")
                            observacion = input(f"Ingrese una observación para {estudiante._nombre} (opcional): ")

                            detalle = DetalleNota(None, estudiante, float(nota1), float(nota2),
                                                  float(recuperacion) if recuperacion else None, observacion)
                            nota_actualizada.add_detalle_nota(detalle) 
                            break
                        except ValueError as e:
                            print(f"Error: {e}")

            # Actualizar el registro en grades_data
            for i, g in enumerate(grades_data):
                if g['_id'] == nota_actualizada._id:
                    # Convertir el objeto Nota a un diccionario, incluyendo los IDs de las entidades relacionadas
                    grade_dict = nota_actualizada.__dict__
                    grade_dict['_periodo_id'] = nota_actualizada._periodo  # Asignar el ID del periodo directamente
                    grade_dict['_profesor_id'] = nota_actualizada._profesor  # Asignar la cédula del profesor directamente
                    grade_dict['_asignatura_id'] = nota_actualizada._asignatura  # Asignar el ID de la asignatura directamente

                    # Convertir los objetos DetalleNota dentro de _detalleNota a diccionarios
                    grade_dict['_detalleNota'] = [detalle.__dict__ for detalle in nota_actualizada._detalleNota] 

                    grades_data[i] = grade_dict
                    break

            self.json_file.save(grades_data)
            print(f"{green_color}{' El Registro de calificaciones a sido actualizado exitosamente. '.center(80)}{reset_color}")
            time.sleep(2)
        else:
            print("Registro de calificaciones no encontrado.")
            time.sleep(2)

    def delete(self):
        """Elimina un registro de calificaciones del archivo JSON."""
        borrarPantalla()
        linea(80, green_color)
        print(f"{purple_color}{' Eliminar Registro de Notas '.center(80)}{reset_color}")
        linea(80, green_color)

        data = self.json_file.read()

        id = self.valida.solo_numeros("Ingrese el ID del registro de calificaciones a eliminar: ", "ID inválido. Ingrese un número entero positivo.", 0, 5)

        # Buscar y eliminar el registro por ID
        data = [g for g in data if g['_id'] != int(id)]

        self.json_file.save(data)
        print(f"{green_color}{' Registro de notas eliminado exitosamente. '.center(80)}{reset_color}")
        time.sleep(2)


    def consult(self):
        """Muestra la lista de registros de calificaciones o busca uno específico."""
        borrarPantalla()
        linea(80, green_color)
        print(f"{purple_color}{' Consultar Registro de Notas '.center(80)}{reset_color}")
        linea(80, green_color)

        data = self.json_file.read()
        if not data:
            print("No hay registros de calificaciones.")
            return

        # Obtener datos de periodos, profesores y asignaturas para mostrar nombres en lugar de IDs
        periodos_data = JsonFile(f'{path}/data/periods.json').read()
        profesores_data = JsonFile(f'{path}/data/teachers.json').read()
        asignaturas_data = JsonFile(f'{path}/data/subjects.json').read()

        while True:
            print(f"{cyan_color}\n{f'1. Listar todos los registros de calificaciones'.center(80)}")
            print(f"{'2. Buscar registro por ID'.center(80)}")
            print(f"{'3. Volver'.center(80)}{reset_color}")
            


            opcion = input(f"{red_color}Seleccione una opción: {reset_color}")

            if opcion == '1':
                borrarPantalla()
                for grade_dict in data:
                    print(f'{cyan_color} Periodo:  {grade_dict["_periodo_id"]}  Profesor: {grade_dict["_profesor_id"]}  Asignatura: {grade_dict["_asignatura_id"]} {reset_color}')


                    for detalle in grade_dict['_detalleNota']:
                        estudiantes_data = JsonFile(f'{path}/data/students.json').read()
                        estudiante_data = next((s for s in estudiantes_data if s['_cedula'] == detalle['_estudiante']['_cedula']), None)  # Corrección aquí
                        if estudiante_data:
                            nombre_estudiante = estudiante_data['_nombre'] + " " + estudiante_data['_apellido']
                        else:
                            nombre_estudiante = "El Estudiante no a sido encontrado"

                        # Calcular el promedio utilizando el método de DetalleNota
                        detalle_nota_obj = DetalleNota(None, detalle['_estudiante']['_cedula'], detalle['_nota1'], detalle['_nota2'], detalle.get('_recuperacion'), detalle.get('_observacion'))
                        promedio = detalle_nota_obj.calcular_promedio()
                        if promedio is None:  # Verificar si hubo un error en el cálculo del promedio
                            estado = "Error en el cálculo"
                        else:
                            estado = "Aprobado" if promedio >= 70 else "Reprobado"

                        print(f"  - Estudiante: {nombre_estudiante}, Nota 1: {detalle['_nota1']}, Nota 2: {detalle['_nota2']}, Recuperación: {detalle.get('_recuperacion')}, Observación: {detalle.get('_observacion')}, Promedio: {promedio}, Estado: {estado}")

            elif opcion == '2':
                borrarPantalla()
                id = self.valida.solo_numeros("Ingrese el ID del registro a buscar: ", "ID inválido. Ingrese un número entero positivo.", 0, 5)
                grade_dict = next((g for g in data if g['_id'] == int(id)), None)
                if grade_dict:
                    print(f"\nID: {grade_dict['_id']}, Periodo: {grade_dict['_periodo_id']}, Profesor: {grade_dict['_profesor_id']}, Asignatura: {grade_dict['_asignatura_id']}")
                    for detalle in grade_dict['_detalleNota']:
                        estudiantes_data = JsonFile(f'{path}/data/students.json').read()
                        estudiante_data = next((s for s in estudiantes_data if s['_cedula'] == detalle['_estudiante']['_cedula']), None)  
                        if estudiante_data:
                            nombre_estudiante = estudiante_data['_nombre'] + " " + estudiante_data['_apellido']
                        else:
                             nombre_estudiante = "El Estudiante no a sido encontrado"
                        
                        # Calcular el promedio utilizando el método de DetalleNota
                        detalle_nota_obj = DetalleNota(None, detalle['_estudiante']['_cedula'], detalle['_nota1'], detalle['_nota2'], detalle.get('_recuperacion'), detalle.get('_observacion'))
                        promedio = detalle_nota_obj.calcular_promedio()
                        if promedio is None:  # Verificar si hubo un error en el cálculo del promedio
                            estado = "Error en el cálculo"
                        else:
                            estado = "Aprobado" if promedio >= 70 else "Reprobado"

                        print(f"  - Estudiante: {nombre_estudiante}, Nota 1: {detalle['_nota1']}, Nota 2: {detalle['_nota2']}, Recuperación: {detalle.get('_recuperacion')}, Observación: {detalle.get('_observacion')}, Promedio: {promedio}, Estado: {estado}")

                else:
                    console.print(f"{red_color}Registro de notas no encontrado.{reset_color}")
                    time.sleep(2)

            elif opcion == '3':
                break
            else:
                console.print(f"{red_color}La Opción es inválida. Intente de nuevo.{reset_color}")
                time.sleep(2)

################################################################################################################

class CrudStudents(Icrud):
    def __init__(self):
        self.json_file = JsonFile(f"{path}/data/students.json") # Modifica la ruta del archivo JSON
        self.valida = Valida()

    def create(self):
        """Crea un nuevo estudiante y lo guarda en el archivo JSON."""
        borrarPantalla()

        console.print(Panel("[bold purple] Crear Estudiante [/bold purple]", border_style="green"))

        data = self.json_file.read()
        estudiantes = [Estudiante(s['_cedula'], s['_nombre'], s['_apellido'], s['_fecha_nacimiento'], s['_active']) for s in data] # Convertir a objetos Estudiante

        while True:
            cedula = self.valida.cedula(f"{purple_color}Ingrese el numero de la cédula del estudiante: {reset_color}", 0, 5)
            if not any(s._cedula == cedula for s in estudiantes):  # Verificar si la cédula ya existe
                break
            else:
                console.print(f"{red_color}La Cédula ya registrada. Intente de nuevo.{reset_color}")

        nombre = self.valida.solo_letras(f"{purple_color}Ingrese el nombre del estudiante: {reset_color}", f"{red_color} Nombre inválido. Solo se permiten letras.{reset_color}")
        apellido = self.valida.solo_letras(f"{purple_color}Ingrese el apellido del estudiante: {reset_color}", f"{red_color} Apellido inválido. Solo se permiten letras.{reset_color}")
        
        fecha_nacimiento_str = input(f"          ------>   | {purple_color}Ingrese la fecha de nacimiento (YYYY-MM-DD): {reset_color}")
        fecha_nacimiento = fecha_nacimiento_str

        nuevo_estudiante = Estudiante(cedula, nombre, apellido, fecha_nacimiento) 
        estudiantes.append(nuevo_estudiante)

        # Convertir los objetos Estudiante de vuelta a diccionarios para guardarlos en el JSON
        data = [estudiante.__dict__ for estudiante in estudiantes]
        self.json_file.save(data)
        console.print(f"{green_color}Estudiante creado exitosamente.{reset_color}")
        time.sleep(2)

    def update(self):
        borrarPantalla()

        console.print(Panel("[bold purple] Actualizar Estudiante [/bold purple]", border_style="green"))

        data = self.json_file.read()
        estudiantes = [Estudiante(s['_cedula'], s['_nombre'], s['_apellido'],
                                  ['_fecha_nacimiento'], s['_active']) for s in data]

        while True:  # Bucle para asegurar que se ingrese una cédula válida
            cedula = self.valida.cedula(f"{purple_color}Ingrese la cédula del estudiante a actualizar: {reset_color}", 0, 5)
            if cedula is not None:
                break

        estudiante = next((s for s in estudiantes if s._cedula == cedula), None)
        if estudiante:
            # Solicitar nuevo nombre, manteniendo el original si se presiona Enter
            nuevo_nombre = input(f"          ------>   | {purple_color}Ingrese el nuevo nombre del estudiante (Enter para mantener {estudiante.nombre}): {reset_color}")
            estudiante._nombre = nuevo_nombre if nuevo_nombre else estudiante.nombre

            # Solicitar nuevo apellido, manteniendo el original si se presiona Enter
            nuevo_apellido = input(f"          ------>   | {purple_color}Ingrese el nuevo apellido del estudiante (Enter para mantener {estudiante.apellido}): {reset_color}")
            estudiante._apellido = nuevo_apellido if nuevo_apellido else estudiante.apellido

            # Convertir los objetos Estudiante de vuelta a diccionarios para guardarlos en el JSON
            data = [estudiante.__dict__ for estudiante in estudiantes]
            self.json_file.save(data)
            print()
            console.print(f"{green_color}Estudiante actualizado exitosamente.{reset_color}")
        else:
            console.print(f"{red_color}El Estudiante no a sido encontrado.{reset_color}")
            time.sleep(2)

    def delete(self):
        """Elimina un estudiante del archivo JSON."""
        borrarPantalla()

        console.print(Panel("[bold purple] Eliminar Estudiante [/bold purple]".center(150), border_style="green"))

        data = self.json_file.read()
        estudiantes = [Estudiante(s['_cedula'], s['_nombre'], s['_apellido'], 
                                  s['_fecha_nacimiento'], 
                                  s['_active']) for s in data]

        while True:
            cedula = self.valida.cedula(f"{purple_color}Ingrese la cédula del estudiante a eliminar: {reset_color}", 0, 5) 
            if cedula is not None:
                break

        estudiante_a_eliminar = next((s for s in estudiantes if s._cedula == cedula), None)

        if estudiante_a_eliminar:
            # Mostrar los datos del estudiante antes de eliminarlo
            print("\nDatos del estudiante a eliminar:".center(80))
            print(f"Cédula: {estudiante_a_eliminar._cedula}")
            print(f"Nombre: {estudiante_a_eliminar._nombre}")
            print(f"Apellido: {estudiante_a_eliminar._apellido}")
            

            # Solicitar confirmación al usuario
            confirmacion = input(f"{purple_color}\n¿Realmente desea eliminar este estudiante? (s/n): {reset_color}")
            if confirmacion.lower() == 's':
                estudiantes.remove(estudiante_a_eliminar)
                data = [estudiante.__dict__ for estudiante in estudiantes]
                self.json_file.save(data)
                console.print(f"{green_color}El Estudiante fue eliminado exitosamente.{reset_color}")
            else:
                console.print(f"{yellow_color}Eliminación cancelada.{reset_color}")
        else:
            console.print(f"{red_color}El Estudiante no a sido encontrado.{reset_color}")

        time.sleep(2)

    def consult(self):
        """Muestra la lista de estudiantes o busca uno específico."""
        borrarPantalla()
        linea(80, green_color)
        console.print(Panel("[bold purple] Consultar Estudiante(s) [/bold purple]".center(150), border_style="green"))
        linea(80, green_color)

        data = self.json_file.read()
        if not data:
            console.print(f"{yellow_color}No hay estudiantes registrados.{reset_color}")
            time.sleep(2)
            return

        while True:
            print(f"{cyan_color}1. Listar todos los estudiantes".center(150))
            print("2. Buscar estudiante por cédula".center(150)) 
            print(f"3. Volver{reset_color}".center(150))

            opcion = input(f"{red_color}Seleccione una opción: {reset_color}")

            if opcion == '1':
                borrarPantalla()
                for student_data in data:
                    # Crear un objeto Estudiante a partir de los datos del diccionario
                    estudiante = Estudiante(student_data['_cedula'], student_data['_nombre'], student_data['_apellido'], 
                                          student_data['_fecha_nacimiento'], 
                                          student_data['_active'])
                    
                    # Usar las propiedades del objeto Estudiante para mostrar la información
                    print(f"Cédula: {estudiante._cedula}, Nombre: {estudiante._nombre}, Apellido: {estudiante._apellido}, ")
            elif opcion == '2':
                borrarPantalla()
                while True:
                    cedula = self.valida.cedula(f"{purple_color}Ingrese la cédula del estudiante a buscar: {reset_color}", 0, 5)
                    if cedula is not None:
                        break

                student_data = next((s for s in data if s['_cedula'] == cedula), None)
                if student_data:
                    # Crear un objeto Estudiante a partir de los datos del diccionario
                    estudiante = Estudiante(student_data['_cedula'], student_data['_nombre'], student_data['_apellido'], 
                                          student_data['_fecha_nacimiento'], 
                                          student_data['_active'])

                    # Usar las propiedades del objeto Estudiante para mostrar la información
                    print(f"Cédula: {estudiante._cedula}, Nombre: {estudiante.nombre}, Apellido: {estudiante._apellido}, ")
                else:
                    console.print(f"{yellow_color}El Estudiante no a sido encontrado.{reset_color}")
                    time.sleep(2)
            elif opcion == '3':
                break
            else:
                console.print(f"{red_color}Opción inválida. Intentelo de nuevo.{reset_color}")
                time.sleep(2)

############################################################################################################

class CrudSubjects(Icrud):
    def __init__(self):
        self.json_file = JsonFile(f'{path}/data/subjects.json')
        self.niveles_json_file = JsonFile(f'{path}/data/levels.json')
        self.valida = Valida()

    def create(self):
        """Crea una nueva asignatura y la guarda en el archivo JSON."""
        borrarPantalla()

        console.print(Panel("[bold purple]Crear Asignatura[/bold purple]".center(150), border_style="green"))

        data = self.json_file.read()
        asignaturas = [Asignatura(s['_id'], s['_descripcion'], s['_nivel'], s['_active']) for s in data]

        if asignaturas:
            id = max([asignatura.id for asignatura in asignaturas]) + 1
        else:
            id = 1

        descripcion = self.valida.solo_letras(f"{purple_color}Ingrese la descripción de la asignatura: {reset_color}", f"{red_color}Descripción inválida. Solo se permiten letras.{reset_color}")

        # Obtener niveles disponibles (solo los activos)
        niveles_data = self.niveles_json_file.read()
        niveles = [Nivel(n['_id'], n['_nivel']) for n in niveles_data]
        niveles_activos = [nivel for nivel in niveles if nivel._active]

        if not niveles_activos:
            console.print(f"{yellow_color}No hay niveles activos registrados. Debe crear un nivel antes de crear una asignatura.{reset_color}")
            time.sleep(2)
            return

        print("\nNiveles disponibles:")
        for nivel in niveles_activos:
            print(f"ID: {nivel._id}, Nivel: {nivel._nivel}")

        while True:
            nivel_id = self.valida.solo_numeros(f"{purple_color}Ingrese el ID del nivel: {reset_color}", f"{red_color}El ID del nivel es inválido. Ingrese un número entero positivo. {reset_color}", 0, 5)
            nivel_seleccionado = next((n for n in niveles_activos if n._id == int(nivel_id)), None)
            if nivel_seleccionado:
                break
            else:
                console.print(f"{red_color}Nivel no encontrado o inactivo. Intente de nuevo.{reset_color}")

        nueva_asignatura = Asignatura(id, descripcion, nivel_seleccionado.id, True)  # Almacenar solo el ID del nivel
        asignaturas.append(nueva_asignatura)

        # Convertir los objetos Asignatura a diccionarios, asegurándonos de que 'nivel' sea un ID
        data = [{**asignatura.__dict__, 'nivel': asignatura.nivel} for asignatura in asignaturas] 
        self.json_file.save(data)
        console.print(f"{green_color}La Asignatura a sido creada exitosamente.{reset_color}")
        time.sleep(2)

    def update(self):
        """Actualiza una asignatura existente en el archivo JSON."""
        borrarPantalla()
        
        console.print(Panel("[bold purple]Actualizar Asignatura[/bold purple]".center(150), border_style="green"))

        data = self.json_file.read()
        asignaturas = [Asignatura(s['_id'], s['_descripcion'], s['_nivel'], s['_active']) for s in data]

        id = self.valida.solo_numeros(f"{purple_color}Ingrese el ID de la asignatura a actualizar: {reset_color}", f"{red_color}ID inválido. Ingrese un número entero positivo.{reset_color}", 0, 5)
        asignatura = next((a for a in asignaturas if a._id == int(id)), None)

        if asignatura:
            # Solicitar nueva descripción, manteniendo la original si se presiona Enter
            nueva_descripcion = input(f"{purple_color}Ingrese la nueva descripción de la asignatura (Enter para mantener '{asignatura._descripcion}'): {reset_color}")
            if nueva_descripcion:  # Actualizar solo si se ingresa un nuevo valor
                asignatura._descripcion = self.valida.solo_letras(nueva_descripcion, f"{red_color}Descripción inválida. Solo se permiten letras.{reset_color}")

            # Obtener niveles disponibles (solo los activos)
            niveles_data = self.niveles_json_file.read()
            niveles = [Nivel(n['_id'], n['_nivel']) for n in niveles_data]
            niveles_activos = [nivel for nivel in niveles if nivel._active]

            if not niveles_activos:
                console.print(f"{yellow_color}No hay niveles activos registrados. No se puede actualizar el nivel de la asignatura.{reset_color}")
                time.sleep(2)
            else:
                print("\nNiveles disponibles:")
                for nivel in niveles_activos:
                    print(f"ID: {nivel._id}, Nivel: {nivel._nivel}")

                # Solicitar al usuario que elija un nivel válido o mantenga el actual
                while True:
                    nivel_id_input = input(f"{purple_color}Ingrese el ID del nuevo nivel (Enter para mantener '{asignatura._nivel}'): {reset_color}")
                    if nivel_id_input == "":
                        break  # Mantener el nivel actual
                    try:
                        nivel_id = int(nivel_id_input)
                        nivel_seleccionado = next((n for n in niveles_activos if n._id == nivel_id), None)
                        if nivel_seleccionado:
                            asignatura._nivel = nivel_seleccionado.id
                            break
                        else:
                            console.print(f"{yellow_color}El Nivel no a sido encontrado o esta inactivo. Intente de nuevo.{reset_color}")
                    except ValueError:
                        print(f"{red_color}{' ID de nivel inválido. Ingrese un número entero positivo o Enter para mantener el nivel actual.'.center(80)}{reset_color}")

            # Solicitar nuevo estado, manteniendo el original si se presiona Enter
            while True:
                nuevo_estado = input(f"{purple_color}Ingrese el nuevo estado de la asignatura (activo/inactivo) (actual: {'activo' if asignatura.active else 'inactivo'}): {reset_color}")
                if nuevo_estado.lower() in ['activo', 'inactivo']:
                    if nuevo_estado.lower() == 'activo':
                        asignatura.activar()
                    else:
                        asignatura.desactivar()
                    break
                elif nuevo_estado == "":  # Mantener el estado original si se presiona Enter
                    break
                else:
                    mensaje = f"{red_color}Estado inválido. Ingrese 'activo' o 'inactivo' o presione Enter para mantener el estado actual.{reset_color}"
                    print(mensaje.center(80))

            data = [asignatura.__dict__ for asignatura in asignaturas]
            self.json_file.save(data)
            console.print(f"{green_color}La Asignatura fue actualizada exitosamente.{reset_color}")
            time.sleep(2)
        else:
            console.print(f"{red_color}La Asignatura no fue encontrada.{reset_color}")
            time.sleep(2)

    def delete(self):
        """Elimina una asignatura del archivo JSON."""
        borrarPantalla()

        console.print(Panel("[bold red]Eliminar Asignatura[/bold red]".center(150), border_style="green"))

        data = self.json_file.read()
        asignaturas = [Asignatura(s['_id'], s['_descripcion'], s['_nivel'], s['_active']) for s in data]

        id = self.valida.solo_numeros("Ingrese el ID de la asignatura a eliminar: ", "El ID es inválido. Ingrese un número entero positivo.", 0, 5)
        asignatura_a_eliminar = next((a for a in asignaturas if a._id == int(id)), None)

        if asignatura_a_eliminar:
            # Mostrar los detalles de la asignatura antes de eliminarla
            print("\nDetalles de la asignatura a eliminar:")
            print(f"ID: {asignatura_a_eliminar._id}")
            print(f"Descripción: {asignatura_a_eliminar._descripcion}")
            print(f"Nivel: {asignatura_a_eliminar._nivel}")
            print(f"Estado: {'Activo' if asignatura_a_eliminar._active else 'Inactivo'}")

            # Solicitar confirmación al usuario
            confirmacion = input(f"{purple_color}\n¿Realmente desea eliminar esta asignatura? (s/n): {reset_color}")
            if confirmacion.lower() == 's':
                asignaturas = [a for a in asignaturas if a._id != int(id)]
                data = [asignatura.__dict__ for asignatura in asignaturas]
                self.json_file.save(data)
                console.print(f"{green_color}La Asignatura fue eliminada exitosamente.{reset_color}")
            else:
                console.print(f"{yellow_color}Eliminación cancelada.{reset_color}")
        else:
            console.print(f"{red_color}La Asignatura no fue encontrada.{reset_color}")

        time.sleep(2)

    def consult(self):
        """Muestra la lista de asignaturas o busca una específica."""
        borrarPantalla()

        console.print(Panel("[bold cyan]Consultar Asignatura[/bold cyan]".center(150), border_style="green"))

        data = self.json_file.read()
        asignaturas = [Asignatura(s['_id'], s['_descripcion'], s['_nivel'], s['_active']) for s in data]

        # Obtener todos los niveles desde el archivo niveles.json
        niveles_data = self.niveles_json_file.read()
        niveles = [Nivel(n['_id'], n['_nivel']) for n in niveles_data] 

        if not asignaturas:
            console.print(f"{yellow_color}No hay asignaturas registradas.{reset_color}")
            return

        while True:
            print(f"{cyan_color}1. Listar todas las asignaturas".center(150))
            print("2. Buscar asignatura por ID".center(150))
            print(f"3. Volver{reset_color}".center(150))

            opcion = input(f"{red_color}Seleccione una opción: {reset_color}")

            if opcion == '1':
                borrarPantalla()
                for asignatura in asignaturas:
                    # Buscar el nivel correspondiente por su ID
                    nivel = next((n for n in niveles if n._id == asignatura._nivel), None)
                    nombre_nivel = nivel._nivel if nivel else "Nivel no encontrado"
                    print(f"ID: {asignatura._id}, Descripción: {asignatura._descripcion}, Nivel: {nombre_nivel}, Estado: {'Activo' if asignatura._active else 'Inactivo'}")
            elif opcion == '2':
                borrarPantalla()
                id = self.valida.solo_numeros(f"{purple_color}Ingrese el ID de la asignatura a buscar: {reset_color}", f"{red_color}ID inválido. Ingrese un número entero positivo.{reset_color}", 0, 5)
                asignatura = next((a for a in asignaturas if a._id == int(id)), None)
                if asignatura:
                    # Buscar el nivel correspondiente por su ID
                    nivel = next((n for n in niveles if n._id == asignatura._nivel), None)
                    nombre_nivel = nivel._nivel if nivel else "Nivel no encontrado"
                    print(f"ID: {asignatura._id}, Descripción: {asignatura._descripcion}, Nivel: {nombre_nivel}, Estado: {'Activo' if asignatura._active else 'Inactivo'}")
                else:
                    console.print(f"{yellow_color}Asignatura no encontrada.{reset_color}")
                    time.sleep(2)
            elif opcion == '3':
                break
            else:
                console.print(f"{red_color}Opción inválida. Intente de nuevo.{reset_color}")
                time.sleep(2)

##################################################################################

class CrudTeacher(Icrud):
    def __init__(self):
        self.json_file = JsonFile(f"{path}/data/teachers.json")
        self.valida = Valida()

    def create(self):
        borrarPantalla()
        
        console.print(Panel("[bold purple] Crear Profesor [/bold purple]".center(150), border_style="green"))

        """Crea un nuevo profesor y lo guarda en el archivo JSON."""
        data = self.json_file.read()
        if not data:  # Si el archivo está vacío, inicializar data con una lista vacía
            data = []
        # Convertir los datos del JSON a objetos Profesor
        profesores = [Profesor(t['_cedula'], t['_nombre'], t.get('_active', True)) for t in data]

        while True:  # Bucle para asegurar que la cédula sea única y válida
            cedula = self.valida.cedula(f"{purple_color}Ingrese la cédula del profesor: {reset_color}", 0, 5)
            if cedula is None:  # Manejar el caso de error en la validación
                continue
            if not any(p.cedula == cedula for p in profesores):
                break
            else:
                console.print(f"{red_color}La Cédula ya esta registrada. Intente de nuevo.{reset_color}")

        nombre = self.valida.solo_letras(f"{purple_color}Ingrese el nombre del profesor: {reset_color}", f"{red_color}Nombre inválido. Solo se permiten letras.{reset_color}")

        nuevo_profesor = Profesor(cedula, nombre, True) 
        profesores.append(nuevo_profesor)

        # Convertir los objetos Profesor de vuelta a diccionarios para guardarlos en el JSON
        data = [profesor.__dict__ for profesor in profesores]
        self.json_file.save(data)
        console.print(f"{green_color} Profesor Creado Exitosamente. {reset_color}")
        time.sleep(2)

    def update(self):
        """Actualiza un profesor existente en el archivo JSON."""
        borrarPantalla()
        
        console.print(Panel("[bold purple] Actualizar Profesor [/bold purple]".center(150), border_style="green"))

        data = self.json_file.read()
        profesores = [Profesor(t['_cedula'], t['_nombre'], t.get('_active', True)) for t in data]

        while True:
            cedula = self.valida.cedula(f"{purple_color}Ingrese la cédula del profesor a actualizar: {reset_color}", 0, 5)
            if cedula is not None:
                break

        profesor = next((p for p in profesores if p.cedula == cedula), None)

        if profesor:
            profesor.nombre = self.valida.solo_letras(f"{purple_color}Ingrese el nuevo nombre del profesor: {reset_color}", f"{red_color}Nombre inválido. Solo se permiten letras. {reset_color}")
            # Actualiza otros atributos del profesor según sea necesario, utilizando profesor.atributo = nuevo_valor

            # Convertir los objetos Profesor de vuelta a diccionarios para guardarlos en el JSON
            data = [profesor.__dict__ for profesor in profesores]
            self.json_file.save(data)
            console.print(f"{green_color} El Profesor fue actualizado exitosamente. {reset_color}")
            time.sleep(2)
        else:
            console.print(f"{yellow_color} El Profesor no fue encontrado. {reset_color}")
            time.sleep(2)

    def delete(self):
        """Elimina un profesor del archivo JSON."""
        borrarPantalla()

        console.print(Panel("[bold red] Eliminar Profesor [/bold red]".center(150), border_style="green"))

        data = self.json_file.read()
        profesores = [Profesor(t['_cedula'], t['_nombre'], t.get('_active', True)) for t in data]

        while True:
            cedula = self.valida.cedula(f"{purple_color}Ingrese la cédula del profesor a eliminar: {reset_color}", 0, 5)
            if cedula is not None:
                break

        # Buscar el profesor por cédula en la lista de objetos Profesor
        profesor_a_eliminar = next((p for p in profesores if p.cedula == cedula), None)

        if profesor_a_eliminar:
            # Mostrar los datos del profesor antes de eliminarlo
            print("\nDatos del profesor a eliminar:".center(150))
            print(f"Cédula: {profesor_a_eliminar.cedula}".center(150))
            print(f"Nombre: {profesor_a_eliminar.nombre}".center(150))
            print(f"Estado: {'Activo' if profesor_a_eliminar.active else 'Inactivo'}".center(150))

            # Solicitar confirmación al usuario
            confirmacion = input(f"{purple_color}\n¿Realmente desea eliminar este profesor? (s/n): {reset_color}")
            if confirmacion.lower() == 's':
                profesores.remove(profesor_a_eliminar)

                # Convertir los objetos Profesor de vuelta a diccionarios para guardarlos en el JSON
                data = [profesor.__dict__ for profesor in profesores]
                self.json_file.save(data)
                console.print(f"{green_color} El Profesor fue eliminado exitosamente. {reset_color}")
            else:
                console.print(f"{yellow_color} Eliminación cancelada. {reset_color}")
        else:
            console.print(f"{red_color} El Profesor no fue encontrado. {reset_color}")

        time.sleep(2)

    def consult(self):
        """Muestra la lista de profesores o busca uno específico."""
        borrarPantalla()

        console.print(Panel("[bold cyan] Consultar Profesores [/bold cyan]".center(150), border_style="green"))

        data = self.json_file.read()
        profesores = [Profesor(t['_cedula'], t['_nombre'], t.get('_active', True)) for t in data]

        if not profesores:
            console.print(f"{yellow_color}No hay profesores registrados.{reset_color}")
            return

        while True:
            print(f"{cyan_color}1. Listar todos los profesores".center(150))
            print("2. Buscar profesor por cédula".center(150)) 
            print(f"3. Volver {reset_color}".center(150)) 
            

            opcion = input(f"\n{red_color}Seleccione una opción: {reset_color}")

            if opcion == '1':
                borrarPantalla()
                for profesor in profesores:
                    print(f"Cédula: {profesor.cedula}, Nombre: {profesor.nombre}")  # Muestra otros atributos según sea necesario
            elif opcion == '2':
                while True:
                    borrarPantalla()
                    cedula = self.valida.cedula(f"{purple_color}Ingrese la cédula del profesor a buscar: {reset_color}", 0, 5)
                    if cedula is not None:
                        break

                profesor = next((p for p in profesores if p.cedula == cedula), None)
                if profesor:
                    print(f"Cédula: {profesor.cedula}, Nombre: {profesor.nombre}")  # Muestra otros atributos según sea necesario
                else:
                    console.print(f"{yellow_color} Profesor no encontrado. {reset_color}")
                    time.sleep(2)
            elif opcion == '3':
                break
            else:
                console.print(f"{red_color} Opción inválida. Intente de nuevo. {reset_color}")
                time.sleep(2)

#######################################################################################################

class CrudPeriodo(Icrud):
    def __init__(self):
        self.json_file = JsonFile(f'{path}/data/periods.json')
        self.valida = Valida()

    def create(self):
        """Crea un nuevo periodo académico y lo guarda en el archivo JSON."""
        borrarPantalla()
        console.print(Panel("[bold purple]Crear Periodo Académico[/bold purple]".center(150), border_style="green"))


        data = self.json_file.read()
        periodos = [Periodo(p['_id'], p['_periodo'], p['_active']) for p in data]

        if periodos:
            id = max([periodo._id for periodo in periodos]) + 1
        else:
            id = 1

        nombre_periodo = input(f"{purple_color}Ingrese el nombre del periodo académico: {reset_color}")
        while not nombre_periodo:
            console.print(f"{red_color}El nombre del periodo no puede estar vacío. Intente de nuevo.{reset_color}")
            nombre_periodo = input(f"{purple_color}Ingrese el nombre del periodo académico: {reset_color}")

        nuevo_periodo = Periodo(id, nombre_periodo, True)
        periodos.append(nuevo_periodo)

        # Convertir los objetos Periodo a diccionarios para guardarlos en el JSON
        data = [periodo.__dict__ for periodo in periodos]
        self.json_file.save(data)
        console.print(f"{green_color}El Periodo académico fue creado exitosamente.{reset_color}")
        time.sleep(2)

    def update(self):
        """Actualiza un periodo académico existente en el archivo JSON."""
        borrarPantalla()
        
        console.print(Panel("[bold purple]Actualizar Periodo Académico[/bold purple]", border_style="green"))

        data = self.json_file.read()
        periodos = [Periodo(p['_id'], p['_periodo'], p['_active']) for p in data]

        id = self.valida.solo_numeros("Ingrese el ID del periodo académico a actualizar: ", "ID inválido. Ingrese un número entero positivo.", 0, 5)
        periodo = next((p for p in periodos if p._id == int(id)), None)

        if periodo:
            nuevo_nombre = input(f"{purple_color}Ingrese el nuevo nombre del periodo académico (Enter para mantener '{periodo.periodo}'): {reset_color}")
            if nuevo_nombre:
                periodo._periodo = nuevo_nombre

            while True:
                nuevo_estado = input(f"{purple_color}Ingrese el nuevo estado del periodo (activo/inactivo) (actual: {'activo' if periodo._active else 'inactivo'}): {reset_color}")
                if nuevo_estado.lower() in ['activo', 'inactivo']:
                    if nuevo_estado.lower() == 'activo':
                        periodo.activar()
                    else:
                        periodo.desactivar()
                    break
                elif nuevo_estado == "":  # Mantener el estado original
                    break
                else:
                    mensaje = f"{red_color}' El Estado es inválido. Ingrese 'activo' o 'inactivo' o presione Enter para mantener el estado actual."
                    print(mensaje.center(80))


            # Convertir los objetos Periodo de vuelta a diccionarios para guardarlos en el JSON
            data = [periodo.__dict__ for periodo in periodos]
            self.json_file.save(data)
            console.print(f"{green_color}El Periodo académico fue actualizado exitosamente.{reset_color}")
            time.sleep(2)
        else:
            console.print(f"{yellow_color}El Periodo académico no fue encontrado.{reset_color}")
            time.sleep(2)

    def delete(self):
        """Elimina un periodo académico del archivo JSON."""
        borrarPantalla()

        console.print(Panel("[bold red]Eliminar Periodo Académico[/bold red]", border_style="green"))

        data = self.json_file.read()
        periodos = [Periodo(p['_id'], p['_periodo'], p['_active']) for p in data]

        id = self.valida.solo_numeros("Ingrese el ID del periodo académico a eliminar: ", "El ID es inválido. Ingrese un número entero positivo.", 0, 5)
        periodo_a_eliminar = next((p for p in periodos if p._id == int(id)), None)

        if periodo_a_eliminar:
            # Mostrar los detalles del periodo antes de eliminarlo
            print("\nDetalles del periodo a eliminar:")
            print(f"ID: {periodo_a_eliminar._id}".center(150))
            print(f"Nombre: {periodo_a_eliminar._periodo}".center(150))
            print(f"Estado: {'Activo' if periodo_a_eliminar._active else 'Inactivo'}".center(150))

            # Solicitar confirmación al usuario
            confirmacion = input(f"{purple_color}\n¿Realmente desea eliminar este periodo académico? (s/n): {reset_color}")
            if confirmacion.lower() == 's':
                periodos = [p for p in periodos if p._id != int(id)]
                data = [periodo.__dict__ for periodo in periodos]
                self.json_file.save(data)
                console.print(f"{green_color}El Periodo académico fue eliminado exitosamente.{reset_color}")
            else:
                console.print(f"{yellow_color}La Eliminación fue cancelada.{reset_color}")
        else:
            console.print(f"{red_color}El Periodo académico no a sido encontrado.{reset_color}")

        time.sleep(2)

    def consult(self):
        """Muestra la lista de periodos académicos o busca uno específico."""
        borrarPantalla()

        console.print(Panel("[bold cyan]Consultar Periodo Académico[/bold cyan]".center(150), border_style="green"))


        data = self.json_file.read()
        periodos = [Periodo(p['_id'], p['_periodo'], p['_active']) for p in data]

        if not periodos:
            console.print(f"{yellow_color}No hay periodos académicos registrados.{reset_color}")
            return

        while True:

            print(f"{cyan_color}1. Listar todos los periodos académicos".center(150))
            print("2. Buscar periodo académico por ID".center(150))
            print(f"3. Volver {reset_color}".center(150))

            opcion = input(f"{red_color}Seleccione una opción: {reset_color}")

            if opcion == '1':
                borrarPantalla()
                for periodo in periodos:
                    print(f"ID: {periodo._id}, Periodo: {periodo._periodo}, Estado: {'Activo' if periodo._active else 'Inactivo'}")
            elif opcion == '2':
                borrarPantalla()
                id = self.valida.solo_numeros(f"{purple_color}Ingrese el ID del periodo académico a buscar: {reset_color}", f"{red_color}El ID es inválido. Ingrese un número entero positivo.{reset_color}", 0, 5)
                periodo = next((p for p in periodos if p._id == int(id)), None)
                if periodo:
                    print(f"ID: {periodo._id}, Periodo: {periodo._periodo}, Estado: {'Activo' if periodo._active else 'Inactivo'}")
                else:
                    print(f"{yellow_color}{' El Periodo académico no fue encontrado. '.center(80)}{reset_color}")
            elif opcion == '3':
                break
            else:
                print(f"{red_color}{' Opción inválida. Intente de nuevo. '.center(80)}{reset_color}")

#########################################################################################################

class CrudLevel(Icrud):
    def __init__(self):
        self.json_file = JsonFile(f'{path}/data/levels.json')
        self.valida = Valida()

        self.niveles_predefinidos = [
            "Primer Semestre",
            "Segundo Semestre",
            "Tercero Semestre",
            "Cuarto Semestre",
            "Quinto Semestre",
            "Sexto Semestre",
            "Séptimo Semestre",
            "Octavo Semestre",
        ]

    def create(self):
        """Crea un nuevo nivel educativo y lo guarda en el archivo JSON."""
        borrarPantalla()
        
        console.print(Panel("[bold purple]Crear Nivel Educativo[/bold purple]".center(150), border_style="green"))

        data = self.json_file.read()
        niveles = [Nivel(n['_id'], n['_nivel']) for n in data]

        if niveles:
            id = max([nivel._id for nivel in niveles]) + 1
        else:
            id = 1

        # Preguntar al usuario si desea crear un nuevo nivel predefinido
        while True:
            crear_nuevo = input(f"{purple_color}¿Desea crear un nuevo nivel predefinido? (s/n): {reset_color}")
            if crear_nuevo.lower() in ['s', 'n']:
                break
            else:
                print(f"{red_color}Opción inválida. Ingrese 's' o 'n'.{reset_color}")

        if crear_nuevo.lower() == 's':
            # Crear un nuevo nivel predefinido
            nombre_nivel = self.valida.solo_letras(f"{purple_color}Ingrese el nombre del nuevo nivel educativo: {reset_color}", f"{red_color}Nombre inválido. Solo se permiten letras.{reset_color}")
            self.niveles_predefinidos.append(nombre_nivel)

        # Mostrar niveles predefinidos (incluyendo el nuevo si se creó)
        print(f"{purple_color}\nNiveles educativos predefinidos:{reset_color}")
        for i, nivel_predefinido in enumerate(self.niveles_predefinidos):
            print(f"{cyan_color}{i+1}. {nivel_predefinido}{reset_color}")

        # Solicitar al usuario que elija un nivel predefinido
        while True:
            opcion = self.valida.solo_numeros(f"{purple_color}Seleccione el número del nivel educativo: {reset_color}",
                                              f"{red_color}Opción inválida. Ingrese un número entero positivo. {reset_color}", 0, 5)
            if 1 <= int(opcion) <= len(self.niveles_predefinidos):
                nombre_nivel = self.niveles_predefinidos[int(opcion) - 1]
                break
            else:
                console.print(f"{red_color}La Opción esta fuera de rango. Intente de nuevo.{reset_color}")

        nuevo_nivel = Nivel(id, nombre_nivel)
        niveles.append(nuevo_nivel)

        # Convertir los objetos Nivel de vuelta a diccionarios para guardarlos en el JSON
        data = [nivel.__dict__ for nivel in niveles]
        self.json_file.save(data)
        console.print(f"{green_color}Nivel educativo creado exitosamente.{reset_color}")
        time.sleep(2)


    def update(self):
        """Actualiza un nivel educativo existente en el archivo JSON."""
        borrarPantalla()
        linea(80, green_color)
        print(f"{purple_color}{' Actualizar Nivel Educativo '.center(80)}{reset_color}")
        linea(80, green_color)

        data = self.json_file.read()
        niveles = [Nivel(n['_id'], n['_nivel']) for n in data] 

        id = self.valida.solo_numeros("Ingrese el ID del nivel educativo a actualizar: ", "ID inválido. Ingrese un número entero positivo.", 0, 5)
        nivel = next((n for n in niveles if n.id == int(id)), None)

        if nivel:
            nivel._nivel = self.valida.solo_letras("Ingrese el nuevo nombre del nivel educativo: ", "Nombre inválido. Solo se permiten letras.")

            while True:
                nuevo_estado = input(f"{purple_color}Ingrese el nuevo estado del nivel (activo/inactivo) (actual: {'activo' if nivel.active else 'inactivo'}): {reset_color}")
                if nuevo_estado.lower() in ['activo', 'inactivo']:
                    if nuevo_estado.lower() == 'activo':
                        nivel.activar() 
                    else:
                        nivel.desactivar() 
                    break
                else:
                    mensaje = f"{purple_color} Estado inválido. Ingrese 'activo' o 'inactivo'. {reset_color}"
                    print(mensaje.center(80)) 
                    

            data = [nivel.__dict__ for nivel in niveles]
            self.json_file.save(data)
            console.print(f"{green_color}El Nivel educativo fue actualizado exitosamente.{reset_color}")
            time.sleep(2)
        else:
            console.print(f"{red_color}El Nivel educativo no fue encontrado.{reset_color}")
            time.sleep(2)
        

    def delete(self):
        """Elimina un nivel educativo del archivo JSON."""
        borrarPantalla()
        
        console.print(Panel("[bold red]Eliminar Nivel Educativo[/bold red]".center(150), border_style="green"))

        data = self.json_file.read()
        niveles = [Nivel(n['_id'], n['_nivel']) for n in data]

        id = self.valida.solo_numeros(f"{purple_color}Ingrese el ID del nivel educativo a eliminar: {reset_color}", f"{red_color}El ID es inválido. Ingrese un número entero positivo.{reset_color}", 0, 5)
        nivel_a_eliminar = next((n for n in niveles if n.id == int(id)), None)

        if nivel_a_eliminar:
            # Mostrar los detalles del nivel antes de eliminarlo
            print("\nDetalles del nivel a eliminar:".center(150))
            print(f"ID: {nivel_a_eliminar.id}".center(150))
            print(f"Nombre: {nivel_a_eliminar.nivel}".center(150))
            print(f"Estado: {'Activo' if nivel_a_eliminar.active else 'Inactivo'}".center(150))

            # Solicitar confirmación al usuario
            confirmacion = input(f"{purple_color}\n¿Realmente desea eliminar este nivel educativo? (s/n): {reset_color}")
            if confirmacion.lower() == 's':
                niveles = [n for n in niveles if n.id != int(id)]
                data = [nivel.__dict__ for nivel in niveles]
                self.json_file.save(data)
                console.print(f"{green_color}El Nivel educativo fue eliminado exitosamente.{reset_color}")
            else:
                console.print(f"{yellow_color}La Eliminación fue cancelada.{reset_color}")
        else:
            console.print(f"{red_color}El Nivel educativo no fue encontrado.{reset_color}")

        time.sleep(2)

    def consult(self):
        """Muestra la lista de niveles educativos o busca uno específico."""
        borrarPantalla()
        console.print(Panel("[bold cyan]Consultar Nivel Educativo[/bold cyan]", border_style="green"))

        data = self.json_file.read()
        niveles = [Nivel(n['_id'], n['_nivel']) for n in data]

        if not niveles:
            console.print(f"{red_color}No hay niveles educativos registrados.{reset_color}")
            return

        while True:
            print(f"{cyan_color}1. Listar todos los niveles educativos".center(150))
            print("2. Buscar nivel educativo por ID".center(150))
            print(f"3. Volver{reset_color}".center(150))

            opcion = input(f"{red_color}Seleccione una opción: {reset_color}")

            if opcion == '1':
                borrarPantalla()
                for nivel in niveles:
                    print(f"ID: {nivel._id}, Nombre: {nivel._nivel}, Estado: {'Activo' if nivel._active else 'Inactivo'}")
                    time.sleep(3)
            elif opcion == '2':
                borrarPantalla()
                id = self.valida.solo_numeros(f"{purple_color}Ingrese el ID del nivel educativo a buscar: {reset_color}", f"{red_color}ID inválido. Ingrese un número entero positivo. {reset_color}", 0, 5)
                nivel = next((n for n in niveles if n._id == int(id)), None)
                if nivel:
                    borrarPantalla()
                    print(f"ID: {nivel._id}, Nombre: {nivel._nivel}, Estado: {'Activo' if nivel._active else 'Inactivo'}")
                    time.sleep(3)
                else:
                    console.print(f"{red_color}El Nivel educativo no fue encontrado.{reset_color}")
            elif opcion == '3':
                break
            else:
                console.print(f"{red_color}La Opción esinválida. Intente de nuevo.{reset_color}")