from utilities import borrarPantalla, gotoxy
from utilities import blue_color, purple_color, reset_color, red_color, green_color, linea
import time


class Menu:
    def __init__(self,titulo="",opciones=[],col=6,fil=1):
        self.titulo=titulo
        self.opciones=opciones
        self.col=col
        self.fil=fil
        
    def menu(self):
        linea(80,green_color); print(f'{purple_color}{self.titulo}{reset_color}'.center(80)); linea(80,green_color)
        self.col-=5
        for opcion in self.opciones:
            self.fil +=1
            print(opcion)
        linea(80,green_color)
        opc = input(f"{red_color}Elija opcion[1...{len(self.opciones)}]: {reset_color}") 
        linea(80,green_color)

        return opc   

class Valida:
    def solo_numeros(self,mensaje, mensajeError,col,fil):
        while True:            
            valor = input(f'          ------>   | {purple_color}{mensaje}{reset_color}')
            try:
                if int(valor) > 0:
                    break
            except:
                gotoxy(col,fil);print(f'{red_color}{mensajeError}{reset_color}')
                time.sleep(1)
                gotoxy(col,fil);print(""*20)
        return valor

    def solo_letras(self, mensaje, mensajeError):
        while True:
            valor = str(input(f"          ------>   | {mensaje} "))
            if all(c.isalpha() or c.isspace() or c.isdigit() or c in "-_" for c in valor):
                break
            else:
                gotoxy(60, 0)
                print(f"          ------>   | {mensajeError} ")
                time.sleep(1)
                gotoxy(60, 0)
                print(" " * 60)
        return valor
    
    def solo_decimales(self,mensaje,mensajeError):
        while True:
            valor = str(input(purple_color + "          ------>   | {} ".format(mensaje) + reset_color))
            try:
                valor = float(valor)
                if valor > float(0):
                    break
            except:
                print("          ------>   | {} ".format(mensajeError))
                time.sleep(1)
        return valor
    
    def cedula(self, mensaje, col1, fil1):
        while True:
            cedula = input(f'          ------>   | {mensaje}')
            
            if len(cedula) == 10 and cedula.isdigit():
                coeficientes = [2, 1, 2, 1, 2, 1, 2, 1, 2]
                suma = 0
                
                for i in range(9):
                    digito = int(cedula[i]) * coeficientes[i]
                    if digito > 9:
                        digito -= 9
                    suma += digito
                
                total = suma % 10
                if total != 0:
                    total = 10 - total
                
                
                if total == int(cedula[9]):
                    return cedula
                
            gotoxy(col1 + 60, fil1 - 1);
            print(red_color + "El formato del DNI es incorrecto." + reset_color)
            time.sleep(1)
            gotoxy(col1 + 60, fil1 - 1)  # Volver a la misma posición
            print(" " * len("El formato del DNI es incorrecto."))  # Borrar el mensaje

    def valida_nota(self, mensaje, mensaje_error):
        while True:
            try:
                nota = float(input(f"          ------>   | {purple_color}{mensaje}{reset_color} "))
                if 0 <= nota <= 50:
                    return nota
                else:
                    print(f"          ------>   | {red_color}{mensaje_error}{reset_color} ")
                    time.sleep(1)
            except ValueError:
                print(f"          ------>   | {red_color}Error: Ingrese un número decimal válido.{reset_color} ")
                time.sleep(1)
            
            

    
class otra:
    pass    

if __name__ == '__main__':
    # instanciar el menu
    opciones_menu = ["1. Entero", "2. Letra", "3. Decimal"]
    menu = Menu(titulo="-- Mi Menú --", opciones=opciones_menu, col=10, fil=5)
    # llamada al menu
    opcion_elegida = menu.menu()
    print("Opción escogida:", opcion_elegida)
    valida = Valida()
    if(opciones_menu==1):
      numero_validado = valida.solo_numeros("Mensaje de error", 10, 10)
      print("Número validado:", numero_validado)
    
    numero_validado = valida.solo_numeros("Mensaje de error", 10, 10)
    print("Número validado:", numero_validado)
    
    letra_validada = valida.solo_letras("Ingrese una letra:", "Mensaje de error")
    print("Letra validada:", letra_validada)
    
    decimal_validado = valida.solo_decimales("Ingrese un decimal:", "Mensaje de error")
    print("Decimal validado:", decimal_validado)