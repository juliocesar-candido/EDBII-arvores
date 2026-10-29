"""
Amazon Engineering Challenge - Árvores Balanceadas (AVL e Rubro-Negra)
IMD0039 - Estruturas de Dados Básicas II
Autor: <SEU NOME> - <SUA MATRÍCULA>

Uso: python main.py
O usuário escolhe, na execução, qual árvore utilizar (AVL ou Rubro-Negra).
Os elementos são identificadores numéricos de encomendas (inteiros).
"""
import random
import sys

from arvores import AVLTree, RedBlackTree

COLORIDO = sys.stdout.isatty()


def escolher_arvore():
    while True:
        print("\nEscolha a estrutura:")
        print("  1) Árvore AVL")
        print("  2) Árvore Rubro-Negra")
        op = input("> ").strip()
        if op == "1":
            return AVLTree()
        if op == "2":
            return RedBlackTree()
        print("Opção inválida.")


def ler_int(msg):
    try:
        return int(input(msg).strip())
    except ValueError:
        print("Valor inválido: informe um número inteiro.")
        return None


def mostrar_stats(t):
    s = t.stats()
    ok, msg = t.validar()
    print(f"\nEstrutura: {s['estrutura']}")
    print(f"  Elementos : {s['tamanho']}")
    print(f"  Altura    : {s['altura']}")
    print(f"  Rotações  : {s['rotacoes']} (esq={s['rot_esq']}, dir={s['rot_dir']})")
    if s["estrutura"] == "AVL":
        print(f"  Rotações duplas (LR/RL): {s['rot_duplas']}")
    else:
        print(f"  Recolorações: {s['recoloracoes']}   Altura negra: {t.black_height()}")
    print(f"  Propriedades: {'OK' if ok else 'FALHA'} - {msg}")


def carga(t):
    print("  1) crescente  2) decrescente  3) aleatória")
    modo = input("Ordem: ").strip()
    n = ler_int("Quantidade N: ")
    if n is None or n < 0 or modo not in ("1", "2", "3"):
        print("Entrada inválida.")
        return
    if modo == "1":
        seq = list(range(1, n + 1))
    elif modo == "2":
        seq = list(range(n, 0, -1))
    else:
        seq = random.sample(range(1, 10 * n + 1), n) if n else []
    novos = sum(t.insert(k) for k in seq)
    print(f"{novos} inseridos, {len(seq) - novos} repetidos ignorados.")


MENU = """
===== MENU =====
 1) Inserir            2) Remover           3) Buscar
 4) Percurso em ordem  5) Imprimir árvore   6) Estatísticas
 7) Inserir vários (ex: 10,20,30)           8) Carga automática
 9) Zerar contadores   10) Trocar de árvore 0) Sair"""


def main():
    t = escolher_arvore()
    while True:
        print(MENU)
        print(f"[{t.nome} | {len(t)} elementos]")
        op = input("> ").strip()
        if op == "1":
            k = ler_int("ID a inserir: ")
            if k is not None:
                print("Inserido." if t.insert(k) else f"Valor {k} já existe: inserção ignorada.")
        elif op == "2":
            k = ler_int("ID a remover: ")
            if k is not None:
                print("Removido." if t.delete(k) else f"Valor {k} não encontrado: nada removido.")
        elif op == "3":
            k = ler_int("ID a buscar: ")
            if k is not None:
                print("Encontrado." if t.search(k) else "Não encontrado.")
        elif op == "4":
            r = t.inorder()
            print(r if r else "(árvore vazia)")
        elif op == "5":
            t.print_tree(colored=COLORIDO)
        elif op == "6":
            mostrar_stats(t)
        elif op == "7":
            try:
                ks = [int(x) for x in input("IDs separados por vírgula: ").split(",")]
            except ValueError:
                print("Entrada inválida.")
                continue
            for k in ks:
                print(f"  {k}: {'inserido' if t.insert(k) else 'repetido, ignorado'}")
        elif op == "8":
            carga(t)
        elif op == "9":
            t.reset_stats()
            print("Contadores zerados.")
        elif op == "10":
            t = escolher_arvore()
        elif op == "0":
            print("Encerrando.")
            break
        else:
            print("Opção inválida.")


if __name__ == "__main__":
    main()
