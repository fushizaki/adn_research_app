from algo import main

def test_insertions():
    with open("algo/data/lapin.adn") as file_adn:
        sequences = file_adn.read()
        sequences_mutations_insertions = main.mutation_par_insertion(sequences, 1)
        assert len(sequences_mutations_insertions) >= len(sequences)

def test_deletion():
    with open("algo/data/lapin.adn") as file_adn:
        sequences = file_adn.read()
        sequences_mutatutions_deletion = main.mutation_par_deletion(sequences, 1)
        assert len(sequences_mutatutions_deletion) <= len(sequences)

def test_remplacement():
    with open("algo/data/lapin.adn") as file_adn:
        sequences = file_adn.read()
        sequences_mutations_remplacement = main.simuler_mutations_remplacements(sequences, 1)
        assert len(sequences_mutations_remplacement) == len(sequences) and sequences_mutations_remplacement != sequences