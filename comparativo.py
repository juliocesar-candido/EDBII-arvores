import csv
import math
import random
import time

from arvores import AVLTree, RedBlackTree

SEED = 42
TAMANHOS = [1000, 10000, 100000]


def sequencias(n):
    rnd = random.Random(SEED)
    cres = list(range(1, n + 1))
    decr = cres[::-1]
    alea = rnd.sample(range(1, 10 * n + 1), n)
    # cenário misto: insere todos, depois remove metade (sempre com o mesmo sorteio)
    remover = rnd.sample(alea, n // 2)
    return [
        ("crescente", cres, []),
        ("decrescente", decr, []),
        ("aleatória", alea, []),
        ("aleatória + remove 50%", alea, remover),
    ]


def executa(Tree, ins, rem):
    t = Tree()
    ini = time.perf_counter()
    for k in ins:
        t.insert(k)
    for k in rem:
        t.delete(k)
    dur = time.perf_counter() - ini
    ok, _ = t.validar()
    s = t.stats()
    return {
        "altura": s["altura"], "tamanho": s["tamanho"], "rotacoes": s["rotacoes"],
        "recoloracoes": s["recoloracoes"], "tempo_s": round(dur, 4), "valida": ok,
    }


def main():
    linhas = []
    cab = f"{'cenário':<24}{'N':>8}{'ideal':>6} | {'AVL alt':>7}{'rot':>9}{'s':>8} | {'RN alt':>6}{'rot':>9}{'recol':>9}{'s':>8}"
    print(cab)
    print("-" * len(cab))
    for n in TAMANHOS:
        for nome, ins, rem in sequencias(n):
            a = executa(AVLTree, ins, rem)
            r = executa(RedBlackTree, ins, rem)
            ideal = math.ceil(math.log2(a["tamanho"] + 1)) if a["tamanho"] else 0
            assert a["valida"] and r["valida"]
            print(f"{nome:<24}{n:>8}{ideal:>6} | {a['altura']:>7}{a['rotacoes']:>9}{a['tempo_s']:>8} |"
                  f" {r['altura']:>6}{r['rotacoes']:>9}{r['recoloracoes']:>9}{r['tempo_s']:>8}")
            linhas.append({"cenario": nome, "N": n, "altura_ideal": ideal,
                           **{f"avl_{k}": v for k, v in a.items()},
                           **{f"rn_{k}": v for k, v in r.items()}})
    with open("resultados.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=linhas[0].keys())
        w.writeheader()
        w.writerows(linhas)
    print("\nResultados salvos em resultados.csv")


if __name__ == "__main__":
    main()
