import os
import random
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from arvores import AVLTree, RedBlackTree


class _Comum:
    Tree = None

    def novo(self, chaves=()):
        t = self.Tree()
        for k in chaves:
            t.insert(k)
        return t

    def valida(self, t):
        ok, msg = t.validar()
        self.assertTrue(ok, msg)

    def test_arvore_vazia(self):
        t = self.novo()
        self.assertEqual(len(t), 0)
        self.assertEqual(t.height(), 0)
        self.assertEqual(t.inorder(), [])
        self.assertFalse(t.search(1))
        self.assertFalse(t.delete(1))
        self.valida(t)

    def test_um_elemento(self):
        t = self.novo([42])
        self.assertEqual(t.height(), 1)
        self.assertTrue(t.search(42))
        self.assertEqual(t.inorder(), [42])
        self.valida(t)
        self.assertTrue(t.delete(42))
        self.assertEqual(len(t), 0)
        self.assertEqual(t.inorder(), [])
        self.valida(t)

    def _insere_validando(self, chaves):
        t = self.Tree()
        for k in chaves:
            self.assertTrue(t.insert(k))
            self.valida(t)
        self.assertEqual(t.inorder(), sorted(chaves))
        return t

    def test_insercao_crescente(self):
        t = self._insere_validando(list(range(1, 501)))
        self.assertLessEqual(t.height(), 2 * 9 + 2) 

    def test_insercao_decrescente(self):
        t = self._insere_validando(list(range(500, 0, -1)))
        self.assertLessEqual(t.height(), 2 * 9 + 2)

    def test_insercao_nao_ordenada(self):
        rnd = random.Random(7)
        self._insere_validando(rnd.sample(range(10000), 500))

    def test_valor_repetido_rejeitado(self):
        t = self.novo([10, 5, 15])
        antes = t.inorder()
        self.assertFalse(t.insert(10))
        self.assertEqual(len(t), 3)
        self.assertEqual(t.inorder(), antes)
        self.valida(t)

    def test_busca_existentes_e_inexistentes(self):
        t = self.novo([50, 30, 70, 20, 40, 60, 80])
        for k in (50, 30, 70, 20, 40, 60, 80):
            self.assertTrue(t.search(k))
        for k in (0, 25, 55, 100, -3):
            self.assertFalse(t.search(k))

    def test_remocao_folha(self):
        t = self.novo([50, 30, 70, 20, 40, 60, 80])
        self.assertTrue(t.delete(20))
        self.assertFalse(t.search(20))
        self.assertEqual(t.inorder(), [30, 40, 50, 60, 70, 80])
        self.valida(t)

    def test_remocao_um_filho(self):
        t = self.novo([50, 30, 70, 20, 60, 80, 10]) 
        self.assertTrue(t.delete(20))
        self.assertEqual(t.inorder(), [10, 30, 50, 60, 70, 80])
        self.valida(t)

    def test_remocao_dois_filhos(self):
        t = self.novo([50, 30, 70, 20, 40, 60, 80])
        self.assertTrue(t.delete(30))
        self.assertEqual(t.inorder(), [20, 40, 50, 60, 70, 80])
        self.valida(t)

    def test_remocao_da_raiz(self):
        t = self.novo([50, 30, 70, 20, 40, 60, 80])
        self.assertTrue(t.delete(50))
        self.assertFalse(t.search(50))
        self.assertEqual(t.inorder(), [20, 30, 40, 60, 70, 80])
        self.valida(t)

    def test_remocao_inexistente(self):
        t = self.novo([10, 20, 30])
        antes = t.inorder()
        self.assertFalse(t.delete(99))
        self.assertEqual(t.inorder(), antes)
        self.assertEqual(len(t), 3)
        self.valida(t)

    def test_remove_todos(self):
        chaves = random.Random(3).sample(range(1000), 200)
        t = self.novo(chaves)
        random.Random(4).shuffle(chaves)
        for k in chaves:
            self.assertTrue(t.delete(k))
            self.valida(t)
        self.assertEqual(len(t), 0)
        self.assertEqual(t.height(), 0)

    def test_operacoes_mistas_aleatorias(self):
        rnd = random.Random(2024)
        t, ref = self.Tree(), set()
        for _ in range(3000):
            k = rnd.randint(0, 150)
            if rnd.random() < 0.55:
                self.assertEqual(t.insert(k), k not in ref)
                ref.add(k)
            else:
                self.assertEqual(t.delete(k), k in ref)
                ref.discard(k)
            self.valida(t)
            self.assertEqual(t.inorder(), sorted(ref))
            self.assertEqual(len(t), len(ref))

    def test_altura_logaritmica(self):
        import math
        n = 2000
        t = self.novo(range(n))
        self.assertLessEqual(t.height(), 2 * math.log2(n + 1))


class TestAVL(_Comum, unittest.TestCase):
    Tree = AVLTree

    def test_rotacao_simples_LL(self):
        t = self.novo([30, 20, 10])
        self.assertEqual(t.root.key, 20)
        self.assertEqual((t.rot_dir, t.rot_esq, t.duplas), (1, 0, 0))

    def test_rotacao_simples_RR(self):
        t = self.novo([10, 20, 30])
        self.assertEqual(t.root.key, 20)
        self.assertEqual((t.rot_esq, t.rot_dir, t.duplas), (1, 0, 0))

    def test_rotacao_dupla_LR(self):
        t = self.novo([30, 10, 20])
        self.assertEqual(t.root.key, 20)
        self.assertEqual((t.rotacoes, t.duplas), (2, 1))

    def test_rotacao_dupla_RL(self):
        t = self.novo([10, 30, 20])
        self.assertEqual(t.root.key, 20)
        self.assertEqual((t.rotacoes, t.duplas), (2, 1))


class TestRubroNegra(_Comum, unittest.TestCase):
    Tree = RedBlackTree

    def test_raiz_sempre_preta(self):
        t = self.novo([10])
        self.assertEqual(t.root.color, "B")

    def test_recoloracao_tio_vermelho(self):
        t = self.novo([10, 5, 15, 1])  # 1 entra com pai e tio vermelhos
        self.assertEqual(t.rotacoes, 0)
        self.assertEqual(t.root.color, "B")
        self.assertEqual(t.root.left.color, "B")
        self.assertEqual(t.root.right.color, "B")
        self.assertEqual(t.root.left.left.color, "R")

    def test_rotacao_e_recoloracao(self):
        t = self.novo([10, 20, 30])
        self.assertEqual(t.root.key, 20)
        self.assertEqual(t.root.color, "B")
        self.assertEqual(t.root.left.color, "R")
        self.assertEqual(t.root.right.color, "R")
        self.assertEqual(t.rotacoes, 1)

    def test_altura_negra_consistente(self):
        t = self.novo(range(1, 200))
        self.valida(t)
        self.assertGreaterEqual(t.black_height(), 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
