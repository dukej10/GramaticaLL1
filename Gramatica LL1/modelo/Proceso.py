

from collections import OrderedDict
from copy import copy
from modelo.Regla import Regla
from modelo.Gramatica import Gramatica, GramaticaInvalida


def convertirLibreContexto(texto, lambdaP='λ', dolarSiguiente='$'):
    """
        Método que convierte o evalua la gramática en libre contexto, si esto
        no se cumple retorna un mensaje de gramática inválida
        """
    try:
        producciones = [i for i in texto.strip().split('\n') if not i.startswith('#')]
        inicio = producciones[0].split('->')[0].strip()  # First rule as starting symbol
        gramatica = Gramatica(inicio=inicio, lambdaP=lambdaP, dolar=dolarSiguiente)

        for j in producciones:
            encabezado, cuerpo = [k.strip() for k in j.split('->')] # separar
            producciones = [p.strip() for p in cuerpo.split('|')] # separa cada produccion
            produccionesTokenizadas = [tuple(i.split()) for i in producciones]  # [('id', ':=', 'P')]
            for h in produccionesTokenizadas:
                gramatica.agregarRegla(Regla(encabezado, h))

        return gramatica
    except ValueError:
        raise GramaticaInvalida("Gramática inválida", texto)


def __normalizarProducciones(gramatica): 

    # Eliminar símbolos vacíos de producciones
    
    gramaticaNormalizada = copy(gramatica)

    for i in gramatica.noTerminales:
        for j in gramatica.producciones[i]:
            # print("x ", j.cuerpo)
            if len(j.cuerpo) > 1:
                j.cuerpo = tuple([k for k in j.cuerpo if i != gramatica.lambdaP])

    return gramaticaNormalizada


def ordenarNoTerminales(gramatica):

    # Ordenar los no terminales de la gramática
    return [i for i in gramatica.noTerminales]


# Nuevo simbolo para quitar recursion
def __generarLlave(gramatica, termino):
    # print(termino)
    nuevoTermino = termino
    while nuevoTermino in gramatica.noTerminales:
        nuevoTermino += "'"

    return nuevoTermino


def eliminarRecursionIzquierdaInmediataXProduccion(gramatica, noTerminal):

    producciones = gramatica.producciones[noTerminal]
    recursion = []
    noRecursivo = []
    nuevasProducciones = []

    for i in producciones:
        if i.esRecursionIzquierda():
            recursion.append(i.cuerpo)
        else:
            noRecursivo.append(i.cuerpo)

    if not recursion:
        return producciones

    nuevoNoTerminal = __generarLlave(gramatica, noTerminal)
    for b in noRecursivo:
        # print("no " + b)
        # A -> b1 A' | ... | bn A'
        nuevasProducciones.append(Regla(noTerminal, b + (nuevoNoTerminal,)))

    for a in recursion:
        # A' -> a1 A' | a2 A' | ... | am A'
        nuevasProducciones.append(Regla(nuevoNoTerminal, a[1:] + (nuevoNoTerminal,)))

    # A' -> ε
    nuevasProducciones.append(Regla(nuevoNoTerminal, (gramatica.lambdaP,)))

    return nuevasProducciones


def eliminarRecursionIzquierda(gramatica):

    gramaticaTemporal = copy(gramatica)
    nuevaGramatica = Gramatica(inicio=gramaticaTemporal.inicio, lambdaP=gramaticaTemporal.lambdaP, dolar=gramaticaTemporal.dolarSiguiente)
    noTerminales = ordenarNoTerminales(gramaticaTemporal)
    """print()
    print(gramaticaTemporal)
    print(noTerminales) """
    for i in range(0, len(noTerminales)):
        subIndiceI = noTerminales[i]
        for j in range(0, i):
            subIndiceJ = noTerminales[j]
            for pSubIndiceI in gramaticaTemporal.producciones[subIndiceI]:
                if pSubIndiceI.cuerpo and subIndiceJ == pSubIndiceI.cuerpo[0]:
                    reemplazarProducciones = [Regla(subIndiceI, pSubIndiceJ.cuerpo + pSubIndiceI.cuerpo[1:]) for pSubIndiceJ in
                                            gramaticaTemporal.producciones[subIndiceJ]]
                    pudoEliminarProducciones = any(map(lambda x: x.esRecursionIzquierda(), reemplazarProducciones))
                    if pudoEliminarProducciones:
                        gramaticaTemporal.eliminarRegla(pSubIndiceI)
                        for p in reemplazarProducciones:
                            gramaticaTemporal.agregarRegla(p)

        nuevasProducciones = eliminarRecursionIzquierdaInmediataXProduccion(gramaticaTemporal, subIndiceI)
        for p in nuevasProducciones:
            nuevaGramatica.agregarRegla(p)

    return __normalizarProducciones(nuevaGramatica)


