import os
import tempfile
import pytest
from algo import main

def test_sauvegarder_sequence_file_exists():
    with tempfile.TemporaryDirectory() as temp_dir:
        data_dir = os.path.join(temp_dir, "data")
        sequence = "ATCGATCG"
        nom_fichier = "test_sequence"
        main.sauvegarder_sequence(sequence, nom_fichier, dossier=data_dir)
        assert os.path.exists(os.path.join(data_dir, f"{nom_fichier}.adn"))