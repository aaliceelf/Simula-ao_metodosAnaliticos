from Evento import Evento
from Escalonador import Escalonador
from Fila import Fila
from Gerador import Gerador


class Simulador:
    def __init__(self, fila1: Fila, fila2: Fila, gerador: Gerador, primeira_chegada=3.0):
        self.fila1 = fila1
        self.fila2 = fila2
        self.gerador = gerador
        self.escalonador = Escalonador()
        self.relogio = 0.0  

        self.escalonador.agendar(Evento("chegada", primeira_chegada, fila_id=1))

    def acumula_tempo(self, ev: Evento) -> None:
        """Contabiliza o tempo decorrido no estado ATUAL das duas filas até o instante do evento."""
        delta = ev.tempo - self.relogio
        self.fila1.times[self.fila1.Status()] += delta
        self.fila2.times[self.fila2.Status()] += delta
        self.relogio = ev.tempo

    def chegada(self, ev: Evento) -> None:
        """Chegada externa de um cliente na Fila1."""
        self.acumula_tempo(ev)

        if self.fila1.Status() < self.fila1.Capacity():
            self.fila1.In()

            if self.fila1.Status() <= self.fila1.Servers():
                t_servico = self.gerador.converte(self.fila1.min_service, self.fila1.max_service)
                if t_servico is not None:
                    self.escalonador.agendar(Evento("passagem", self.relogio + t_servico, fila_id=1))
        else:
            self.fila1.Loss()

        intervalo = self.gerador.converte(self.fila1.min_arrival, self.fila1.max_arrival)
        if intervalo is not None:
            self.escalonador.agendar(Evento("chegada", self.relogio + intervalo, fila_id=1))

    def passagem(self, ev: Evento) -> None:
        """Cliente termina o atendimento na Fila1 e passa para a Fila2."""
        self.acumula_tempo(ev)

        self.fila1.Out()

        if self.fila1.Status() >= self.fila1.Servers():
            t_servico = self.gerador.converte(self.fila1.min_service, self.fila1.max_service)
            if t_servico is not None:
                self.escalonador.agendar(Evento("passagem", self.relogio + t_servico, fila_id=1))

        if self.fila2.Status() < self.fila2.Capacity():
            self.fila2.In()

            if self.fila2.Status() <= self.fila2.Servers():
                t_servico = self.gerador.converte(self.fila2.min_service, self.fila2.max_service)
                if t_servico is not None:
                    self.escalonador.agendar(Evento("saida", self.relogio + t_servico, fila_id=2))
        else:
            self.fila2.Loss()

    def saida(self, ev: Evento) -> None:
        """Cliente termina o atendimento na Fila2 e sai do sistema."""
        self.acumula_tempo(ev)

        self.fila2.Out()

        if self.fila2.Status() >= self.fila2.Servers():
            t_servico = self.gerador.converte(self.fila2.min_service, self.fila2.max_service)
            if t_servico is not None:
                self.escalonador.agendar(Evento("saida", self.relogio + t_servico, fila_id=2))

    def simula(self) -> dict:
        while not self.escalonador.vazio():
            ev = self.escalonador.proximo()

            if ev.tipo == "chegada":
                self.chegada(ev)
            elif ev.tipo == "saida":
                self.saida(ev)
            elif ev.tipo == "passagem":
                self.passagem(ev)

        return self._resultado()

    def _resultado(self) -> dict:
        resultado = {"tempo_global": self.relogio, "aleatorios_usados": self.gerador.usados}

        for nome, fila in (("fila1", self.fila1), ("fila2", self.fila2)):
            resultado[nome] = {
                "tempo_acumulado_por_estado": list(fila.times),
                "probabilidades": [t / self.relogio for t in fila.times],
                "perdas": fila.loss,
            }

        return resultado