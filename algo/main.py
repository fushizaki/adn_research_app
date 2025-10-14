def sauvegarder_sequence(sequence: str, nom_fichier: str) -> None:
    """
    Sauvegarde une séquence ADN dans un fichier .adn
    
    Args:
        sequence (str): La séquence ADN à sauvegarder
        nom_fichier (str): Le nom du fichier (sans extension)
    """
    with open(f"./data/{nom_fichier}.adn", 'w') as fichier:
        fichier.write(sequence)
    print(f"Séquence sauvegardée dans {nom_fichier}.adn")