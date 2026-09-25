from Simulador import Simulador
from yaml_loader import carrega_modelo

filas, gerador, fila_inicial, tempo_inicial = carrega_modelo("modelo.yml")

sim = Simulador(filas, gerador, fila_id_primeira_chegada=fila_inicial, primeira_chegada=tempo_inicial)
resultado = sim.simula()

print(f"Tempo global da simulação: {resultado['tempo_global']:.4f}")
print(f"Aleatórios usados: {resultado['aleatorios_usados']}")
print()

for fila_id in sorted(resultado["filas"]):
    r = resultado["filas"][fila_id]
    print(f"--- FILA {fila_id} ---")
    print(f"Perdas: {r['perdas']}")
    print("Estado | Tempo acumulado | Probabilidade")
    for estado, (t, p) in enumerate(zip(r["tempo_acumulado_por_estado"], r["probabilidades"])):
        print(f"{estado:6d} | {t:15.4f} | {p:.6f}")
    print()
