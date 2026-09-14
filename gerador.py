class gerador:

    def __init__(self, a, c, M, seed):
        self.a = a
        self.c = c
        self.M = M
        self._previous = seed
        self.contador = 0  # quantos números já foram gerados (usado como critério de parada)

    def NextRandom(self) -> float:
        """Gera o próximo número pseudoaleatório normalizado entre 0 e 1."""
        self._previous = (self.a * self._previous + self.c) % self.M
        self.contador += 1
        return self._previous / self.M
 
    def uniforme(self, lo, hi):
        """U(a,b) = a + [(b-a) * x], onde x é o próximo número pseudoaleatório."""
        return lo + (hi - lo) * self.NextRandom()
