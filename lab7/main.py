class DiagonalMatrix:
    def __init__(self, size=16):
        # Initialize a size x size zero matrix
        self.size = size
        self.matrix = [[0] * size for _ in range(size)]

    def initialize_from_list(self, data):
        # Validate dimensions
        if len(data) != self.size or any(len(row) != self.size for row in data):
            raise ValueError(f"Input data must be {self.size}x{self.size}")
        # Deep copy
        self.matrix = [list(row) for row in data]

    def read_word(self, j):
        # Read the j-th "diagonal" word: elements along column j shifted down-right by j
        return [ self.matrix[(i + j) % self.size][j] for i in range(self.size) ]

    def read_column(self, j):
        # Read the "address" column j: take bit j from each diagonal word
        return [ self.read_word(k)[j] for k in range(self.size) ]

    def write_word(self, j, word):
        # Write a full-size word at diagonal position j (inverse of read_word)
        if len(word) != self.size:
            raise ValueError(f"Word length must be {self.size}")
        for i in range(self.size):
            self.matrix[(i + j) % self.size][j] = word[i]

    def apply_logical_function(self, func, word1, word2=None):
        # Four functions for Variant 1: f1 (AND), f3 (OR), f12 (XOR), f14 (NOT)
        if func == "f1":
            return [a & b for a, b in zip(word1, word2)]
        if func == "f3":
            return [a | b for a, b in zip(word1, word2)]
        if func == "f12":
            return [a ^ b for a, b in zip(word1, word2)]
        if func == "f14":
            return [1 - a for a in word1]
        raise ValueError(f"Unknown function {func}")

    def find_nearest(self, reference_index, target_word=None, direction="top"):  # corrected
        # If no target_word provided, use word at reference_index
        if target_word is None:
            target_word = self.read_word(reference_index)
        # Search above: decreasing indices
        if direction == "top":
            for offset in range(1, self.size):
                j = (reference_index - offset) % self.size
                if self.read_word(j) == target_word:
                    return j
        # Search below: increasing
        elif direction == "bottom":
            for offset in range(1, self.size):
                j = (reference_index + offset) % self.size
                if self.read_word(j) == target_word:
                    return j
        else:
            raise ValueError("direction must be 'top' or 'bottom'")
        return -1

    def add_aj_bj(self, V):
        # For each word j whose first 3 bits equal V, sum A (bits 3-6) and B (7-10), store 5-bit result in S (11-15)
        for j in range(self.size):
            word = self.read_word(j)
            if word[:3] == V:
                Aj = int(''.join(map(str, word[3:7])), 2)
                Bj = int(''.join(map(str, word[7:11])), 2)
                S_new = Aj + Bj
                S_bits = list(map(int, f"{S_new:05b}"))
                new_word = word[:3] + word[3:7] + word[7:11] + S_bits
                self.write_word(j, new_word)

    def print_matrix(self, title="Matrix"):
        print(f"\n{title}:")
        for row in self.matrix:
            print(' '.join(map(str, row)))
