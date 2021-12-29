

class ProduccionInvalida(Exception): 

    def __init__(self, mensaje, produccion):
        super().__init__(mensaje)
        self.produccion = produccion


class Regla:
    """
        Identifica que los componentes, encabezado y cuerpo de cada
        producción sean válidos.
        """

    def __init__(self, encabezado, cuerpo):
        hash(encabezado)
        hash(cuerpo)
        # print("encabezado ", encabezado)
        # print("cuerpo ", cuerpo)
        self.encabezado = encabezado
        self.cuerpo = cuerpo
        if not isinstance(self.cuerpo, tuple):
            raise ValueError("El cuerpo de la producción debe ser una tupla")
        if (encabezado,) == cuerpo:
            raise ProduccionInvalida("Producción inválida. El encabezado es igual al cuerpo.", self)

    def esRecursionIzquierda(self):

        # Compruebe si la producción tiene recursividad Izquierda

        return self.cuerpo and self.encabezado == self.cuerpo[0]

    def __eq__(self, otro):
        return self.encabezado == otro.encabezado and self.cuerpo == otro.cuerpo

    def __str__(self):
        return "{} → {}".format(self.encabezado, ' '.join(self.cuerpo))

    # retorna un string que describe el objeto
    def __repr__(self):
        return "Rule({}, {})".format(repr(self.encabezado), self.cuerpo)

    def __hash__(self):
        return hash((self.encabezado, self.cuerpo))
