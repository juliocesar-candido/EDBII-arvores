class AVLNode:
    __slots__ = ("key", "left", "right", "height")

    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1


class AVLTree:
    nome = "AVL"

    def __init__(self):
        self.root = None
        self._size = 0
        self._ok = False 
        self.reset_stats()

    def reset_stats(self):
        self.rot_esq = 0
        self.rot_dir = 0
        self.duplas = 0

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
            "rot_duplas": self.duplas,
            "recoloracoes": 0, 
        }

    def __len__(self):
        return self._size

    @staticmethod
    def _h(n):
        return n.height if n else 0

    def _update(self, n):
        n.height = 1 + max(self._h(n.left), self._h(n.right))

    def _balance(self, n):
        return self._h(n.left) - self._h(n.right) if n else 0

    def height(self):
        return self._h(self.root)

    def _rot_right(self, y):
        x = y.left
        y.left = x.right
        x.right = y
        self._update(y)
        self._update(x)
        self.rot_dir += 1
        return x

    def _rot_left(self, x):
        y = x.right
        x.right = y.left
        y.left = x
        self._update(x)
        self._update(y)
        self.rot_esq += 1
        return y

    def _rebalance(self, n):
        self._update(n)
        bal = self._balance(n)
        if bal > 1:                                
            if self._balance(n.left) < 0:          
                n.left = self._rot_left(n.left)
                self.duplas += 1
            return self._rot_right(n)
        if bal < -1:                                 
            if self._balance(n.right) > 0:          
                n.right = self._rot_right(n.right)
                self.duplas += 1
            return self._rot_left(n)
        return n

  
    def insert(self, key):
        self._ok = False
        self.root = self._insert(self.root, key)
        if self._ok:
            self._size += 1
        return self._ok

    def _insert(self, n, key):
        if n is None:
            self._ok = True
            return AVLNode(key)
        if key < n.key:
            n.left = self._insert(n.left, key)
        elif key > n.key:
            n.right = self._insert(n.right, key)
        else:
            return n  # duplicada: rejeita
        return self._rebalance(n) if self._ok else n

   
    def search(self, key):
        n = self.root
        while n:
            if key == n.key:
                return True
            n = n.left if key < n.key else n.right
        return False

  
    def delete(self, key):
        self._ok = False
        self.root = self._delete(self.root, key)
        if self._ok:
            self._size -= 1
        return self._ok

    def _delete(self, n, key):
        if n is None:
            return None 
        if key < n.key:
            n.left = self._delete(n.left, key)
        elif key > n.key:
            n.right = self._delete(n.right, key)
        else:
            self._ok = True
            if n.left is None:
                return n.right
            if n.right is None:
                return n.left
            s = n.right
            while s.left:
                s = s.left
            n.key = s.key
            n.right = self._delete_min(n.right)
        return self._rebalance(n) if self._ok else n

    def _delete_min(self, n):
        if n.left is None:
            return n.right
        n.left = self._delete_min(n.left)
        return self._rebalance(n)

   
    def inorder(self):
        res, stack, n = [], [], self.root
        while stack or n:
            while n:
                stack.append(n)
                n = n.left
            n = stack.pop()
            res.append(n.key)
            n = n.right
        return res

    
    def render(self, colored=False):
        if not self.root:
            return "(árvore vazia)"
        lines = []

        def rec(n, prefix, is_left):
            if n.right:
                rec(n.right, prefix + ("│   " if is_left else "    "), False)
            lines.append(f"{prefix}{'└── ' if is_left else '┌── '}{n.key} [fb={self._balance(n)}]")
            if n.left:
                rec(n.left, prefix + ("    " if is_left else "│   "), True)

        rec(self.root, "", True)
        return "\n".join(lines)

    def print_tree(self, colored=False):
        print(self.render(colored))

    def validar(self):
        def rec(n, lo, hi):
            if n is None:
                return 0, None
            if (lo is not None and n.key <= lo) or (hi is not None and n.key >= hi):
                return 0, f"violação BST em {n.key}"
            hl, e = rec(n.left, lo, n.key)
            if e:
                return 0, e
            hr, e = rec(n.right, n.key, hi)
            if e:
                return 0, e
            if n.height != 1 + max(hl, hr):
                return 0, f"altura armazenada incorreta em {n.key}"
            if abs(hl - hr) > 1:
                return 0, f"desbalanceado em {n.key} (fb={hl - hr})"
            return 1 + max(hl, hr), None

        _, err = rec(self.root, None, None)
        return (err is None), (err or "AVL válida")

    def is_valid(self):
        return self.validar()[0]
