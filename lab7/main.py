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

    def int_to_bits(self, num, bits=16):
        return list(map(int, f"{num:0{bits}b}"))[-bits:]

    def compute_gl(self, A_word):
        g = [0] * self.size
        l = [0] * self.size
        for j in range(self.size):
            S_word = self.read_word(j)
            g_current = 0
            l_current = 0
            for i in reversed(range(16)):  # Сравнение с старшего бита (i=15)
                a_i = A_word[i]
                s_i = S_word[i]
                g_prev = g_current
                l_prev = l_current
                g_current = g_prev | (a_i & ~s_i & ~l_prev)
                l_current = l_prev | (~a_i & s_i & ~g_prev)
            g[j] = g_current
            l[j] = l_current
        return g, l

    def find_nearest(self, A_value, direction="top"):
        A_word = self.int_to_bits(A_value)
        g, l = self.compute_gl(A_word)

        candidates = []
        for j in range(self.size):
            S_value = self._word_to_int(self.read_word(j))
            if direction == "top" and l[j] and not g[j]:
                candidates.append((j, S_value))
            elif direction == "bottom" and g[j] and not l[j]:
                candidates.append((j, S_value))

        if not candidates:
            return -1

        if direction == "top":
            nearest = max(candidates, key=lambda x: x[1])
        else:
            nearest = min(candidates, key=lambda x: x[1])

        return nearest[0]

    def _word_to_int(self, word):
        return int(''.join(map(str, word)), 2)


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