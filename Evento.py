class Evento:
    def init(self, tipo, tempo, fila_id=None, servidor_idx=None):
        self.tipo = tipo              # "chegada", "saida" ou "passagem"
        self.tempo = tempo            # tempo em que o evento deve ocorrer
        self.fila_id = fila_id        # qual fila esse evento pertence (1 ou 2, por exemplo)
        self.servidor_idx = servidor_idx  # qual servidor, quando aplicável (evento de saída)

    def lt(self, other):
        """Sobrecarga equivalente ao compareTo: ordena pelo tempo do evento."""
        return self.tempo < other.tempo

    def repr(self):
        return f"Evento({self.tipo}, t={self.tempo:.4f}, fila={self.fila_id})"