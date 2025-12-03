from algo import main

def test_distance_levenshtein():
    sequence1 = "AGCT"
    sequence2 = "AGT"
    assert main.distance_de_levenshtein(sequence1, sequence2) == 1

def test_distance_levenshtein_identique():
    sequence1 = "AGCT"
    sequence2 = "AGCT"
    assert main.distance_de_levenshtein(sequence1, sequence2) == 0

def test_distance_levenshtein_vide():
    sequence1 = ""
    sequence2 = "AGCT"
    assert main.distance_de_levenshtein(sequence1, sequence2) == 4

def test_distance_mutation():
    sequence1 = "AGCTAGCTAGCT"
    sequence2 = main.simuler_mutations_remplacements(sequence1, 0.5)
    distance = main.estimation_distance_mutation(sequence1, sequence2)
    assert distance >= 0 and distance <= len(sequence1)