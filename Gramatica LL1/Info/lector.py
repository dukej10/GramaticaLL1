import json
import os


class JSON:
    def __init__(self):
        self.file = ""
        self.datos = {}
        self.datosf = []

    def read(self):
        data = {}
        if os.name == "posix":
            file = "Info/gramaticas.json"
        else:
            file = "C:\\Users\\Juandi Duque\\Documents\\LENGUAJES\\Gramatica LL1\\Recursos\\gramaticas.json"

        with open(file) as jfile:
            self.datos = json.load(jfile)
        #print(self.datos)
        #print(self.datos['gramaticas'][0])
        longitudes = [len(v) for v in self.datos.values()]
        for i in range(longitudes[0]):
            self.datosf.append(self.datos['gramaticas'][i]['producciones'])
        # Para poner el simbolo lambda
        for i in range(len(self.datosf)): # Cuando se carga el archivo en vez de λ se puso otro símbolo
            if "Î»" in self.datosf[i]:
                self.datosf[i] = self.datosf[i].replace("Î»", "λ") # Reemplaza el símbolo por el correspondiente
        # print(len(self.datosf[0]))
        return self.datosf

