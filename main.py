from Fila import Fila
from Gerador import Gerador
from Simulador import Simulador

class main:

    #Fila 1 - G/G/2/3, chegadas entre 1..5, atendimento entre 4..5
    fila1 = Fila(servers=2, capacity=3, min_arrival=1, max_arrival=5, min_service=4, max_service=5)

    #Fila 2 - G/G/1/5, sem chegadas externas, atendimento entre 1..3
    fila2 = Fila(servers=1, capacity=5, min_arrival=None, max_arrival=None, min_service=1, max_service=3)

    gerador = Gerador(seed=12345, n=100000)

    sim = Simulador(fila1, fila2, gerador, primeira_chegada=2.5)
    resultado = sim.simula()

    print(f"Tempo global da simulação: {resultado['tempo_global']:.4f}")
    print(f"Aleatórios usados: {resultado['aleatorios_usados']}")
    print()

    for nome in ("fila1", "fila2"):
        r = resultado[nome]
        print(f"--- {nome.upper()} ---")
        print(f"Perdas: {r['perdas']}")
        print("Estado | Tempo acumulado | Probabilidade")
        for estado, (t, p) in enumerate(zip(r["tempo_acumulado_por_estado"], r["probabilidades"])):
            print(f"{estado:6d} | {t:15.4f} | {p:.6f}")
        print()

