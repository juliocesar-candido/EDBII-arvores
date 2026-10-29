# Amazon Engineering Challenge – Árvores Balanceadas (AVL e Rubro-Negra)

**Disciplina:** Estruturas de Dados Básicas II
**Autor:** Júlio César Cândido de Santana

Protótipo para registrar, localizar e remover identificadores de encomendas (Black Friday)
usando árvores balanceadas implementadas do zero, sem bibliotecas de balanceamento.

## Requisitos
Python 3.8+ (somente biblioteca padrão; sem dependências externas).

## Como executar
```bash
python main.py
```
O programa pergunta qual árvore usar (AVL ou Rubro-Negra) e abre um menu interativo.

## Funcionalidades
Inserção, remoção, busca, percurso em ordem, impressão da árvore (na Rubro-Negra com
cor de cada nó: `(R)`/`(B)`, e ANSI em terminais compatíveis), estatísticas (altura,
rotações, recolorações) e validação das propriedades da estrutura.

## Decisões de implementação
| Situação | Decisão |
|---|---|
| Inserir valor repetido | Rejeitado; árvore inalterada; retorna `False` |
| Buscar inexistente | Retorna `False` (sem exceção) |
| Remover inexistente | Árvore inalterada; retorna `False` |
| Remoção com 2 filhos | Substitui pelo sucessor em ordem |
| Altura | Vazia = 0; um nó = 1 |
| Rotações | Contam-se rotações simples individuais; rotação dupla = 2 simples |
| Recolorações | Contam-se mudanças reais de cor (nó novo nasce vermelho e não conta) |

## Estrutura
```
main.py             menu interativo
trees/avl.py        AVL (rotações LL, RR, LR, RL)
trees/red_black.py  Rubro-Negra (recoloração + rotações, estilo CLRS com sentinela NIL)
tests/              testes (a adicionar)
```

## Referências
- CORMEN et al. *Introduction to Algorithms* (CLRS) – capítulo de árvores rubro-negras.
- https://github.com/nkokor/red-black-tree
- https://github.com/burpeesDaily/forest-python
