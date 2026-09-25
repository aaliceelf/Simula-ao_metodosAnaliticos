# Simulador de Rede de Filas com Topologia Genérica

Simulador de eventos discretos para uma rede de filas com qualquer topologia (múltiplas filas,
roteamento probabilístico entre elas, chegadas externas configuráveis), carregada a partir de
um arquivo `.yml`.

## Requisitos

- Python 3.10 ou superior
- `pyyaml` (`pip install pyyaml`)

## Estrutura dos arquivos

- `Evento.py` — classe `Evento`: tipo (`chegada` ou `saida`), tempo, fila de origem
- `Escalonador.py` — fila de prioridade (heap) que ordena os eventos por tempo
- `Fila.py` — classe `Fila`: servidores, capacidade, contadores, tempos por estado, e a tabela
  de roteamento (`routing`), uma lista de tuplas `(probabilidade, destino)`, onde `destino` é o
  id de outra fila ou `None` (cliente sai do sistema)
- `Gerador.py` — gerador de números pseudoaleatórios (LCG)
- `yaml_loader.py` — lê o `.yml` e monta o dicionário de `Fila`s, o `Gerador` e os dados da
  primeira chegada
- `Simulador.py` — controla o laço principal; **evento CHEGADA** trata chegada externa;
  **evento SAÍDA** trata fim de atendimento, libera o próximo cliente da mesma fila (se houver)
  e sorteia o roteamento do cliente que terminou (para outra fila, de volta pra própria fila —
  feedback —, ou saída do sistema)
- `modelo.yml` — modelo de validação pedido no enunciado (3 filas)
- `main.py` — carrega `modelo.yml` e roda a simulação

## Como executar

```
pip install pyyaml
python main.py
```

## Formato do arquivo `.yml`

```yaml
chegada_inicial:
  fila: 1        # id da fila onde chega o primeiro cliente
  tempo: 2.0     # instante da primeira chegada

aleatorios:
  seed: 12345
  quantidade: 100000   # simulação encerra ao usar o último aleatório

filas:
  1:
    servidores: 1
    capacidade: 3
    atendimento: [1, 2]     # min, max do tempo de atendimento
    chegada: [2, 4]         # min, max do intervalo entre chegadas externas
                             # (omitir "chegada" se a fila não recebe clientes de fora)
    roteamento:
      - {probabilidade: 0.2, destino: 2}
      - {probabilidade: 0.8, destino: 3}
  2:
    servidores: 2
    capacidade: 5
    atendimento: [4, 8]
    roteamento:
      - {probabilidade: 0.5, destino: 2}     # feedback: volta pra própria fila
      - {probabilidade: 0.3, destino: 1}
      - {probabilidade: 0.2, destino: null}  # sai do sistema
```

As probabilidades de cada fila em `roteamento` devem somar 1.0.

## Saída

Para cada fila: número de clientes perdidos, tempo acumulado em cada estado e a probabilidade
de cada estado (tempo acumulado / tempo global). Também imprime o tempo global da simulação e
a quantidade de aleatórios efetivamente usados (sempre 100.000, salvo se você reduzir `quantidade`).
