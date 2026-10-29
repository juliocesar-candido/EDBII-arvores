"""
Árvore Rubro-Negra (implementação própria, baseada no algoritmo do CLRS
com nó sentinela NIL).

Propriedades:
  1. Todo nó é vermelho ou preto.
  2. A raiz é preta.
  3. As folhas (NIL) são pretas.
  4. Filho de nó vermelho é preto (sem dois vermelhos seguidos).
  5. Todo caminho de um nó até suas folhas NIL tem o mesmo nº de nós pretos.

Decisões de projeto (documentadas conforme o enunciado):
  - Inserir chave repetida: REJEITADA, árvore inalterada, retorna False.
  - Remover chave inexistente: árvore inalterada, retorna False.
  - Buscar chave inexistente: retorna False (sem exceção).
  - Remoção de nó com 2 filhos: substituído pelo SUCESSOR em ordem.
  - Altura: árvore vazia = 0; árvore com um nó = 1.

Contadores (para a análise comparativa):
  - rot_esq / rot_dir: rotações simples executadas.
  - recoloracoes: nº de vezes que um nó REALMENTE mudou de cor
    (a cor inicial vermelha de um nó recém-inserido não conta).
"""

RED = "R"
BLACK = "B"


class RBNode:
    __slots__ = ("key", "color", "left", "right", "parent")

    def __init__(self, key, color=RED):
        self.key = key
        self.color = color
        self.left = None
        self.right = None
        self.parent = None


