import math

class Fila:
    def __init__(self, id, servers, capacity, min_service, max_service,
                 min_arrival=None, max_arrival=None, routing=None):

        self.id = id
        self.servers = servers
        self.capacity = capacity
        self.min_arrival = min_arrival
        self.max_arrival = max_arrival
        self.min_service = min_service
        self.max_service = max_service

        # roteamento: lista de tuplas (probabilidade, destino)
        # destino é o id de outra Fila, ou None (cliente sai do sistema).
        # Se não for informado, assume-se 100% de saída do sistema (como antes).
        self.routing = routing if routing is not None else [(1.0, None)]

        self.customers = 0
        self.loss = 0
        self.times = [0.0] * (capacity + 1)

    def Status(self) -> int:
        """Retorna quantos clientes estão na fila no momento."""
        return self.customers

    def Capacity(self) -> int:
        """Retorna a capacidade da fila."""
        return self.capacity

    def Servers(self) -> int:
        """Retorna o número de servidores da fila."""
        return self.servers

    def Loss(self) -> None:
        """Contabiliza uma perda (incrementa self.loss em 1)."""
        self.loss += 1

    def In(self) -> None:
        """Contabiliza a chegada de um cliente (incrementa self.customers em 1)."""
        self.customers += 1

    def Out(self) -> None:
        """Contabiliza a saída de um cliente (decrementa self.customers em 1)."""
        self.customers -= 1

    def tem_chegada_externa(self) -> bool:
        """Indica se esta fila recebe clientes vindos de fora da rede (não só de roteamento)."""
        return self.min_arrival is not None and self.max_arrival is not None

    def sorteia_destino(self, r: float):
        """Dado um número aleatório r em [0,1), percorre as faixas acumuladas de probabilidade
        do roteamento e retorna o destino sorteado (id de outra fila, ou None se sai do sistema)."""
        acumulado = 0.0
        for probabilidade, destino in self.routing:
            acumulado += probabilidade
            if r < acumulado:
                return destino
        return self.routing[-1][1]  # salvaguarda para erro de arredondamento (r muito perto de 1.0)
