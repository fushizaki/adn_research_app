from datetime import timedelta
from .app import db
from .models import CAMPAGNE, PLANIFIER

def verifier_chevauchement_campagne(id_plateforme, date_debut, duree_jours):
    """
    Vérifie si une maintenance chevauche une campagne existante sur la même plateforme.
    Retourne un message d'erreur si chevauchement, None sinon.
    """
    date_fin_maintenance = date_debut + timedelta(days=duree_jours - 1)
    
    campagnes_plateforme = db.session.query(CAMPAGNE).join(
        PLANIFIER, CAMPAGNE.idCampagne == PLANIFIER.idCampagne).filter(
        PLANIFIER.idPlateforme == id_plateforme).all()
    
    for campagne in campagnes_plateforme:
        date_fin_campagne = campagne.dateDebut + timedelta(days=campagne.duree - 1)
        if date_debut <= date_fin_campagne and date_fin_maintenance >= campagne.dateDebut:
            return f"Conflit avec une campagne existante (du {campagne.dateDebut} au {date_fin_campagne}) pour cette plateforme."
    
    return None
