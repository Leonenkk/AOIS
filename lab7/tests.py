import unittest
from main import DiagonalMatrix  # assuming your implementation is in diagonal_matrix.py

class TestDiagonalMatrix(unittest.TestCase):
    def setUp(self):
        # Use a small 4x4 matrix for basic tests
        self.data4 = [
            [1,0,0,1],
            [0,1,1,0],
            [1,1,0,0],
            [0,0,1,1]
        ]
        self.dm4 = DiagonalMatrix(size=4)
        self.dm4.initialize_from_list(self.data4)

        # Use the full 16x16 matrix for add_aj_bj test
        self.data16 = [
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [1,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0],
            [1,1,0,1,1,0,0,0,1,1,1,1,0,0,0,0],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [1,1,1,0,1,0,0,0,0,0,0,1,0,0,0,0],
            [0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,1,0,1,1,0,0,0,0,0,1,1,0,0,0],
            [0,0,0,0,1,1,0,0,0,0,0,0,1,0,0,0],
            [0,0,0,0,0,1,1,0,1,0,1,0,1,0,0,0],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1],
            [0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0],
            [0,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0],
            [0,1,0,1,0,1,0,1,0,1,0,1,0,1,1,1],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        ]
        self.dm16 = DiagonalMatrix(size=16)
        self.dm16.initialize_from_list(self.data16)

    def test_read_word(self):
        expected = [self.data4[(i+1)%4][1] for i in range(4)]
        self.assertEqual(self.dm4.read_word(1), expected)

    def test_read_column(self):
        diagonal = [self.dm4.read_word(k) for k in range(4)]
        expected = [word[2] for word in diagonal]
        self.assertEqual(self.dm4.read_column(2), expected)

    def test_write_word(self):
        new_word = [0,0,0,0]
        self.dm4.write_word(3, new_word)
        self.assertEqual(self.dm4.read_word(3), new_word)

    def test_logical_functions(self):
        w0 = self.dm4.read_word(0)
        w1 = self.dm4.read_word(1)
        # AND
        r_and = self.dm4.apply_logical_function("f1", w0, w1)
        self.assertListEqual(r_and, [a & b for a, b in zip(w0, w1)])
        # OR
        r_or  = self.dm4.apply_logical_function("f3", w0, w1)
        self.assertListEqual(r_or, [a | b for a, b in zip(w0, w1)])
        # XOR
        r_xor = self.dm4.apply_logical_function("f12", w0, w1)
        self.assertListEqual(r_xor, [a ^ b for a, b in zip(w0, w1)])
        # NOT
        r_not = self.dm4.apply_logical_function("f14", w0)
        self.assertListEqual(r_not,[1 - a for a in w0])

    def test_find_nearest(self):
        w0 = self.dm4.read_word(0)
        self.dm4.write_word(2, w0)
        self.assertEqual(self.dm4.find_nearest(0, direction="bottom"), 2)
        self.assertEqual(self.dm4.find_nearest(0, direction="top"), 2)

    def test_add_aj_bj(self):
        # Test with full 16x16 data\, V = [1,1,1]
        # Before addition, extract initial S field
        w0_before = self.dm16.read_word(0)
        # Perform Aj+Bj
        self.dm16.add_aj_bj([1,1,1])
        w0_after = self.dm16.read_word(0)
        # Expected new S bits = lower 5 bits of (A+B) for word0:
        Aj = int(''.join(map(str, w0_before[3:7])), 2)
        Bj = int(''.join(map(str, w0_before[7:11])), 2)
        sum_bits = list(map(int, f"{(Aj + Bj):05b}"))
        self.assertEqual(w0_after[11:16], sum_bits)

if __name__ == '__main__':
    unittest.main()
