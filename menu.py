from utilities import green_color, blue_color, purple_color, reset_color, red_color, borrarPantalla, linea, gotoxy, cyan_color
from Icrud import Icrud
from Cruds import CrudStudents,CrudTeacher,CrudLevel,CrudSubjects,CrudGrades,CrudPeriodo
from clsJson import JsonFile
from datetime import date
from components import Valida, Menu
import datetime
import os
import time
import platform
from rich.panel import Panel
from rich.console import Console

# Crear la consola rich
console = Console()

def borrarPantalla():
    console.clear()

opc = ''
while opc != '7':
    borrarPantalla()

    # Mostrar el menú principal con rich Panel
    console.print(Panel("[bold cyan]📚 SISTEMA DE GESTIÓN ACADÉMICA 📚[/bold cyan]", title="[bold yellow]Menú Principal[/bold yellow]", border_style="blue"), justify="center")

    # Opciones del menú principal
    menu_main_options = [
        "[bold green]1) Estudiantes 👨‍🎓[/bold green]",
        "[bold green]2) Profesores 👩‍🏫[/bold green]",
        "[bold green]3) Asignaturas 📘[/bold green]",
        "[bold green]4) Niveles 🏫[/bold green]",
        "[bold green]5) Periodos 📅[/bold green]",
        "[bold green]6) Notas 📝[/bold green]",
        "[bold green]7) Salir 🛫[/bold green]"
    ]
    
    # Mostrar las opciones del menú principal
    for option in menu_main_options:
        console.print(option, justify="center")
    
    # Leer la opción seleccionada
    opc = console.input("\n[bold yellow]Seleccione una opción: [/bold yellow]")

    # Submenú de Estudiantes
    if opc == '1':
        opc1 = ''
        while opc1 != '5':
            borrarPantalla()
            # Encabezado del submenú de estudiantes
            console.print(Panel("[bold magenta]🎓 MENÚ ESTUDIANTES 🎓[/bold magenta]", title="[bold yellow]Estudiantes[/bold yellow]", border_style="magenta"), justify="center")

            # Opciones del submenú de estudiantes
            student_menu_options = [
                "[bold green]1) Crear 🗿[/bold green]",
                "[bold green]2) Actualizar 📣[/bold green]",
                "[bold green]3) Eliminar 🗑️[/bold green]",
                "[bold green]4) Consultar 🔍[/bold green]",
                "[bold green]5) Volver 🛫[/bold green]"
            ]

            for option in student_menu_options:
                console.print(option, justify="center")

            opc1 = console.input("\n[bold yellow]Seleccione una opción: [/bold yellow]")

            crud = CrudStudents()
            if opc1 == '1':
                crud.create()
            elif opc1 == '2':
                crud.update()
            elif opc1 == '3':
                crud.delete()
            elif opc1 == '4':
                crud.consult()
            console.print("[bold cyan]Regresando al menú principal...[/bold cyan]", justify="center")

    # Submenú de Profesores
    elif opc == '2':
        opc2 = ''
        while opc2 != '5':
            borrarPantalla()
            # Encabezado del submenú de profesores
            console.print(Panel("[bold magenta]🧑‍🏫 MENÚ PROFESORES 🧑‍🏫[/bold magenta]", title="[bold yellow]Profesores[/bold yellow]", border_style="magenta"), justify="center")

            # Opciones del submenú de profesores
            teacher_menu_options = [
                "[bold green]1) Crear 🗿[/bold green]",
                "[bold green]2) Actualizar 📣[/bold green]",
                "[bold green]3) Eliminar 🗑️[/bold green]",
                "[bold green]4) Consultar 🔍[/bold green]",
                "[bold green]5) Volver 🛫[/bold green]"
            ]

            for option in teacher_menu_options:
                console.print(option, justify="center")

            opc2 = console.input("\n[bold yellow]Seleccione una opción: [/bold yellow]")

            crud = CrudTeacher()
            if opc2 == '1':
                crud.create()
            elif opc2 == '2':
                crud.update()
            elif opc2 == '3':
                crud.delete()
            elif opc2 == '4':
                crud.consult()
            console.print("[bold cyan]Regresando al menú principal...[/bold cyan]", justify="center")

    # Submenú de Asignaturas
    elif opc == '3':
        opc3 = ''
        while opc3 != '5':
            borrarPantalla()
            # Encabezado del submenú de asignaturas
            console.print(Panel("[bold blue]📘 MENÚ ASIGNATURAS 📘[/bold blue]", title="[bold yellow]Asignaturas[/bold yellow]", border_style="blue"), justify="center")

            # Opciones del submenú de asignaturas
            subject_menu_options = [
                "[bold green]1) Crear 🗿[/bold green]",
                "[bold green]2) Actualizar 📣[/bold green]",
                "[bold green]3) Eliminar 🗑️[/bold green]",
                "[bold green]4) Consultar 🔍[/bold green]",
                "[bold green]5) Volver 🛫[/bold green]"
            ]

            for option in subject_menu_options:
                console.print(option, justify="center")

            opc3 = console.input("\n[bold yellow]Seleccione una opción: [/bold yellow]")

            crud = CrudSubjects()
            if opc3 == '1':
                crud.create()
            elif opc3 == '2':
                crud.update()
            elif opc3 == '3':
                crud.delete()
            elif opc3 == '4':
                crud.consult()
            console.print("[bold cyan]Regresando al menú principal...[/bold cyan]", justify="center")

    # Submenú de Niveles
    elif opc == '4':
        opc4 = ''
        while opc4 != '5':
            borrarPantalla()
            # Encabezado del submenú de niveles
            console.print(Panel("[bold purple]🏫 MENÚ NIVELES 🏫[/bold purple]", title="[bold yellow]Niveles[/bold yellow]", border_style="purple"), justify="center")

            # Opciones del submenú de niveles
            level_menu_options = [
                "[bold green]1) Crear 🗿[/bold green]",
                "[bold green]2) Actualizar 📣[/bold green]",
                "[bold green]3) Eliminar 🗑️[/bold green]",
                "[bold green]4) Consultar 🔍[/bold green]",
                "[bold green]5) Volver 🛫[/bold green]"
            ]

            for option in level_menu_options:
                console.print(option, justify="center")

            opc4 = console.input("\n[bold yellow]Seleccione una opción: [/bold yellow]")

            crud = CrudLevel()
            if opc4 == '1':
                crud.create()
            elif opc4 == '2':
                crud.update()
            elif opc4 == '3':
                crud.delete()
            elif opc4 == '4':
                crud.consult()
            console.print("[bold cyan]Regresando al menú principal...[/bold cyan]", justify="center")

    # Submenú de Periodos
    elif opc == '5':
        opc5 = ''
        while opc5 != '5':
            borrarPantalla()
            # Encabezado del submenú de periodos
            console.print(Panel("[bold cyan]📅 MENÚ PERIODOS 📅[/bold cyan]", title="[bold yellow]Periodos[/bold yellow]", border_style="cyan"), justify="center")

            # Opciones del submenú de periodos
            period_menu_options = [
                "[bold green]1) Crear 🗿[/bold green]",
                "[bold green]2) Actualizar 📣[/bold green]",
                "[bold green]3) Eliminar 🗑️[/bold green]",
                "[bold green]4) Consultar 🔍[/bold green]",
                "[bold green]5) Volver 🛫[/bold green]"
            ]

            for option in period_menu_options:
                console.print(option, justify="center")

            opc5 = console.input("\n[bold yellow]Seleccione una opción: [/bold yellow]")

            crud = CrudPeriodo()
            if opc5 == '1':
                crud.create()
            elif opc5 == '2':
                crud.update()
            elif opc5 == '3':
                crud.delete()
            elif opc5 == '4':
                crud.consult()
            console.print("[bold cyan]Regresando al menú principal...[/bold cyan]", justify="center")

    # Submenú de Notas
    elif opc == '6':
        opc6 = ''
        while opc6 != '5':
            borrarPantalla()
            # Encabezado del submenú de notas
            console.print(Panel("[bold green]📝 MENÚ NOTAS 📝[/bold green]", title="[bold yellow]Notas[/bold yellow]", border_style="green"), justify="center")

            # Opciones del submenú de notas
            grades_menu_options = [
                "[bold green]1) Crear 🗿[/bold green]",
                "[bold green]2) Actualizar 📣[/bold green]",
                "[bold green]3) Eliminar 🗑️[/bold green]",
                "[bold green]4) Consultar 🔍[/bold green]",
                "[bold green]5) Volver 🛫[/bold green]"
            ]

            for option in grades_menu_options:
                console.print(option, justify="center")

            opc6 = console.input("\n[bold yellow]Seleccione una opción: [/bold yellow]")

            crud = CrudGrades()
            if opc6 == '1':
                crud.create()
            elif opc6 == '2':
                crud.update()
            elif opc6 == '3':
                crud.delete()
            elif opc6 == '4':
                crud.consult()
            console.print("[bold cyan]Regresando al menú principal...[/bold cyan]", justify="center")

    # Opción para salir
    elif opc == '7':
        break

borrarPantalla()
input("Presione una tecla para salir...")
borrarPantalla()