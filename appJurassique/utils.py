from datetime import timedelta
from .app import db
from .models import *

def calculer_date_fin(date_debut, duree_jours):

    if not date_debut:
        return None
    jours = max(1, int(duree_jours))
    return date_debut + timedelta(days=jours - 1)


def periodes_se_chevauchent(debut_a, fin_a, debut_b, fin_b):

    return not (fin_a < debut_b or fin_b < debut_a)


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
        date_fin = calculer_date_fin(date_debut, duree_jours)

        # ok, erreur = verifier_disponibilite_plateforme(id_plateforme, date_debut, date_fin)
        # if not ok:
        #     return None, erreur

        # ok, erreur = verifier_disponibilite_membres(membres, date_debut, date_fin)
        # if not ok:
        #     return None, erreur

        # ok, erreur = verifier_habilitations_membres(id_plateforme, membres)
        # if not ok:
        #     return None, erreur

        # ok, erreur = verifier_maintenance_plateforme(plateforme, date_debut, date_fin)
        # if not ok:
        #     return None, erreur

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

def obtenir_membres_compatibles(id_plateforme, date_debut=None, date_fin=None):
    """
    Filtre les membres habilités ET disponibles pour les dates données.
    Args:
        id_plateforme: ID 
        date_debut: Date de début 
        date_fin: Date de fin 
    Returns:
        list: liste de tuples (PERSONNE, bool)
    """
    
    try:
        plateforme = PLATEFORME.query.get(id_plateforme)
        if not plateforme:
            return []
        
        tous_membres = PERSONNE.query.all()
        utilisations = UTILISER.query.filter_by(idPlateforme=id_plateforme).all()
        
        if not utilisations:
            materiels_ids = []
        else:
            materiels_ids = [u.idMateriel for u in utilisations]
        
        if materiels_ids:
            habilitations_requises = db.session.query(HABILITATION).join(
                NECESSITER, HABILITATION.idHabilitation == NECESSITER.idHabilitation
            ).filter(NECESSITER.idMateriel.in_(materiels_ids)).all()
        else:
            habilitations_requises = []
        
        habilitations_requises_ids = set([h.idHabilitation for h in habilitations_requises])
        
        membres_compatibles = []
        for membre in tous_membres:
            if hasattr(membre, 'habiliter') and membre.habiliter:
                habilitations_membre_ids = set([h.idHabilitation for h in membre.habiliter])
            else:
                habilitations_membre_ids = set()
            
            habilite = habilitations_requises_ids.issubset(habilitations_membre_ids)
            
            disponible = True
            if date_debut and date_fin:
                campagnes = (CAMPAGNE.query
                            .join(PARTICIPER, PARTICIPER.idCampagne == CAMPAGNE.idCampagne)
                            .filter(PARTICIPER.username == membre.username)
                            .all())
                for campagne in campagnes:
                    fin_existante = calculer_date_fin(campagne.dateDebut, campagne.duree)
                    if periodes_se_chevauchent(date_debut, date_fin, campagne.dateDebut, fin_existante):
                        disponible = False
                        break
            
            compatible = habilite and disponible
            membres_compatibles.append((membre, compatible))
        
        return membres_compatibles
    
    except Exception as e:
        print(f"erreur dans la fonction obtenir_membres_compatibles: {str(e)}")
        import traceback
        traceback.print_exc()
        return []
    


#====== fonctions qui verifient. elles sont commentées car pas assez d'insert  ======

def verifier_disponibilite_plateforme(id_plateforme, date_debut, date_fin):
    """Vérifie que la plateforme n'est pas déjà utilisée sur la période."""
    # campagnes = (CAMPAGNE.query
    #              .join(PLANIFIER, PLANIFIER.idCampagne == CAMPAGNE.idCampagne)
    #              .filter(PLANIFIER.idPlateforme == id_plateforme)
    #              .all())
    # for campagne in campagnes:
    #     fin_existante = calculer_date_fin(campagne.dateDebut, campagne.duree)
    #     if periodes_se_chevauchent(date_debut, date_fin, campagne.dateDebut, fin_existante):
    #         return False, (
    #             f"La plateforme est déjà mobilisée du {campagne.dateDebut.strftime('%d/%m/%Y')} "
    #             f"au {fin_existante.strftime('%d/%m/%Y')}.")
    return True, None


