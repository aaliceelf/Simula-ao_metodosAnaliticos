import yaml
from Fila import Fila
from Gerador import Gerador


def carrega_modelo(caminho_yaml):
    """Lê um arquivo .yml com a topologia da rede de filas e monta os objetos Fila, o Gerador
    e os dados da primeira chegada, prontos para o Simulador."""

    with open(caminho_yaml, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    filas = {}
    for fila_id_bruto, dados in config["filas"].items():
        fila_id = int(fila_id_bruto)

        atendimento = dados["atendimento"]
        chegada = dados.get("chegada")  # None se a fila não recebe chegada externa

        roteamento_bruto = dados.get("roteamento", [{"probabilidade": 1.0, "destino": None}])
        routing = [(item["probabilidade"], item["destino"]) for item in roteamento_bruto]

        filas[fila_id] = Fila(
            id=fila_id,
            servers=dados["servidores"],
            capacity=dados["capacidade"],
            min_service=atendimento[0],
            max_service=atendimento[1],
            min_arrival=chegada[0] if chegada else None,
            max_arrival=chegada[1] if chegada else None,
            routing=routing,
        )

    gerador = Gerador(seed=config["aleatorios"]["seed"], n=config["aleatorios"]["quantidade"])

    chegada_inicial = config["chegada_inicial"]

    return filas, gerador, chegada_inicial["fila"], chegada_inicial["tempo"]
