class Evento:

    def __init__(self, tipo, tempo, fila_id=None, servidor_idx=None):
        self.tipo = tipo              
        self.tempo = tempo           
        self.fila_id = fila_id        
        self.servidor_idx = servidor_idx  

    def __lt__(self, other):
        """Sobrecarga equivalente ao compareTo: ordena pelo tempo do evento."""
        return self.tempo < other.tempo

    def __repr__(self):
        return f"Evento({self.tipo}, t={self.tempo:.4f}, fila={self.fila_id})"