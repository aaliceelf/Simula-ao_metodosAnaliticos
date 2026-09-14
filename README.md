# Simulador de Filas em Tandem

Simulador de eventos discretos para uma rede de duas filas em tandem (Fila 1 → Fila 2), desenvolvido em Python.

## Requisitos

- Python 3.10 ou superior (não usa bibliotecas externas, apenas `math` e `heapq` da biblioteca padrão)

## Estrutura dos arquivos

- `evento.py` — classe `Evento`, representa um evento da simulação (tipo, tempo, fila de origem)
- `escalonador.py` — classe `Escalonador`, fila de prioridade que ordena os eventos por tempo de ocorrência
- `fila.py` — classe `Fila`, representa uma fila individual (servidores, capacidade, contadores de clientes e perdas, tempos acumulados por estado)
- `gerador.py` — classe `Gerador`, gerador de números pseudoaleatórios (LCG) usado para os intervalos de chegada e tempos de atendimento
- `simulador.py` — classe `Simulador`, controla o laço principal da simulação e o tratamento dos eventos de chegada, saída e passagem entre filas
- `main.py` — script pronto com o cenário de validação pedido no enunciado

## Como executar

No terminal, a partir da pasta do projeto:

```
python main.py
```

O script já está configurado com o cenário de teste:

- Fila 1: G/G/2/3, chegadas entre 1 e 5, atendimento entre 4 e 5
- Fila 2: G/G/1/5, sem chegadas externas (recebe 100% dos clientes vindos da Fila 1), atendimento entre 1 e 3
- Filas inicialmente vazias, primeiro cliente chega em t = 2,5
- Simulação com 100.000 números aleatórios

## Saída

O programa imprime, para cada fila:

- Número de clientes perdidos
- Tempo acumulado em cada estado (quantidade de clientes na fila)
- Probabilidade de cada estado (tempo acumulado dividido pelo tempo global)

Também imprime o tempo global da simulação e a quantidade de aleatórios efetivamente usados.

## Rodando outro cenário

Para simular com outros parâmetros, edite `main.py` e ajuste os argumentos ao instanciar as filas:

```python
fila1 = Fila(servers=2, capacity=3, min_arrival=1, max_arrival=5, min_service=4, max_service=5)
fila2 = Fila(servers=1, capacity=5, min_arrival=None, max_arrival=None, min_service=1, max_service=3)

sim = Simulador(fila1, fila2, gerador, primeira_chegada=2.5)
```

A Fila 2 não usa `min_arrival`/`max_arrival` porque não recebe chegadas externas — todo cliente que entra nela vem da saída da Fila 1.
