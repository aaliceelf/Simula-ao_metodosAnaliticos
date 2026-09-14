class Gerador:
     
    def __init__(self, seed=12345, a=2023, c=8, M=2*32, n=100000):
        self.a = a
        self.c = c
        self.M = M
        self.n = n             
        self.previous = seed
        self.primeiro = True   
        self.usados = 0         

    def _next_random(self) -> float:
        """Gera o próximo número em [0,1) via LCG (equivalente a NextRandom())."""
        if self.primeiro:
            self.primeiro = False
            return self.previous / self.M

        self.previous = (self.a self.previous + self.c) % self.M
        return self.previous / self.M

    def proximo(self):
        """Consome e retorna o próximo aleatório, ou None se a cota (n) já foi usada (equivalente a numeroUsado())."""
        if self.usados >= self.n:
            return None

        self.usados += 1
        return self._next_random()

    def converte(self, minimo, maximo):
        """Transforma o próximo aleatório de [0,1) em um valor de [minimo, maximo]."""
        u = self.proximo()

        if u is None:
            return None

        return minimo + u * (maximo - minimo)



