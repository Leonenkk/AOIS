import unittest
import io
import sys
from main import SportsHashTable, HashTableEntry

class TestSportsHashTable(unittest.TestCase):
    def setUp(self):
        # small size to force collisions
        self.ht = SportsHashTable(size=5)

    def test_calculate_V_and_hash(self):
        # 'A' is Latin not in alphabet -> maps to 0
        v = self.ht.calculate_V('АБ')  # Cyrillic A (А) and B (Б)
        # Alphabet: 'А' -> 0, 'Б'->1 so V=0*33+1
        self.assertEqual(v, 1)
        idx = self.ht.hash_function(v)
        self.assertEqual(idx, 1 % self.ht.size)

    def test_insert_and_search_short_data(self):
        self.ht.insert('Тест', 'data')
        entry = self.ht.search('Тест')
        self.assertIsNotNone(entry)
        self.assertEqual(entry.ID, 'Тест')
        self.assertEqual(entry.Pi, 'data')
        self.assertEqual(entry.L, 0)

    def test_insert_and_search_long_data(self):
        long_data = 'x' * 25
        self.ht.insert('Ключ', long_data)
        entry = self.ht.search('Ключ')
        self.assertIsNotNone(entry)
        ext_key = f"EXT_Ключ"
        self.assertEqual(entry.Pi, ext_key)
        self.assertEqual(entry.L, 1)
        self.assertIn(ext_key, self.ht.external_data)
        self.assertEqual(self.ht.external_data[ext_key], long_data)


    def test_update(self):
        self.ht.insert('Ключ2', 'short')
        self.ht.update('Ключ2', 'new')
        e = self.ht.search('Ключ2')
        self.assertEqual(e.Pi, 'new')
        # Update to long
        long_val = 'y' * 30
        self.ht.update('Ключ2', long_val)
        e2 = self.ht.search('Ключ2')
        ext_key = f"EXT_Ключ2"
        self.assertEqual(e2.Pi, ext_key)
        self.assertIn(ext_key, self.ht.external_data)
        self.assertEqual(self.ht.external_data[ext_key], long_val)

    def test_invalid_insert_search_delete(self):
        with self.assertRaises(ValueError):
            self.ht.insert('', 'data')
        with self.assertRaises(ValueError):
            self.ht.calculate_V(123)
        self.assertIsNone(self.ht.search('НеСуществует'))
        with self.assertRaises(KeyError):
            self.ht.delete('НеСуществует')
        with self.assertRaises(KeyError):
            self.ht.update('НеСуществует', 'x')

    def test_print_table_outputs(self):
        # Insert one and capture print
        self.ht.insert('Спорт', 'game')
        buf = io.StringIO()
        sys_stdout = sys.stdout
        sys.stdout = buf
        try:
            self.ht.print_table()
        finally:
            sys.stdout = sys_stdout
        output = buf.getvalue()
        self.assertIn('Спорт', output)
        self.assertIn('game', output)
        self.assertIn('Индекс', output)

    def test_rebuild_chain_minimal(self):
        self.ht.calculate_V = lambda kw: 2
        self.ht.insert('Solo', 'one')
        idx = self.ht.hash_function(2)
        entry = self.ht.table[idx]
        self.assertEqual(entry.ID, 'Solo')
        self.ht.delete('Solo')
        self.assertIsNone(self.ht.search('Solo'))
        entry_after = self.ht.table[idx]
        self.assertEqual(entry_after.U, 0)
        self.assertEqual(entry_after.D, 1)

if __name__ == '__main__':
    unittest.main()
