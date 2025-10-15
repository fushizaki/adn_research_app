# Implémentation littérale de l'algorithme de Levenshtein depuis Wikipédia
def distance_de_levenshtein(seq1: str, seq2: str) -> int:
    """Calcule la distance de Levenshtein entre deux séquences.

    Args:
        seq1 (str): La première séquence
        seq2 (str): La deuxième séquence

    Returns:
        int: La distance de Levenshtein entre les deux séquences
    """
    len_seq1 = len(seq1)
    len_seq2 = len(seq2)
    D = [[0] * (len_seq2 + 1) for _ in range(len_seq1 + 1)]
    for i in range(len_seq1 + 1):
        D[i][0] = i
    for j in range(len_seq2 + 1):
        D[0][j] = j
    for i in range(1, len_seq1 + 1):
        for j in range(1, len_seq2 + 1):
            if seq1[i - 1] == seq2[j - 1]:
                cout_substitution = 0
            else:
                cout_substitution = 1
            D[i][j] = min(D[i - 1][j] + 1, D[i][j - 1] + 1,
                          D[i - 1][j - 1] + cout_substitution)
    return D[len_seq1][len_seq2]