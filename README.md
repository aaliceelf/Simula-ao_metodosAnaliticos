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

## ⚠️ Atenção: confira duas suposições antes de entregar

1. **Capacidade da Fila 1**: o diagrama mostra "G/G/1" sem indicar a capacidade K. Assumi K=3
   em `modelo.yml` — ajuste esse valor se o enunciado/módulo 8 especificar outro número.
2. **Leitura das setas curvas do diagrama**: interpretei as curvas pequenas perto de cada
   círculo (nós 2 e 3) como *feedback* — o cliente volta para a fila de onde saiu — e a curva
   grande do nó 2 até a entrada da Fila 1 como roteamento de rede. Se no material da disciplina
   essas curvas representarem outra coisa (ex: as duas saem para fora do sistema, ou apontam
   para lugares diferentes), é só editar a seção `roteamento` de cada fila no `modelo.yml` —
   o código não precisa mudar.
