import math

class Fila:
    def __init__(self, servers, capacity, min_arrival, max_arrival, min_service, max_service):
        
        self.servers = servers
        self.capacity = capacity
        self.min_arrival = min_arrival
        self.max_arrival = max_arrival
        self.min_service = min_service
        self.max_service = max_service

        
        self.customers = 0
        self.loss = 0
        self.times = [0.0] * (capacity + 1)

        
        self.scheduled_departures = [math.inf] * servers
        self.waiting_line = 0

   
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