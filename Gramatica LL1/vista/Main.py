
from vista.GUI import VentanaGramatica
from Info.lector import JSON


def main():

    json = JSON()
    datos = json.read()
    #print(datos[0])
    ventana = VentanaGramatica(datos)


main()
