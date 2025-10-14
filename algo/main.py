import random
from constants import *

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