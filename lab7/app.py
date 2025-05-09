from main import DiagonalMatrix

data = [
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0],
    [1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
    [0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0],
    [0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]

dm = DiagonalMatrix()
dm.initialize_from_list(data)

print("== = Исходная матрица == = ")
dm.print_matrix()

# 1) Чтение слова и адресного столбца
print("1) Чтение данных: ")
w2 = dm.read_word(2)
c3 = dm.read_column(3)
print(f"   Слово №2:           {''.join(map(str, w2))}")
print(f"   Адресный столбец №3:{''.join(map(str, c3))}")

# 2) Логические функции
print("2) Логические операции над словом №2и №3: ")
res_and = dm.apply_logical_function("f1", w2, dm.read_word(3))
res_or = dm.apply_logical_function("f3", w2, dm.read_word(3))
res_xor = dm.apply_logical_function("f12", w2, dm.read_word(3))
res_not = dm.apply_logical_function("f14", w2)
print(f"   f1 (AND) : {''.join(map(str, res_and))}")
print(f"   f3 (OR)  : {''.join(map(str, res_or))}")
print(f"   f12(XOR): {''.join(map(str, res_xor))}")
print(f"   f14(NOT): {''.join(map(str, res_not))}")

# Запись результата f1 в слово №15
dm.write_word(15, res_and)
print("После записи результата f1 в слово №15: ")
dm.print_matrix()

# 3) Арифметика Aj + Bj при V=111
print(" 3) Арифметическая операция Aj + Bj дляV = 111:")
dm.add_aj_bj([1, 1, 1])
print("После обновления полей S:")
dm.print_matrix()
print("Поле S после обновления:", dm.read_word(0)[-5:])  # [0,1,1,1,1]

# 4) Поиск ближайшего слова
A_value = 14416

# Поиск ближайшего сверху (максимальное значение < A)
nearest_top = dm.find_nearest(A_value, direction="top")

# Поиск ближайшего снизу (минимальное значение > A)
nearest_bottom = dm.find_nearest(A_value, direction="bottom")

print(f"Ближайший сверху: {nearest_top}")
print(f"Ближайший снизу: {nearest_bottom}")