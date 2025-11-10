import random
import math

from constants import *


def sauvegarder_sequence(sequence: str, nom_fichier: str) -> None:
    """
    Sauvegarde une séquence ADN dans un fichier .adn
    
    Args:
        sequence (str): La séquence ADN à sauvegarder
        nom_fichier (str): Le nom du fichier (sans extension)
    """
    try:
        with open(f"./data/{nom_fichier}.adn", 'w') as fichier:
            fichier.write(sequence)
        print(f"Séquence sauvegardée dans {nom_fichier}.adn")
    except OSError:
        print(f"Erreur lors de la sauvegarde du fichier : {nom_fichier}")
        

def simuler_mutations_remplacements(sequence: str, p: float) -> str:
    """Simule des mutations par remplacement dans une séquence ADN.

    Args:
        sequence (str): sequence 
        p (float): probabilité qu'une mutation se fasse

    Returns:
        str: sequence avec mutation
    """
    sequence_mutation = ""
    if p < 0 or p > 1:
        raise ValueError("Valeur de p pas comprise entre 0 et 1")
    for base in sequence:
        if random.random() < p:
            restes_bases = bases.copy()
            restes_bases.remove(base)
            nouvelle_base = random.choice(restes_bases)
            sequence_mutation += nouvelle_base
        else:
            sequence_mutation += base
    return sequence_mutation


def mutation_par_insertion(sequence: str, p: float) -> str:
    """Mutation obtenue par intégration d'un ou plusieurs nucléotides dans une séquence

    Args:
        sequence(str) : une sequence adn
        p (float) : probabilité qu'une mutation ait lieu

    Returns:
        str_: une sequence avec mutation d'insertion
    """
    res = ""

    if p < 0 or p > 1: 
        raise ValueError("Valeur de p impossibles : doit être comprit entre 0 et 1")
    
    for nucleotide in sequence:
        if random.random() < p:
            res += random.choice(bases)  
        res += nucleotide  

    if random.random() < p:
        res += random.choice(bases)
    return res


def mutation_par_deletion(sequence: str, p: float) -> str:
    """Mutation obtenue par suppression d'un nucléotide dans une séquence

    Args:
        sequence(str) : une sequence adn
        p (float) : probabilité qu'une mutation ait lieu

    Returns:
        str_: une sequence ADN
    """
    res = ""

    if p < 0 or p > 1: 
        raise ValueError("Valeur de p impossibles : doit être comprit entre 0 et 1")
    
    for nucleotide in sequence:
        if random.random() > p:
            res += nucleotide
    return res


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
    tableau_d = [[0] * (len_seq2 + 1) for _ in range(len_seq1 + 1)]
    for i in range(len_seq1 + 1):
        tableau_d[i][0] = i
    for j in range(len_seq2 + 1):
        tableau_d[0][j] = j
    for i in range(1, len_seq1 + 1):
        for j in range(1, len_seq2 + 1):
            if seq1[i - 1] == seq2[j - 1]:
                cout_substitution = 0
            else:
                cout_substitution = 1
            tableau_d[i][j] = min(tableau_d[i - 1][j] + 1, tableau_d[i][j - 1] + 1,
                          tableau_d[i - 1][j - 1] + cout_substitution)
    return tableau_d[len_seq1][len_seq2]
