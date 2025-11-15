import random
import math
from . import constants
from algo import Espece


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
            restes_bases = constants.bases.copy()
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
            res += random.choice(constants.bases)  
        res += nucleotide  

    if random.random() < p:
        res += random.choice(constants.bases)
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
            tableau_d[i][j] = min(tableau_d[i - 1][j] + 1,
                                  tableau_d[i][j - 1] + 1,
                                  tableau_d[i - 1][j - 1] + cout_substitution)
    return tableau_d[len_seq1][len_seq2]


def generer_sequence_adn_aleatoirement(bases: list, longeur: int) -> str:
    """Genère une sequence adn aléatoirement a partir d'une base donnée
        en paramètre

    Args:
        constants.bases (list): les constants.bases qui vont constituer l'ADN
        longeur (int): la longeur de la séquence à génerer

    Returns:
        str: la séquence générée
    """

    sequence_aleatoire = ""
    for i in range(longeur):
        sequence_aleatoire += random.choice(constants.bases)
    return sequence_aleatoire

def estimation_distance_mutation(echantillon1: str, echantillion2: str) -> int:
    """Calcule la distance entre deux échantillon en se basant 
        sur les mutations de remplacement

    Args:
        echantillon1 (str): l'echantillon 1
        echantillion2 (str): l'échantillon 2 

    Returns:
        int: la distance entre les deux échantillons
    """
    
    distance = 0
    
    for base in range(len(echantillon1)):
        if echantillon1[base] != echantillion2[base]:
            distance += 1
    
    return distance

def calculer_distance(espece1: Espece, espece2: Espece) -> int:
    """Calcule la distance entre deux espèces en fonction de leur statut (hypothétique ou avérée).
    Args:
        espece1 (Espece): une espèce hypothétique 
        espece2 (Espece): une espèce soit hypothétique soit avérée  

    Returns:
        int: la distance entre les deux espèces
    """
    
    if espece1.est_hypothetique and espece2.est_averee():
        espece1_filles = espece1.get_especes_filles()
        somme_dist = 0

        for e in espece1_filles:
            somme_dist += distance_de_levenshtein(espece1.sequence_adn, e.sequence_adn)
        moyenne = somme_dist / len(espece1_filles)
        return moyenne

    if espece1.est_hypothetique and espece2.est_hypothetique:
        espece1_filles = espece1.get_especes_filles()
        espece2_filles = espece2.get_especes_filles()
        somme_dist = 0

        for e1 in espece1_filles:
            for e2 in espece2_filles:
                somme_dist += distance_de_levenshtein(e1.sequence_adn ,e2.sequence_adn)
        moyenne = somme_dist / len(espece1_filles) * len(espece2_filles)
        return moyenne

def reconstruction_arbre_phylogenetique(liste_fichier_adn):
    """Construit un arbre phylogénétique à partir de fichiers adn

    Args:
        liste_fichier_adn (str): les chemiens vers les fichiers adn

    Returns:
        Espece: l'espèce à la racine de l'arbre, qui contient l'arbre phylogénétique 
    """
    les_especes = []
    sequence_adn = ""
    nom_espece = ""
    count = 0
    dist_min = None
    
    if(liste_fichier_adn == []):
        return None
    
    for adn_file in liste_fichier_adn:
        nom_espece = adn_file.replace(".", "/").split("/")[-2]
        sequence_adn = open(adn_file)
        les_especes.append(Espece(nom_espece, sequence_adn.read(), False, None))
        
    while len(les_especes) >= 2:
        dist_min = None
        paire_min = None

        for esp_count1 in range(len(les_especes)):
            for esp_count2 in range(esp_count1+1, len(les_especes)):
                espece_a = les_especes[esp_count1]
                espece_b = les_especes[esp_count2]

                if(espece_a.est_averee() and espece_b.est_averee()):
                    dist = distance_de_levenshtein(espece_a.sequence_adn, espece_b.sequence_adn)
                else:
                    if(espece_a.est_hypothetique):
                        dist = calculer_distance(espece_a, espece_b)

                    if(espece_b.est_hypothetique):
                        dist = calculer_distance(espece_b, espece_a)
                    
                if dist_min is None or dist < dist_min:
                    dist_min = dist
                    paire_min = (espece_a, espece_b)

        if paire_min:
            esp_a, esp_b = paire_min
            esp_hypo = Espece(f"EspeceHypothetique_{count}", '', True, [esp_a, esp_b])

            les_especes.remove(esp_a)
            les_especes.remove(esp_b)
            les_especes.append(esp_hypo)

            count += 1

    racine = les_especes[0] 
    return racine   