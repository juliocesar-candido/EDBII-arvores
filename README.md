# Amazon Engineering Challenge – Árvores Balanceadas (AVL e Rubro-Negra)

**Disciplina:** Estruturas de Dados Básicas II
**Autor:** Júlio César Cândido de Santana

Protótipo para registrar, localizar e remover identificadores de encomendas (Black Friday)
usando árvores balanceadas implementadas do zero

## Requisitos
Python 3.8+ (somente biblioteca padrão; sem dependências externas)

## Como executar
```bash
python main.py
```
O programa pergunta qual árvore usar (AVL ou Rubro-Negra) e abre um menu interativo

## Funcionalidades
Inserção, remoção, busca, percurso em ordem, impressão da árvore (na Rubro-Negra com
cor de cada nó: `(R)`/`(B)`, e ANSI em terminais compatíveis), estatísticas (altura,
rotações, recolorações) e validação das propriedades da estrutura

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

## Evidências de execução

Todos os prints foram gerados com `python main.py`, `python -m unittest discover -s tests -v` e `python comparativo.py`.

### Testes automatizados (38 testes, mesmos testes nas duas árvores)
![Testes - início](prints/01_testes_inicio.png)
![Testes - fim, 38 testes OK](prints/02_testes_fim_ok.png)

### Comparativo AVL × Rubro-Negra (mesmas sequências)
![Tabela comparativa](prints/03_comparativo_tabela.png)

### Árvore AVL
Inserção e impressão da árvore (cada nó mostra o fator de balanceamento):
![AVL - inserção e árvore](prints/04_avl_insercao_arvore.png)

Busca de existente e inexistente, e inserção de valor repetido (ignorada):
![AVL - busca e repetido](prints/05_avl_busca_repetido.png)

Remoção de folha (20), de nó com dois filhos (70) e de inexistente (99):
![AVL - remoção](prints/06_avl_remocao.png)

Percurso em ordem, árvore final e estatísticas (propriedades válidas):
![AVL - percurso e estatísticas](prints/07_avl_percurso_stats.png)

Árvore vazia:
![AVL - árvore vazia](prints/11_avl_arvore_vazia.png)

Carga de 1.000 IDs em ordem crescente (altura 10):
![AVL - carga de 1000](prints/12_avl_carga_1000.png)

### Árvore Rubro-Negra
Inserção e impressão da árvore (cada nó mostra a cor, R ou B):
![Rubro-Negra - inserção e árvore](prints/08_rb_insercao_arvore.png)

Busca de existente e inexistente, e inserção de valor repetido (ignorada):
![Rubro-Negra - busca e repetido](prints/09_rb_busca_repetido.png)

Remoção, percurso em ordem e árvore final com cores:
![Rubro-Negra - remoção](prints/10_rb_remocao_arvore.png)

## Referências
- CORMEN et al. *Introduction to Algorithms* (CLRS) – capítulo de árvores rubro-negras.
- https://github.com/nkokor/red-black-tree
- https://github.com/burpeesDaily/forest-python
