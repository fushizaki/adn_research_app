class Espece:

    def __init__(self, nom, sequence_adn, est_hypothetique, especes_filles):
        self.nom = nom
        self.sequence_adn = sequence_adn
        self.est_hypothetique = est_hypothetique
        self.especes_filles = especes_filles

    def est_averee(self):
        """Vérifie si l'espèce est avérée (non hypothétique).

        Returns:
            bool: True si l'espèce est avérée, False sinon.
        """
        return not self.est_hypothetique

    def add_espece_fille(self, espece_fille):
        """Ajoute une espèce fille à l'espèce actuelle si elle est hypothétique.

        Args:
            espece_fille (Espece): L'espèce fille à ajouter.
        """
        if self.est_hypothetique:
            self.especes_filles.append(espece_fille)

    def del_espece_fille(self, espece_fille):
        """Supprime une espèce fille de l'espèce actuelle.

        Args:
            espece_fille (Espece): L'espèce fille à supprimer.
        """
        self.especes_filles.remove(espece_fille)

    def __str__(self):
        return f"Espece(nom={self.nom}, sequence_adn={self.sequence_adn}, est_hypothetique={self.est_hypothetique}, especes_filles={[fille.nom for fille in self.especes_filles]})"
