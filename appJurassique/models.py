from .app import db
from datetime import datetime

class MATERIEL(db.Model):
    __tablename__ = 'MATERIEL'
    idMateriel = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500))
    plateforme = db.relationship('PLATEFORME', back_populates='materiel')
    habitations = db.relationship('HABITATION', back_populates='materiel')
    
    def __repr__(self):
        return f"<MATERIEL {self.nom}>"


class PLATEFORME(db.Model):
    __tablename__ = 'PLATEFORME'
    idPlateforme = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    min_nb_personne = db.Column(db.Integer)
    cout_journalier = db.Column(db.Float)
    intervalle_maintenance = db.Column(db.Integer)
    idMateriel = db.Column(db.Integer, db.ForeignKey('MATERIEL.idMateriel'))
    materiel = db.relationship('MATERIEL', back_populates='plateforme')
    #manque des trucs jsp
    
    def __repr__(self):
        return f"<PLATEFORME {self.nom}>"


class HABITATION(db.Model):
    __tablename__ = 'HABITATION'
    idHabitation = db.Column(db.Integer, primary_key=True)
    nom_habitation = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500))
    idMateriel = db.Column(db.Integer, db.ForeignKey('MATERIEL.idMateriel'))
    materiel = db.relationship('MATERIEL', back_populates='habitations')
    
    def __repr__(self):
        return f"<HABITATION {self.nom_habitation}>"


class BUDGET_MENSUEL(db.Model):
    __tablename__ = 'BUDGET_MENSUEL'
    annee = db.Column(db.Integer, primary_key=True)
    mois = db.Column(db.Integer, primary_key=True)
    budget = db.Column(db.Float, nullable=False)
    
    def __repr__(self):
        return f"<BUDGET_MENSUEL {self.annee}-{self.mois} {self.budget}>"


class LIEU_FOUILLE(db.Model):
    __tablename__ = 'LIEU_FOUILLE'
    idLieu = db.Column(db.Integer, primary_key=True)
    nomLieu = db.Column(db.String(100), nullable=False)
    campagnes = db.relationship('CAMPAGNE', back_populates='lieu')
    
    def __repr__(self):
        return f"<LIEU_FOUILLE {self.nomLieu}>"


class PERSONNE(db.Model):
    __tablename__ = 'PERSONNE'
    idPersonne = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    prenom = db.Column(db.String(100), nullable=False)
    login = db.relationship('LOGIN', back_populates='personne')
    #a rajouter des liaisons
    def __repr__(self):
        return f"<PERSONNE {self.prenom} {self.nom}>"


class LOGIN(db.Model):
    __tablename__ = 'LOGIN'
    username = db.Column(db.String(50), primary_key=True)
    password = db.Column(db.String(255), nullable=False)
    idPersonne = db.Column(db.Integer, db.ForeignKey('PERSONNE.idPersonne'), nullable=False)
    personne = db.relationship('PERSONNE', back_populates='login')
    
    def __repr__(self):
        return f"<LOGIN {self.username}>"


class CAMPAGNE(db.Model):
    __tablename__ = 'CAMPAGNE'
    idCampagne = db.Column(db.Integer, primary_key=True)
    dateDebut = db.Column(db.Date, nullable=False)
    duree = db.Column(db.Integer, nullable=False)
    idLieu = db.Column(db.Integer, db.ForeignKey('LIEU_FOUILLE.idLieu'))
    lieu = db.relationship('LIEU_FOUILLE', back_populates='campagnes')
    #pareil

    def __repr__(self):
        return f"<CAMPAGNE ({self.idCampagne}) {self.dateDebut}>"
