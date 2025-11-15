from algo import main
import pytest

def test_generer_sequence_adn_aleatoirement():
    bases = ['A', 'T', 'C', 'G']
    longeur = 10
    sequence = main.generer_sequence_adn_aleatoirement(bases, longeur)
    assert len(sequence) == longeur
    for base in sequence:
        assert base in bases