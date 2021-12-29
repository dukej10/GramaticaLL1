

class EvaluadorSiguiente:

    def __init__(self, secuencia=()):
        self.tupla = tuple(secuencia)

    def __eq__(self, otro):
        return isinstance(self, type(otro))

    def __hash__(self):
        return hash(type(self))

    def __add__(self, secuencia=()):
        return EvaluadorSiguiente(self.tupla + tuple(secuencia))

    def __iter__(self):
        return iter(self.tupla)

    def __str__(self):
        return str(self.tupla)