class RedBlackTree:
    nome = "Rubro-Negra"

    def __init__(self):
        self.NIL = RBNode(None, BLACK)
        self.NIL.left = self.NIL.right = self.NIL.parent = self.NIL
        self.root = self.NIL
        self._size = 0
        self.reset_stats()

    # ------------------------------------------------------------ estatísticas
    def reset_stats(self):
        self.rot_esq = 0
        self.rot_dir = 0
        self.recoloracoes = 0

    @property
    def rotacoes(self):
        return self.rot_esq + self.rot_dir

    def stats(self):
        return {
            "estrutura": self.nome,
            "tamanho": self._size,
            "altura": self.height(),
            "rotacoes": self.rotacoes,
            "rot_esq": self.rot_esq,
            "rot_dir": self.rot_dir,
            "rot_duplas": 0,
            "recoloracoes": self.recoloracoes,
        }

    def __len__(self):
        return self._size

    # ------------------------------------------------------------- utilidades
    def _set_color(self, node, color):
        """Muda a cor contando apenas mudanças reais (nunca mexe no NIL)."""
        if node is not self.NIL and node.color != color:
            node.color = color
            self.recoloracoes += 1

    def _minimum(self, n):
        while n.left is not self.NIL:
            n = n.left
        return n

    def height(self):
        def rec(n):
            return 0 if n is self.NIL else 1 + max(rec(n.left), rec(n.right))
        return rec(self.root)

    # --------------------------------------------------------------- rotações
    def _rot_left(self, x):
        y = x.right
        x.right = y.left
        if y.left is not self.NIL:
            y.left.parent = x
        y.parent = x.parent
        if x.parent is self.NIL:
            self.root = y
        elif x is x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y
        self.rot_esq += 1

    def _rot_right(self, y):
        x = y.left
        y.left = x.right
        if x.right is not self.NIL:
            x.right.parent = y
        x.parent = y.parent
        if y.parent is self.NIL:
            self.root = x
        elif y is y.parent.right:
            y.parent.right = x
        else:
            y.parent.left = x
        x.right = y
        y.parent = x
        self.rot_dir += 1

    # ---------------------------------------------------------------- inserção
    def insert(self, key):
        parent, cur = self.NIL, self.root
        while cur is not self.NIL:
            parent = cur
            if key == cur.key:
                return False  # duplicada: rejeita
            cur = cur.left if key < cur.key else cur.right

        z = RBNode(key, RED)
        z.left = z.right = self.NIL
        z.parent = parent
        if parent is self.NIL:
            self.root = z
        elif key < parent.key:
            parent.left = z
        else:
            parent.right = z
        self._size += 1
        self._insert_fixup(z)
        return True

    def _insert_fixup(self, z):
        while z.parent.color == RED:
            gp = z.parent.parent
            if z.parent is gp.left:
                uncle = gp.right
                if uncle.color == RED:              # caso 1: tio vermelho -> recolore
                    self._set_color(z.parent, BLACK)
                    self._set_color(uncle, BLACK)
                    self._set_color(gp, RED)
                    z = gp
                else:
                    if z is z.parent.right:         # caso 2: triângulo -> rotação
                        z = z.parent
                        self._rot_left(z)
                    self._set_color(z.parent, BLACK)  # caso 3: linha -> rotação + cores
                    self._set_color(z.parent.parent, RED)
                    self._rot_right(z.parent.parent)
            else:
                uncle = gp.left
                if uncle.color == RED:
                    self._set_color(z.parent, BLACK)
                    self._set_color(uncle, BLACK)
                    self._set_color(gp, RED)
                    z = gp
                else:
                    if z is z.parent.left:
                        z = z.parent
                        self._rot_right(z)
                    self._set_color(z.parent, BLACK)
                    self._set_color(z.parent.parent, RED)
                    self._rot_left(z.parent.parent)
        self._set_color(self.root, BLACK)

    # ------------------------------------------------------------------ busca
    def _find(self, key):
        n = self.root
        while n is not self.NIL:
            if key == n.key:
                return n
            n = n.left if key < n.key else n.right
        return self.NIL

    def search(self, key):
        return self._find(key) is not self.NIL

    # ----------------------------------------------------------------- remoção
    def _transplant(self, u, v):
        if u.parent is self.NIL:
            self.root = v
        elif u is u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent  # funciona mesmo se v for NIL

    def delete(self, key):
        z = self._find(key)
        if z is self.NIL:
            return False

        y = z
        y_orig_color = y.color
        if z.left is self.NIL:
            x = z.right
            self._transplant(z, z.right)
        elif z.right is self.NIL:
            x = z.left
            self._transplant(z, z.left)
        else:
            y = self._minimum(z.right)
            y_orig_color = y.color
            x = y.right
            if y.parent is z:
                x.parent = y
            else:
                self._transplant(y, y.right)
                y.right = z.right
                y.right.parent = y
            self._transplant(z, y)
            y.left = z.left
            y.left.parent = y
            self._set_color(y, z.color)
        self._size -= 1
        if y_orig_color == BLACK:
            self._delete_fixup(x)
        return True

    def _delete_fixup(self, x):
        while x is not self.root and x.color == BLACK:
            if x is x.parent.left:
                w = x.parent.right
                if w.color == RED:                          # caso 1: irmão vermelho
                    self._set_color(w, BLACK)
                    self._set_color(x.parent, RED)
                    self._rot_left(x.parent)
                    w = x.parent.right
                if w.left.color == BLACK and w.right.color == BLACK:   # caso 2
                    self._set_color(w, RED)
                    x = x.parent
                else:
                    if w.right.color == BLACK:              # caso 3
                        self._set_color(w.left, BLACK)
                        self._set_color(w, RED)
                        self._rot_right(w)
                        w = x.parent.right
                    self._set_color(w, x.parent.color)      # caso 4
                    self._set_color(x.parent, BLACK)
                    self._set_color(w.right, BLACK)
                    self._rot_left(x.parent)
                    x = self.root
            else:
                w = x.parent.left
                if w.color == RED:
                    self._set_color(w, BLACK)
                    self._set_color(x.parent, RED)
                    self._rot_right(x.parent)
                    w = x.parent.left
                if w.right.color == BLACK and w.left.color == BLACK:
                    self._set_color(w, RED)
                    x = x.parent
                else:
                    if w.left.color == BLACK:
                        self._set_color(w.right, BLACK)
                        self._set_color(w, RED)
                        self._rot_left(w)
                        w = x.parent.left
                    self._set_color(w, x.parent.color)
                    self._set_color(x.parent, BLACK)
                    self._set_color(w.left, BLACK)
                    self._rot_right(x.parent)
                    x = self.root
        self._set_color(x, BLACK)

    # ----------------------------------------------------------------- percurso
    def inorder(self):
        res, stack, n = [], [], self.root
        while stack or n is not self.NIL:
            while n is not self.NIL:
                stack.append(n)
                n = n.left
            n = stack.pop()
            res.append(n.key)
            n = n.right
        return res

    # ------------------------------------------------------------ visualização
    def render(self, colored=False):
        """Desenho horizontal. Cada nó mostra: chave (R) ou (B).
        Com colored=True usa cores ANSI (vermelho/branco) além da letra."""
        if self.root is self.NIL:
            return "(árvore vazia)"
        lines = []

        def label(n):
            txt = f"{n.key}({n.color})"
            if colored:
                return f"\033[91m{txt}\033[0m" if n.color == RED else f"\033[1m{txt}\033[0m"
            return txt

        def rec(n, prefix, is_left):
            if n.right is not self.NIL:
                rec(n.right, prefix + ("│   " if is_left else "    "), False)
            lines.append(f"{prefix}{'└── ' if is_left else '┌── '}{label(n)}")
            if n.left is not self.NIL:
                rec(n.left, prefix + ("    " if is_left else "│   "), True)

        rec(self.root, "", True)
        return "\n".join(lines)

    def print_tree(self, colored=False):
        print(self.render(colored))

    # ------------------------------------------------------------- validação
    def validar(self):
        """Retorna (ok, mensagem). Verifica BST e as propriedades 2, 4 e 5."""
        if self.root.color != BLACK:
            return False, "raiz não é preta"
        if self.NIL.color != BLACK:
            return False, "NIL não é preto"

        def rec(n, lo, hi):
            if n is self.NIL:
                return 1, None
            if (lo is not None and n.key <= lo) or (hi is not None and n.key >= hi):
                return 0, f"violação BST em {n.key}"
            if n.color == RED and (n.left.color == RED or n.right.color == RED):
                return 0, f"dois vermelhos seguidos em {n.key}"
            for c in (n.left, n.right):
                if c is not self.NIL and c.parent is not n:
                    return 0, f"ponteiro pai incorreto em {c.key}"
            bl, e = rec(n.left, lo, n.key)
            if e:
                return 0, e
            br, e = rec(n.right, n.key, hi)
            if e:
                return 0, e
            if bl != br:
                return 0, f"altura negra diferente em {n.key} ({bl} x {br})"
            return bl + (1 if n.color == BLACK else 0), None

        _, err = rec(self.root, None, None)
        return (err is None), (err or "Rubro-Negra válida")

    def is_valid(self):
        return self.validar()[0]

    def black_height(self):
        n, bh = self.root, 0
        while n is not self.NIL:
            if n.color == BLACK:
                bh += 1
            n = n.left
        return bh
