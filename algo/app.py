"""
Application terminal pour tester les fonctionnalités de gestion d'espèces et d'ADN
"""

import os
from Espece import Espece
from main import (
    generer_sequence_adn_aleatoirement,
    simuler_mutations_remplacements,
    mutation_par_insertion,
    mutation_par_deletion,
    distance_de_levenshtein,
    estimation_distance_mutation,
    calculer_distance,
    sauvegarder_sequence,
    reconstruction_arbre_phylogenetique,
)
from constants import bases


def afficher_menu():
    """Affiche le menu principal de l'application."""
    print("\n" + "="*50)
    print("    APPLICATION DINOTRACK")
    print("="*50)
    print("\n[1] Generer une sequence ADN aleatoire")
    print("[2] Simuler des mutations")
    print("[3] Calculer la distance de Levenshtein")
    print("[4] Tester calculer_distance entre especes")
    print("[5] Reconstruire un arbre phylogenetique")
    print("[6] Sauvegarder une sequence")
    print("[0] Quitter")
    print("\n" + "-"*50)


def afficher_menu_mutations():
    """Affiche le sous-menu des mutations."""
    print("\n" + "="*50)
    print("    MENU MUTATIONS")
    print("="*50)
    print("\n[1] Mutation par remplacement")
    print("[2] Mutation par insertion")
    print("[3] Mutation par deletion")
    print("[0] Retour au menu principal")
    print("\n" + "-"*50)


def generer_sequence():
    """Genere une sequence ADN aleatoire."""
    try:
        longueur = int(input("\nQuelle longueur de sequence souhaitez-vous generer : "))
        if longueur <= 0:
            print("Erreur : La longueur doit etre un nombre positif.")
            return None
        
        sequence = generer_sequence_adn_aleatoirement(bases, longueur)
        print(f"\nSequence generee avec succes ({longueur} bases) :")
        print(f"   {sequence}")
        return sequence
    except ValueError:
        print("Erreur : Veuillez entrer un nombre entier valide pour la longueur.")
        return None
    except Exception as e:
        print(f"Erreur : Une erreur inattendue s'est produite lors de la generation de la sequence: {e}")
        return None


def menu_mutations():
    """Gere le sous-menu des mutations."""
    sequence = input("\nEntrez la sequence ADN a muter (ou 'G' pour en generer une) : ").strip().upper()
    
    if sequence == 'G':
        sequence = generer_sequence()
        if sequence is None:
            return
    
    if not all(base in bases for base in sequence):
        print("Erreur : La sequence contient des bases invalides. Veuillez utiliser uniquement A, T, G, C.")
        return
    
    while True:
        afficher_menu_mutations()
        choix = input("Votre choix : ").strip()
        
        match choix:
            case "1":
                try:
                    p = float(input("Entrez la probabilite de mutation (entre 0 et 1) : "))
                    sequence_mutee = simuler_mutations_remplacements(sequence, p)
                    print(f"\nSequence originale : {sequence}")
                    print(f"Sequence mutee     : {sequence_mutee}")
                    distance = estimation_distance_mutation(sequence, sequence_mutee)
                    print(f"Nombre de mutations effectuees : {distance}")
                except ValueError as e:
                    print(f"Erreur : {e}")
                except Exception as e:
                    print(f"Une erreur inattendue s'est produite : {e}")
            
            case "2":
                try:
                    p = float(input("Entrez la probabilite d'insertion (entre 0 et 1) : "))
                    sequence_mutee = mutation_par_insertion(sequence, p)
                    print(f"\nSequence originale ({len(sequence)} bases) : {sequence}")
                    print(f"Sequence mutee     ({len(sequence_mutee)} bases) : {sequence_mutee}")
                    print(f"Difference de longueur : +{len(sequence_mutee) - len(sequence)} bases")
                except ValueError as e:
                    print(f"Erreur : {e}")
                except Exception as e:
                    print(f"Une erreur s'est produite : {e}")
            
            case "3":
                try:
                    p = float(input("Entrez la probabilite de deletion (entre 0 et 1) : "))
                    sequence_mutee = mutation_par_deletion(sequence, p)
                    print(f"\nSequence originale ({len(sequence)} bases) : {sequence}")
                    print(f"Sequence mutee     ({len(sequence_mutee)} bases) : {sequence_mutee}")
                    print(f"Difference de longueur : {len(sequence_mutee) - len(sequence)} bases")
                except ValueError as e:
                    print(f"Erreur : {e}")
                except Exception as e:
                    print(f"Une erreur s'est produite : {e}")
            
            case "0":
                print("Retour au menu principal...")
                break
            
            case _:
                print("Choix invalide. Veuillez entrer un numero entre 0 et 3.")


