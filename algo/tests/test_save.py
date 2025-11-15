import os
import tempfile
import pytest
from algo import main

def test_sauvegarder_sequence_file_exists():
    with tempfile.TemporaryDirectory() as temp_dir:
        original_cwd = os.getcwd()
        os.chdir(temp_dir)
        try:
            os.makedirs("data", exist_ok=True)
            sequence = "ATCGATCG"
            nom_fichier = "test_sequence"
            main.sauvegarder_sequence(sequence, nom_fichier)
            assert os.path.exists(f"./data/{nom_fichier}.adn")
        finally:
            os.chdir(original_cwd)