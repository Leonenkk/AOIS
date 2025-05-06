class HashTableEntry:
    def __init__(self):
        self.ID = None       # Ключевое слово
        self.C = 0           # Флажок коллизии
        self.U = 0           # Флажок занятости
        self.T = 0           # Терминальный флажок
        self.L = 0           # Флажок связи
        self.D = 0           # Флажок удаления
        self.P0 = None       # Указатель следующей ячейки
        self.Pi = None       # Данные или указатель
        self.V = None        # Числовое значение ключа
        self.h = None        # Хеш-адрес

class SportsHashTable:
    def __init__(self, size=20):
        self.size = size
        self.table = [HashTableEntry() for _ in range(size)]
        self.alphabet = {
            **{chr(i): i - 1040 for i in range(1040, 1072)},  # А-Я без Ё
            'Ё': 6,  # Ё после Е (Е=5, Ё=6)
            'ё': 6
        }
        self.external_data = {}  # Внешнее хранилище данных

    def _validate_keyword(self, keyword):
        if not keyword or not isinstance(keyword, str):
            raise ValueError("Некорректное ключевое слово")

    def _update_chain(self, start_idx, new_idx):
        """Обновление цепочки коллизий"""
        current = start_idx
        while self.table[current].P0 is not None:
            current = self.table[current].P0
        self.table[current].T = 0
        self.table[current].P0 = new_idx

    def calculate_V(self, keyword):
        """Вычисление V по первым двум буквам"""
        self._validate_keyword(keyword)
        first = self.alphabet.get(keyword[0].upper(), 0)
        second = self.alphabet.get(keyword[1].upper(), 0) if len(keyword) > 1 else 0
        return first * 33 + second

    def hash_function(self, V):
        return V % self.size

    def _find_free_slot(self, start_idx):
        """Линейный пробинг для поиска свободной ячейки"""
        idx = start_idx
        for _ in range(self.size):
            if self.table[idx].U == 0 or self.table[idx].D == 1:
                return idx
            idx = (idx + 1) % self.size
        raise OverflowError("Таблица переполнена")

    def insert(self, keyword, data):
        """Добавление записи с проверкой уникальности"""
        if self.search(keyword):
            raise ValueError(f"Ключ '{keyword}' уже существует")

        V = self.calculate_V(keyword)
        h = self.hash_function(V)

        # Обработка коллизий
        if self.table[h].U == 1 and self.table[h].D == 0:
            new_idx = self._find_free_slot(h)
            self._update_chain(h, new_idx)
            self._insert_entry(new_idx, keyword, data, V, h)
            self.table[h].C = 1
            self.table[h].T = 0
            self.table[h].P0 = new_idx
        else:
            self._insert_entry(h, keyword, data, V, h)

    def _insert_entry(self, idx, keyword, data, V, h):
        """Вставка данных в ячейку"""
        entry = self.table[idx]
        entry.ID = keyword
        entry.V = V
        entry.h = h  # Явное сохранение хеш-адреса
        entry.U = 1
        entry.D = 0
        entry.T = 1
        entry.C = 0

        # Обработка длинных данных
        if len(data) > 20:
            ext_key = f"EXT_{keyword}"
            self.external_data[ext_key] = data
            entry.Pi = ext_key
            entry.L = 1
        else:
            entry.Pi = data
            entry.L = 0

    def search(self, keyword):
        """Поиск игнорирует флаг C, проверяет всю цепочку"""
        V = self.calculate_V(keyword)
        h = self.hash_function(V)
        current = h
        while current is not None:
            entry = self.table[current]
            if entry.U == 1 and entry.D == 0 and entry.ID == keyword:
                return entry
            current = entry.P0
        return None

    def delete(self, keyword):
        """Удаление записи с перестройкой цепочек"""
        entry = self.search(keyword)
        if not entry:
            raise KeyError(f"Ключ '{keyword}' не найден")

        entry.D = 1
        entry.U = 0
        self._rebuild_chain(entry.h)

    def _rebuild_chain(self, start_idx):
        """Перестройка цепочки после удаления"""
        prev = None
        current = start_idx
        new_chain_start = None

        while current is not None:
            entry = self.table[current]
            next_entry = entry.P0

            if entry.D == 1:
                # Удаляем ссылку на текущий элемент
                if prev:
                    prev.P0 = next_entry
                # Сбрасываем флаги удаленного элемента
                entry.P0 = None
                entry.T = 0
            else:
                # Обновляем начало новой цепочки
                if new_chain_start is None:
                    new_chain_start = current
                prev = current

            current = next_entry

        # Обновляем терминальный флажок
        if prev:
            self.table[prev].T = 1
        else:
            # Если цепочка пуста, сбрасываем флаг коллизии
            self.table[start_idx].C = 0

    def update(self, keyword, new_data):
        """Обновление данных записи"""
        entry = self.search(keyword)
        if not entry:
            raise KeyError(f"Ключ '{keyword}' не найден")

        if len(new_data) > 20:
            ext_key = f"EXT_{keyword}"
            self.external_data[ext_key] = new_data
            entry.Pi = ext_key
            entry.L = 1
        else:
            entry.Pi = new_data
            entry.L = 0

    def print_table(self):
        """Визуализация таблицы с отображением всех флагов"""
        print(f"{'Индекс':<6} | {'ID':<15} | {'V':<4} | {'h':<2} | {'C':<1} | {'U':<1} | {'T':<1} | {'L':<1} | {'D':<1} | {'P0':<3} | {'Данные':<30}")
        print("-" * 110)
        for idx, entry in enumerate(self.table):
            if entry.D == 1:
                data = "[УДАЛЕНО]"
                entry_id = "[УДАЛЕНО]"
            else:
                data = self.external_data.get(entry.Pi, entry.Pi) if entry.L == 1 else entry.Pi
                entry_id = entry.ID or ""
            print(
                f"{idx:<6} | {entry_id:<15} | {entry.V or '':<4} | {entry.h or '':<2} | "
                f"{entry.C:<1} | {entry.U:<1} | {entry.T:<1} | {entry.L:<1} | {entry.D:<1} | "
                f"{entry.P0 or '':<3} | {str(data)[:30]:<30}"
            )
