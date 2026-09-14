from Gerador import Gerador

if __name__ == "__main__":
    g = Gerador(seed=12345, n=6)

    for _ in range(6):
        print(g.proximo())