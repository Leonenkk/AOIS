class DiagonalMatrix:
    def __init__(self, size=16):
        self.size = size
        self.matrix = [[0] * size for _ in range(size)]

    def initialize_from_list(self, data):
        if len(data) != self.size or any(len(row) != self.size for row in data):
            raise ValueError(f"Input data must be {self.size}x{self.size}")
        self.matrix = [list(row) for row in data]

    def read_word(self, j):
        return [self.matrix[(i + j) % self.size][j] for i in range(self.size)]

    def read_column(self, j):
        return [self.read_word(k)[j] for k in range(self.size)]

    def write_word(self, j, word):
        if len(word) != self.size:
            raise ValueError(f"Word length must be {self.size}")
        for i in range(self.size):
            self.matrix[(i + j) % self.size][j] = word[i]

    def apply_logical_function(self, func, word1, word2=None):
        if func == "f1":
            return [a & b for a, b in zip(word1, word2)]
        elif func == "f3":
            return [a | b for a, b in zip(word1, word2)]
        elif func == "f12":
            return [a ^ b for a, b in zip(word1, word2)]
        elif func == "f14":
            return [1 - a for a in word1]
        raise ValueError(f"Unknown function {func}")

    def find_nearest(self, reference_index, direction="top"):
        target_word = self.read_word(reference_index)
        nearest_index = -1
        min_distance = float('inf')

        # Проверяем все столбцы, кроме reference_index
        for j in range(self.size):
            if j == reference_index:
                continue
            if self.read_word(j) == target_word:
                # Вычисляем "циклическое" расстояние между индексами
                distance = (j - reference_index) % self.size

                if direction == "top":
                    # Для "top" ищем минимальное расстояние влево (j < reference_index)
                    if distance > (self.size // 2):
                        continue  # Пропускаем индексы справа
                    if distance < min_distance:
                        min_distance = distance
                        nearest_index = j
                elif direction == "bottom":
                    # Для "bottom" ищем минимальное расстояние вправо (j > reference_index)
                    if distance <= (self.size // 2):
                        continue
                    adjusted_distance = self.size - distance
                    if adjusted_distance < min_distance:
                        min_distance = adjusted_distance
                        nearest_index = j

        return nearest_index

    def add_aj_bj(self, V):
        for j in range(self.size):
            word = self.read_word(j)
            if word[:3] == V:
                Aj = int(''.join(map(str, word[3:7])), 2)
                Bj = int(''.join(map(str, word[7:11])), 2)
                S_new = Aj + Bj
                S_bits = list(map(int, f"{S_new:05b}"))[-5:]

                Aj_bits = list(map(int, f"{Aj:04b}"))
                Bj_bits = list(map(int, f"{Bj:04b}"))
                new_word = word[:3] + Aj_bits + Bj_bits + S_bits
                self.write_word(j, new_word)

    def print_matrix(self, title="Matrix"):
        print(f"\n{title}:")
        for row in self.matrix:
            print(' '.join(map(str, row)))