import heapq
from Evento import Evento

class Escalonador:
    """Fila de prioridade mínima: o próximo() sempre retorna o evento com menor tempo."""

    def __init__(self):
        self._eventos = []

    def agendar(self, evento: Evento) -> None:
        """Insere um evento na ordem correta (equivalente a add() da PriorityQueue)."""
        heapq.heappush(self._eventos, evento)

    def proximo(self) -> Evento:
        """Remove e retorna o evento de menor tempo (equivalente a poll())."""
        if self.vazio():
            return None
        return heapq.heappop(self._eventos)

    def vazio(self) -> bool:
        return len(self._eventos) == 0
