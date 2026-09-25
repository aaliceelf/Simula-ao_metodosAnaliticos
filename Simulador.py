from Evento import Evento
from Escalonador import Escalonador
from Fila import Fila
from Gerador import Gerador


class Simulador:
    def __init__(self, filas: dict, gerador: Gerador, fila_id_primeira_chegada, primeira_chegada=3.0):
        self.filas = filas  # dict {id: Fila}
        self.gerador = gerador
        self.escalonador = Escalonador()
        self.relogio = 0.0

        self.escalonador.agendar(Evento("chegada", primeira_chegada, fila_id=fila_id_primeira_chegada))

    def acumula_tempo(self, ev: Evento) -> None:
        """Contabiliza o tempo decorrido no estado ATUAL de TODAS as filas até o instante do evento."""
        delta = ev.tempo - self.relogio
        for fila in self.filas.values():
            fila.times[fila.Status()] += delta
        self.relogio = ev.tempo

    def _agenda_servico(self, fila: Fila) -> None:
        """Sorteia o tempo de atendimento e agenda o evento de SAÍDA (fim de serviço) da fila."""
        t_servico = self.gerador.converte(fila.min_service, fila.max_service)
        if t_servico is not None:
            self.escalonador.agendar(Evento("saida", self.relogio + t_servico, fila_id=fila.id))

    def _recebe_cliente(self, fila: Fila) -> None:
        """Um cliente tenta entrar na fila — seja por chegada externa, seja roteado de outra fila."""
        if fila.Status() < fila.Capacity():
            fila.In()
            if fila.Status() <= fila.Servers():
                self._agenda_servico(fila)
        else:
            fila.Loss()

    def chegada(self, ev: Evento) -> None:
        """Chegada externa de um cliente na fila ev.fila_id."""
        self.acumula_tempo(ev)
        fila = self.filas[ev.fila_id]

        self._recebe_cliente(fila)

        if fila.tem_chegada_externa():
            intervalo = self.gerador.converte(fila.min_arrival, fila.max_arrival)
            if intervalo is not None:
                self.escalonador.agendar(Evento("chegada", self.relogio + intervalo, fila_id=fila.id))

    def saida(self, ev: Evento) -> None:
        """Cliente termina o atendimento na fila ev.fila_id. Se havia alguém esperando, o próximo
        entra em serviço; em seguida sorteia-se o roteamento: para qual fila o cliente vai (ou se
        sai do sistema)."""
        self.acumula_tempo(ev)
        fila = self.filas[ev.fila_id]

        fila.Out()

        if fila.Status() >= fila.Servers():
            self._agenda_servico(fila)

        r = self.gerador.proximo()
        if r is not None:
            destino_id = fila.sorteia_destino(r)
            if destino_id is not None:
                self._recebe_cliente(self.filas[destino_id])

    def simula(self) -> dict:
        while not self.escalonador.vazio():
            ev = self.escalonador.proximo()

            if ev.tipo == "chegada":
                self.chegada(ev)
            elif ev.tipo == "saida":
                self.saida(ev)

        return self._resultado()

    def _resultado(self) -> dict:
        resultado = {
            "tempo_global": self.relogio,
            "aleatorios_usados": self.gerador.usados,
            "filas": {},
        }

        for fila_id, fila in self.filas.items():
            resultado["filas"][fila_id] = {
                "tempo_acumulado_por_estado": list(fila.times),
                "probabilidades": [t / self.relogio for t in fila.times],
                "perdas": fila.loss,
            }

        return resultado
