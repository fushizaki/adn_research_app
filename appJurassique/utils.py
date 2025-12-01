from appJurassique.models import MATERIEL, UTILISER
from .app import app, db

def update_qte(qte, idMat, idPlat):
    
    materiel_deja_utilise = db.session.query(UTILISER).filter(UTILISER.idMateriel == idMat, UTILISER.idPlateforme == idPlat).first()
    
    print(materiel_deja_utilise)
    
    if materiel_deja_utilise != None:
        new_qte = materiel_deja_utilise.quantite + qte
        if new_qte >= 0:
            db.session.query(UTILISER).filter(UTILISER.idMateriel == idMat, UTILISER.idPlateforme == idPlat).update({UTILISER.quantite: UTILISER.quantite + qte})
            db.session.commit()
            return True
    else:
            utilise = UTILISER(idMateriel= idMat, idPlateforme=idPlat, quantite= qte)
            db.session.add(utilise)
            db.session.commit()
            return True
    return False