def comprobarIgualdad(lista):

    return lista[1:] == lista[:-1]


def obtenerLongitudMaxima(lista):
    
    return max([len(l) for l in lista])


def obtenerPrefijos(producciones):

    usual = OrderedDict()
    ordenarProducciones = sorted(producciones)
    for x in ordenarProducciones:
        if x:
            usual.setdefault(x[0], []).append(x)
    for i, j in usual.items():
        indiceUsual = 0
        if (len(j) > 1):
            indiceUsual = 1
            subLista = [l[0:indiceUsual + 1] for l in j]
            while comprobarIgualdad(subLista) and indiceUsual < obtenerLongitudMaxima(j):
                indiceUsual += 1
                subLista = [l[0:indiceUsual + 1] for l in j]
            indiceUsual = indiceUsual - 1
            usual[i] = [l[indiceUsual + 1:] for l in j]
        if indiceUsual > 0:
            usual[i] = [l[indiceUsual + 1:] for l in j]
            llaveFinal = ' '.join(j[0][0:indiceUsual + 1])
            usual[llaveFinal] = usual[i]
            del usual[i]

    return usual


def comprobarFactoresIzquierdos(gramatica):
    
    for noTerminal in gramatica.noTerminales:
        producciones = gramatica.obtenerProducciones(noTerminal)
        if len(producciones) > 1:
            elementosIniciales = [l[0] for l in producciones if l]
            #resultado = comprobarIgualdad(elementosIniciales)
            valoresDiferentes = set(elementosIniciales)
            for i in valoresDiferentes:
                if elementosIniciales.count(i) > 1:
                    return True
    return False


def eliminarFactorizacionIzquierda(gramatica):

    
    gramat = gramatica
    print("oe ", type(gramat))
    while (comprobarFactoresIzquierdos(gramat)):
        gramat = __eliminarFactorizacionIzquierda(gramat)
    return gramat


def __eliminarFactorizacionIzquierda(gramatica):

    nuevaGramatica = Gramatica(inicio=gramatica.inicio, lambdaP=gramatica.lambdaP, dolar=gramatica.dolarSiguiente)

    nuevasProducciones = []

    for noTerminal in gramatica.noTerminales:

        producciones = gramatica.obtenerProducciones(noTerminal)
        if len(producciones) > 1:
            prefijos = obtenerPrefijos(producciones)
            for prefijo, i in prefijos.items():
                if (len(i) == 1):
                    nuevasProducciones.append(Regla(noTerminal, tuple(i[0])))
                    continue
                nuevaLlave = __generarLlave(gramatica, noTerminal)
                cuerpo = [prefijo] + [nuevaLlave]
                nuevasProducciones.append(Regla(noTerminal, tuple(cuerpo)))
                for prod in i:
                    if not prod:
                        nuevasProducciones.append(Regla(nuevaLlave, tuple([gramatica.lambdaP])))
                    else:
                        nuevasProducciones.append(Regla(nuevaLlave, tuple(prod)))
        else:
            nuevasProducciones.append(Regla(noTerminal, tuple(producciones[0])))

    for produccion in nuevasProducciones:
        nuevaGramatica.agregarRegla(produccion)
    return __normalizarProducciones(nuevaGramatica)
