from datetime import timedelta
from .app import db
from .models import (
    CAMPAGNE, PLATEFORME, PERSONNE, PARTICIPER,
    PLANIFIER, SEJOURNER, NECESSITER, HABILITATION, UTILISER, MATERIEL
)


def verifier_nombre_membres(plateforme, membres):
    """Vérifie que le nombre de membres est suffisant pour la plateforme."""
    if plateforme.min_nb_personne and len(membres) < plateforme.min_nb_personne:
        return False, (
            f"La plateforme '{plateforme.nom}' nécessite au minimum "
            f"{plateforme.min_nb_personne} personnes, mais seulement {len(membres)} "
            f"ont été sélectionnées."
        )
    return True, None


def creer_campagne(date_debut, duree_jours, id_lieu, id_plateforme, noms_utilisateurs_membres, titre=None):
    """
    Crée une nouvelle campagne avec toutes les validations nécessaires.
    Les triggers SQL géreront les validations de disponibilité et d'habilitations.
    
    Note: le paramètre titre est accepté pour compatibilité mais n'est pas stocké en base.
    """
    try:
        plateforme = PLATEFORME.query.get(id_plateforme)
        if not plateforme:
            return None, f"Plateforme avec l'ID {id_plateforme} introuvable."

        membres = PERSONNE.query.filter(PERSONNE.username.in_(noms_utilisateurs_membres)).all()
        if len(membres) != len(noms_utilisateurs_membres):
            return None, "Un ou plusieurs membres n'ont pas été trouvés."

        ok, erreur = verifier_nombre_membres(plateforme, membres)
        if not ok:
            return None, erreur

        nouvelle_campagne = CAMPAGNE(
            dateDebut=date_debut,
            duree=duree_jours
        )
        db.session.add(nouvelle_campagne)
        db.session.flush()

        for membre in membres:
            participation = PARTICIPER(
                username=membre.username,
                idCampagne=nouvelle_campagne.idCampagne
            )
            db.session.add(participation)

        planification = PLANIFIER(
            idPlateforme=id_plateforme,
            idCampagne=nouvelle_campagne.idCampagne
        )
        db.session.add(planification)

        sejour = SEJOURNER(
            idCampagne=nouvelle_campagne.idCampagne,
            idLieu=id_lieu
        )
        db.session.add(sejour)

        db.session.commit()

        return nouvelle_campagne, None

    except Exception as e:
        db.session.rollback()
        raise e

def obtenir_membres_compatibles(id_plateforme):
    """
    Retourne la liste des membres compatibles avec une plateforme donnée.
    Utilisé pour l'affichage dans l'interface utilisateur.
    
    Args:
        id_plateforme: ID de la plateforme
    
    Returns:
        list: liste de tuples (PERSONNE, bool) où bool indique si compatible
    """
    
    try:
        plateforme = PLATEFORME.query.get(id_plateforme)
        if not plateforme:
            return []
        
        tous_membres = PERSONNE.query.all()
        
        utilisations = UTILISER.query.filter_by(idPlateforme=id_plateforme).all()
        
        if not utilisations:
            return [(membre, True) for membre in tous_membres]
        
        materiels_ids = [u.idMateriel for u in utilisations]
        habilitations_requises = db.session.query(HABILITATION).join(
            NECESSITER, HABILITATION.idHabilitation == NECESSITER.idHabilitation
        ).filter(NECESSITER.idMateriel.in_(materiels_ids)).all()
        
        if not habilitations_requises:
            return [(membre, True) for membre in tous_membres]
        
        habilitations_requises_ids = set([h.idHabilitation for h in habilitations_requises])
        
        membres_compatibles = []
        for membre in tous_membres:
            if hasattr(membre, 'habiliter') and membre.habiliter:
                habilitations_membre_ids = set([h.idHabilitation for h in membre.habiliter])
            else:
                habilitations_membre_ids = set()
            
            compatible = habilitations_requises_ids.issubset(habilitations_membre_ids)
            membres_compatibles.append((membre, compatible))
        
        return membres_compatibles
    
    except Exception as e:
        print(f"Error in obtenir_membres_compatibles: {str(e)}")
        import traceback
        traceback.print_exc()
        return []