def calculer_distance_sequences():
    """Calcule la distance de Levenshtein entre deux sequences."""
    try:
        print("\n--- Calcul de la distance de Levenshtein ---")
        seq1 = input("Entrez la premiere sequence : ").strip().upper()
        seq2 = input("Entrez la deuxieme sequence : ").strip().upper()
        
        if not seq1 or not seq2:
            print("Erreur : Les deux sequences doivent etre non vides.")
            return
        
        if not all(base in bases for base in seq1):
            print("Erreur : La sequence contient des bases invalides. Utilisez uniquement A, T, G, C.")
            return
        
        if not all(base in bases for base in seq2):
            print("Erreur : La sequence contient des bases invalides. Utilisez uniquement A, T, G, C.")
            return
        
        distance = distance_de_levenshtein(seq1, seq2)
        print(f"\nSequence 1 ({len(seq1)} bases) : {seq1}")
        print(f"Sequence 2 ({len(seq2)} bases) : {seq2}")
        print(f"Distance de Levenshtein calculee : {distance}")
    except Exception as e:
        print(f"Une erreur s'est produite lors du calcul de la distance : {e}")


def tester_calculer_distance():
    """Teste la fonction calculer_distance avec un arbre phylogenetique."""
    print("\nCOMING SOON")
    print("\nNote : On ne peut pas tester calculer_distance() avec une espece hypothetique...")
    print("Cela sera disponible plus tard.")
    print("Pour visualiser le fonctionnement, consultez la fonction reconstruction_arbre_phylogenetique().")


def sauvegarder_sequence_1():
    """Sauvegarde une sequence dans un fichier."""
    try:
        sequence = input("\nEntrez la sequence a sauvegarder (ou 'G' pour en generer une) : ").strip().upper()
        if sequence == 'G':
            sequence = generer_sequence()
            if sequence is None:
                return
        
        if not all(base in bases for base in sequence):
            print("Erreur : La sequence contient des bases invalides. Utilisez uniquement A, T, G, C.")
            return
        nom_fichier = input("Quel nom souhaitez-vous donner au fichier (sans extension) : ").strip()
        if not nom_fichier:
            print("Erreur : Le nom du fichier ne peut pas etre vide.")
            return
       
        os.makedirs("./data", exist_ok=True)
        sauvegarder_sequence(sequence, nom_fichier)
    except Exception as e:
        print(f"Erreur : Une erreur s'est produite lors de la sauvegarde de la sequence : {e}")


def reconstruire_arbre_phylogenetique():
    try:
        print("\n--- Reconstruction d'arbre phylogenetique ---")
        chemin_dossier = input("Entrez le chemin vers le dossier contenant les fichiers adn : ").strip()
        
        if not os.path.isdir(chemin_dossier):
            print(f"Erreur : Le dossier '{chemin_dossier}' n'existe pas.")
            return
        
        fichiers_adn = []
        for fichier in os.listdir(chemin_dossier):
            if fichier.endswith(".adn"):
                chemin_complet = os.path.join(chemin_dossier, fichier)
                fichiers_adn.append(chemin_complet)
        if not fichiers_adn:
            print(f"Erreur : Aucun fichier .adn trouve dans le dossier '{chemin_dossier}'. Je vous suggere d'en creer d'abord.")
            return
        
        print(f"\nFichiers ADN trouves : {len(fichiers_adn)}")
        for fichier in fichiers_adn:
            print(f"   - {fichier}")
        
        print("\nReconstruction de l'arbre phylogenetique en cours...")
        racine = reconstruction_arbre_phylogenetique(fichiers_adn)
        
        if racine is None:
            print("Erreur : Impossible de reconstruire l'arbre phylogenetique.")
            return

        print("\nArbre phylogenetique reconstruit avec succes !")
        print(f"Racine de l'arbre : {racine.nom}") 
        print(f"Statut : {'hypothetique' if racine.est_hypothetique else 'averee'}") 
        print(f"Nombre d'especes filles : {len(racine.get_especes_filles())}")
    except Exception as e:
        print(f"Erreur : Une erreur s'est produite lors de la reconstruction : {e}")


def main():
    """Fonction principale de l'application."""
    print("\nBienvenue dans l'application DinoTrack.")
    print("Cette application vous permet de tester les principales fonctions.")
    
    while True:
        afficher_menu()
        choix = input("Votre choix : ").strip()
        
        match choix:
            case "1":
                generer_sequence()
            
            case "2":
                menu_mutations()
            
            case "3":
                calculer_distance_sequences()
            
            case "4":
                tester_calculer_distance()
            
            case "5":
                reconstruire_arbre_phylogenetique()
            
            case "6":
                sauvegarder_sequence_1()
            
            case "0":
                print("\nMerci d'avoir utilise l'application. Bye")
                break
            
            case _:
                print("Erreur : Choix invalide. Veuillez entrer un numero entre 0 et 6.")


if __name__ == "__main__":
    main()