def verifier_disponibilite_membres(membres, date_debut, date_fin):
    """S'assure qu'aucun membre n'est engagé sur une autre campagne."""
    # for membre in membres:
    #     campagnes = (CAMPAGNE.query
    #                  .join(PARTICIPER, PARTICIPER.idCampagne == CAMPAGNE.idCampagne)
    #                  .filter(PARTICIPER.username == membre.username)
    #                  .all())
    #     for campagne in campagnes:
    #         fin_existante = calculer_date_fin(campagne.dateDebut, campagne.duree)
    #         if periodes_se_chevauchent(date_debut, date_fin, campagne.dateDebut, fin_existante):
    #             return False, (
    #                 f"{membre.prenom} {membre.nom} participe déjà à une campagne du "
    #                 f"{campagne.dateDebut.strftime('%d/%m/%Y')} au {fin_existante.strftime('%d/%m/%Y')}.")
    return True, None


def verifier_habilitations_membres(id_plateforme, membres):
    """Confirme que tous les membres sélectionnés sont habilités pour la plateforme."""
    # compatibles = obtenir_membres_compatibles(id_plateforme)
    # habilites = {m.username for m, ok in compatibles if ok}
    # non_habilites = [m for m in membres if m.username not in habilites]
    # if non_habilites:
    #     noms = ", ".join(f"{m.prenom} {m.nom}" for m in non_habilites)
    #     return False, f"Les membres suivants n'ont pas les habilitations requises : {noms}."
    return True, None


def verifier_maintenance_plateforme(plateforme, date_debut, date_fin):
    """Vérifie que l'intervalle de maintenance n'arrive pas à expiration."""
    # intervalle = plateforme.intervalle_maintenance
    # if not intervalle:
    #     return True, None
    #
    # derniere_maintenance = (MAINTENANCE.query
    #                         .filter(MAINTENANCE.idPlateforme == plateforme.idPlateforme)
    #                         .filter(MAINTENANCE.dateMaintenance <= date_debut)
    #                         .order_by(MAINTENANCE.dateMaintenance.desc())
    #                         .first())
    # if not derniere_maintenance:
    #     return False, (
    #         f"Aucune maintenance n'a été effectuée pour cette plateforme. "
    #         f"Une maintenance est obligatoire avant d'utiliser la plateforme.")
    #
    # limite = derniere_maintenance.dateMaintenance + timedelta(days=intervalle)
    # if date_fin >= limite:
    #     return False, (
    #         f"La durée de la campagne dépasse l'intervalle de maintenance. "
    #         f"Dernière maintenance effectuée le {derniere_maintenance.dateMaintenance.strftime('%d/%m/%Y')}. "
    #         f"Prochaine maintenance requise le {limite.strftime('%d/%m/%Y')}.")
    return True, None



#==== getters


def obtenir_plateformes_disponibles(date_debut, duree_jours):
    """
    Retourne la liste des plateformes disponibles pour une date et durée donnée.
    Args:
        date_debut: Date de début de la campagne
        duree_jours: Durée en jours
    Returns:
        list: IDs des plateformes disponibles
    """
    if not date_debut or not duree_jours:
        return []

    try:
        date_fin = calculer_date_fin(date_debut, duree_jours)
        toutes_plateformes = PLATEFORME.query.all()
        plateformes_disponibles = []
        
        for plateforme in toutes_plateformes:
            ok, _ = verifier_disponibilite_plateforme(plateforme.idPlateforme, date_debut, date_fin)
            if not ok:
                continue
            ok, _ = verifier_maintenance_plateforme(plateforme, date_debut, date_fin)
            if not ok:
                continue
            plateformes_disponibles.append(plateforme.idPlateforme)
        return plateformes_disponibles
    
    except Exception as e:
        print(f"Erreur dans obtenir_plateformes_disponibles: {str(e)}")
        return []


def recuperer_budget_mensuel(date_objet):

    if not date_objet:
        return None
    return BUDGET_MENSUEL.query.filter_by(
        annee=date_objet.year,
        mois=date_objet.month
    ).first()


def estimer_cout_campagne(plateforme, duree_jours):

    if not plateforme or not plateforme.cout_journalier:
        return None
    jours = max(1, int(duree_jours))
    return round(plateforme.cout_journalier * jours, 2)
