
from collections import OrderedDict, Counter
import itertools
from modelo.Evaluador import EvaluadorSiguiente
from copy import copy


class GramaticaInvalida(Exception):

    def __init__(self, mensaje, libreContexto):

        super().__init__(mensaje)
        self.libreContexto = libreContexto


class Gramatica:
    """
       encargada de realizar la distinción de los
       diferentes procesos que hay en las gramáticas
       """
    def __init__(self, producciones=None, inicio=None, lambdaP='λ', dolar='$'):

        self.producciones = producciones if producciones else OrderedDict()
        # print("Produ ", self.producciones)
        self.inicio = inicio
        self.lambdaP = lambdaP
        self.dolarSiguiente = dolar

    @property  # Obtiene los no terminales de la gramatica
    def noTerminales(self):
        # print("Produ ", self.producciones)
        return self.producciones.keys()

    @property # Revisa los no terminales de la gramatica
    def terminales(self):

        noTerminales = self.noTerminales
        terminales = OrderedDict()   # Ordered mantiene la posicion de la clave por más que se cambie la posicion
        for i in self.listaProducciones():
            for simbolo in i.cuerpo:
                if simbolo not in noTerminales:   # Si no esta lo añade
                    terminales.update({simbolo: 1})
        return terminales.keys()

    def listaProducciones(self):
        """
               Método encargado de listar las producciones en un solo iterador
               """ # ['ABC', 'DEF'] --> A B C D E F
        return itertools.chain.from_iterable(self.producciones.values())

    def agregarRegla(self, regla):
        try:
            produccionesActuales = self.producciones[regla.encabezado] # valores del dic producciones
            if regla not in produccionesActuales:
                produccionesActuales.append(regla)
        except KeyError:
            self.producciones[regla.encabezado] = [regla]

    def eliminarRegla(self, regla):
        self.producciones[regla.encabezado].remove(regla)

    def esTerminal(self, termino):

        """
               Método encargado de evaluar si el termino que se le pasa como
               parámetro es un terminal
               """

        return termino not in self.noTerminales

    """
            Método encargado de inicializar el inicio de la gramática como 
            simbolo inicial
            """
    def esSimboloInicial(self, simbolo):

        return self.inicio == simbolo

    """
            Método encargado de retornar las gramáticas asociadas a un no terminal
            """
    def obtenerProducciones(self, termino):

        return [i.cuerpo for i in self.producciones[termino]]

    def primeros(self, termino):

        listaPrimeros = set()
        if isinstance(termino, tuple): # chequea que el termino sea una tupla
            # print("P", termino)
            listaPrimeros = self.conjuntoPrimeros(termino)
        elif self.esTerminal(termino): # chequea que es un terminal
            listaPrimeros = {termino}
        else:
            for i in self.obtenerProducciones(termino):
                listaPrimeros = listaPrimeros.union(self.primeros(i))
        return sorted(listaPrimeros)

    def conjuntoPrimeros(self, listaSimbolos):
        listaPrimeros = set()
        for i in listaSimbolos:
            prim = self.primeros(i)
            listaPrimeros = listaPrimeros.union(prim)
            #print("P ", listaPrimeros)
            if self.lambdaP not in prim:
                break
        return listaPrimeros

    def siguientes(self, noTerminal, anterior=EvaluadorSiguiente()):

        anterior += (noTerminal,)

        listaSiguientes = set()
        if self.esSimboloInicial(noTerminal):
            listaSiguientes.add(self.dolarSiguiente) # Agrega $

        subConjuntos = set()
        for i in self.listaProducciones():
            if noTerminal in i.cuerpo:
                posicion = i.cuerpo.index(noTerminal)
                b = i.cuerpo[posicion + 1:] # Recorre desde esa posicion hasta el final
                if b:
                    listaSiguientes = listaSiguientes.union(set(self.conjuntoPrimeros(b)) - {self.lambdaP})

                if not b:   # none   Encontró terminal
                    subConjuntos.add(i.encabezado)
                
                elif b and self.lambdaP in self.conjuntoPrimeros(b):
                    subConjuntos.add(i.encabezado)

        subConjuntos = subConjuntos - {noTerminal}  # quita repetido

        for j in subConjuntos:
            if j not in anterior:
                listaSiguientes = listaSiguientes.union(self.siguientes(j, anterior))
        
        return sorted(listaSiguientes)
    
    def conjuntoPrediccion(self, noTerminal, produccion):

        lst = produccion.split() # separa producciones
        # lst[0] = primer termino de la produccion
        if self.esTerminal(lst[0]) and lst[0] != self.lambdaP:
            tmp= [lst[0]]
            return tmp
        elif lst[0] == self.lambdaP:
            return self.siguientes(noTerminal.strip())  # strip quita los espacios
        else:
            return self.primeros(lst[0])
        
    def hayInterseccion(self, lst):
        # Mirar si existe intersección para definir si es gramárica LL1
        
        temp = Counter(lst)  # cuenta cuantas veces esta
        for i in range(len(lst)):
            if (temp[lst[i]] > 1):   # si esta más que uno
                return True
        return False

    def produccionesXTermino(self, termino):

        produccion = [' '.join(i.cuerpo) for i in self.producciones[termino]]  # une cada elemento
        return produccion

    def __str__(self):
        cadenaProducciones = []
        for i in self.noTerminales:
            cuerpos = [' '.join(j.cuerpo) for j in self.producciones[i]]
            cadenaProducciones.append("{} -> {}".format(i, ' | '.join(cuerpos)))

        return '\n'.join(cadenaProducciones)

    def __repr__(self):
        return '\n'.join([str(i) for i in self.obtenerProducciones()])

    def __eq__(self, otro):
        return hash(self) == hash(otro)

    def __hash__(self):
        cadenas = tuple(sorted([str(i) for i in self.obtenerProducciones()]))
        return hash(cadenas)

    def __copy__(self):
        gramatica = Gramatica(inicio=self.inicio, lambdaP=self.lambdaP, dolar=self.dolarSiguiente)
        for a, b in self.producciones.items():
            gramatica.producciones[a] = copy(b)

        return gramatica
