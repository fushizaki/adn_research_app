import pytest
from algo.Espece import Espece

def test_init():
    espece = Espece("Homo sapiens", "ATCG", False, None)
    assert espece.nom == "Homo sapiens"
    assert espece.sequence_adn == "ATCG"
    assert espece.est_hypothetique == False
    assert espece.especes_filles == []

def test_init_with_especes_filles():
    fille = Espece("Fille", "GCTA", True, [])
    espece = Espece("Parent", "ATCG", True, [fille])
    assert espece.especes_filles == [fille]

def test_est_averee_true():
    espece = Espece("Test", "ATCG", False, [])
    assert espece.est_averee() == True

def test_est_averee_false():
    espece = Espece("Test", "ATCG", True, [])
    assert espece.est_averee() == False

def test_est_hypothetique_true():
    espece = Espece("Test", "ATCG", True, [])
    assert espece.get_est_hypothetique() == True

def test_est_hypothetique_false():
    espece = Espece("Test", "ATCG", False, [])
    assert espece.get_est_hypothetique() == False

def test_add_espece_fille_hypothetique():
    parent = Espece("Parent", "ATCG", True, [])
    fille = Espece("Fille", "GCTA", False, [])
    parent.add_espece_fille(fille)
    assert fille in parent.especes_filles

def test_add_espece_fille_averee():
    parent = Espece("Parent", "ATCG", False, [])
    fille = Espece("Fille", "GCTA", False, [])
    parent.add_espece_fille(fille)
    assert fille not in parent.especes_filles

def test_del_espece_fille():
    fille = Espece("Fille", "GCTA", False, [])
    parent = Espece("Parent", "ATCG", True, [fille])
    parent.del_espece_fille(fille)
    assert fille not in parent.especes_filles

def test_del_espece_fille_not_exists():
    parent = Espece("Parent", "ATCG", True, [])
    fille = Espece("Fille", "GCTA", False, [])
    with pytest.raises(ValueError):
        parent.del_espece_fille(fille)

def test_get_adn():
    espece = Espece("Test", "ATCGAAAA", False, [])
    assert espece.get_adn() == "ATCGAAAA"

def test_get_especes_filles():
    fille1 = Espece("Fille1", "GCTA", False, [])
    fille2 = Espece("Fille2", "TTTT", False, [])
    parent = Espece("Parent", "ATCG", True, [fille1, fille2])
    assert parent.get_especes_filles() == [fille1, fille2]

def test_str():
    fille = Espece("Fille", "GCTA", False, [])
    parent = Espece("Parent", "ATCG", True, [fille])
    str_attendu = "Espece(nom=Parent, sequence_adn=ATCG, est_hypothetique=True, especes_filles=['Fille'])"
    assert str(parent) == str_attendu