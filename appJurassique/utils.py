from appJurassique.models import MATERIEL, UTILISER
from .app import app, db

def update_qte(qte, idMat, idPlat, retirer):
    
    materiel = MATERIEL.query.get(idMat)
    materiel_deja_utilise = db.session.query(UTILISER).filter(UTILISER.idMateriel == idMat, UTILISER.idPlateforme == idPlat).all()
    
    print(materiel_deja_utilise)
    
    if materiel:
        if retirer:
            new_qte = materiel.quantite - qte
            if materiel_deja_utilise != []:
                if new_qte >= 0:
                    db.session.query(MATERIEL).filter(MATERIEL.idMateriel == idMat).update({MATERIEL.quantite: new_qte})
                    db.session.query(UTILISER).filter(UTILISER.idMateriel == idMat, UTILISER.idPlateforme == idPlat).update({UTILISER.quantite: UTILISER.quantite + qte})
                    db.session.commit()
                    return True
            else:
                if new_qte >= 0:
                    db.session.query(MATERIEL).filter(MATERIEL.idMateriel == idMat).update({MATERIEL.quantite: new_qte})
                    utilise = UTILISER(idMateriel= idMat, idPlateforme=idPlat, quantite= qte)
                    db.session.add(utilise)
                    db.session.commit()
                    return True 
        else:
            new_qte = materiel.quantite + qte
            if materiel_deja_utilise is not None:
                if new_qte >= 0:
                    db.session.query(MATERIEL).filter(MATERIEL.idMateriel == idMat).update({MATERIEL.quantite: new_qte})
                    db.session.query(UTILISER).filter(UTILISER.idMateriel == idMat, UTILISER.idPlateforme == idPlat).update({UTILISER.quantite: new_qte})
                    db.session.commit()
                    return True
            else:
                if new_qte >= 0:
                    db.session.query(MATERIEL).filter(MATERIEL.idMateriel == idMat).update({MATERIEL.quantite: new_qte})
                    utilise = UTILISER(idMateriel= idMat, idPlateforme=idPlat, quantite= qte)
                    db.session.add(utilise)
                    db.session.commit()
                    return True 
    return False