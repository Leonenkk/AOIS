from .mccluskey_calc import select_essential_calc,eliminate_redundant_implicants,quine_mccluskey_tabular
from .translate import bin_to_lits,absorb_clauses

def minimize_tab_dnf(minterms, n_vars, vars_):
    print("\n==== Минимизация СДНФ (расчётно-табличный метод) ====")
    prime = quine_mccluskey_tabular(minterms, n_vars, vars_, is_dnf=True)
    need = select_essential_calc(prime, minterms, n_vars, vars_, is_dnf=True)
    need = eliminate_redundant_implicants(need, minterms, n_vars)
    result = []
    for x in need:
        result.append("(" + bin_to_lits(x, vars_, True) + ")")
    minimized = " ∨ ".join(result)
    print("\nРЕЗУЛЬТАТ (табличный метод, СДНФ): " + minimized)
    return minimized

def minimize_tab_cnf(maxterms, n_vars, vars_):
    print("\n==== Минимизация СКНФ (расчётно-табличный метод) ====")
    prime = quine_mccluskey_tabular(maxterms, n_vars, vars_, is_dnf=False)
    need = select_essential_calc(prime, maxterms, n_vars, vars_, is_dnf=False)
    need = eliminate_redundant_implicants(need, maxterms, n_vars)
    need = absorb_clauses(need, vars_, is_dnf=False)
    result = []
    for x in need:
        result.append("(" + bin_to_lits(x, vars_, False) + ")")
    minimized = " ∧ ".join(result)
    print("\nРЕЗУЛЬТАТ (табличный метод, СКНФ): " + minimized)
    return minimized

def displayKMap(newGrid, newRowLabels, newColLabels):
    if newColLabels:
        print("         " + "  ".join(f"{lbl:12}" for lbl in newColLabels))
    for idx, newRow in enumerate(newGrid):
        if newRowLabels:
            print(f"{newRowLabels[idx]:12} " + "  ".join(f"{cell:12}" for cell in newRow))
        else:
            print("".join(str(cell) for cell in newRow))
