from .app import db, login_manager
from datetime import datetime
from flask_login import UserMixin
import enum


class MATERIEL(db.Model):
    __tablename__ = 'MATERIEL'
    idMateriel = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500))
    plateforme = db.relationship('PLATEFORME', back_populates='materiel')
    habilitations = db.relationship('HABILITATION', back_populates='materiel')
    utilisations = db.relationship('UTILISER', back_populates='materiel', cascade='all, delete-orphan')
    necessites = db.relationship('NECESSITER', back_populates='materiel', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<MATERIEL {self.nom}>"


class PLATEFORME(db.Model):
    __tablename__ = 'PLATEFORME'
    idPlateforme = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    min_nb_personne = db.Column(db.Integer)
    cout_journalier = db.Column(db.Float)
    intervalle_maintenance = db.Column(db.Integer)
    materiel = db.relationship('UTILISER', back_populates='plateforme')
    planifier = db.relationship('PLANIFIER', back_populates='plateforme', cascade='all, delete-orphan')
    maintenance = db.relationship('MAINTENANCE', back_populates='plateforme', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<PLATEFORME {self.nom}>"


class HABILITATION(db.Model):
    __tablename__ = 'HABILITATION'
    idHabilitation = db.Column(db.Integer, primary_key=True)
    nom_habilitation = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500))
    idMateriel = db.Column(db.Integer, db.ForeignKey('MATERIEL.idMateriel'))
    materiel = db.relationship('MATERIEL', back_populates='habilitations')
    habiliter = db.relationship('HABILITER', back_populates='habilitation', cascade='all, delete-orphan')
    necessites = db.relationship('NECESSITER', back_populates='habilitation', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<HABILITATION {self.nom_habilitation}>"


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
    sejourner = db.relationship('SEJOURNER', back_populates='lieu', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<LIEU_FOUILLE {self.nomLieu}>"

class role_labo_enum(enum.Enum):
    DIRECTION = "DIRECTION"
    TECHNICIEN = "TECHNICIEN"
    ADMINISTRATION = "ADMINISTRATION"
    CHERCHEUR = "CHERCHEUR"
    
    def get_roles():
        return [role.value for role in role_labo_enum]

class PERSONNE(UserMixin, db.Model):
    __tablename__ = 'PERSONNE'
    username = db.Column(db.String(50), primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    prenom = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role_labo = db.Column(db.Enum(role_labo_enum), nullable=False)
    participer = db.relationship('PARTICIPER', back_populates='personne', cascade='all, delete-orphan')
    habiliter = db.relationship('HABILITER', back_populates='personne', cascade='all, delete-orphan')

    def get_id(self):
        return self.username
    
    @login_manager.user_loader
    def load_user(username):
        return PERSONNE.query.get(username)
    
    def __repr__(self):
        return f"<PERSONNE {self.prenom} {self.nom}>"


class CAMPAGNE(db.Model):
    __tablename__ = 'CAMPAGNE'
    idCampagne = db.Column(db.Integer, primary_key=True)
    dateDebut = db.Column(db.Date, nullable=False)
    duree = db.Column(db.Integer, nullable=False)
    idLieu = db.Column(db.Integer, db.ForeignKey('LIEU_FOUILLE.idLieu'))
    lieu = db.relationship('LIEU_FOUILLE', back_populates='campagnes')
    participer = db.relationship('PARTICIPER', back_populates='campagne', cascade='all, delete-orphan')
    planifier = db.relationship('PLANIFIER', back_populates='campagne', cascade='all, delete-orphan')
    sejourner = db.relationship('SEJOURNER', back_populates='campagne', cascade='all, delete-orphan')
    rapporter = db.relationship('RAPPORTER', back_populates='campagne', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<CAMPAGNE ({self.idCampagne}) {self.dateDebut}>"


class PARTICIPER(db.Model):
    __tablename__ = 'PARTICIPER'
    username = db.Column(db.String(50),
                         db.ForeignKey('PERSONNE.username'),
                         primary_key=True)
    idCampagne = db.Column(db.Integer,
                           db.ForeignKey('CAMPAGNE.idCampagne'),
                           primary_key=True)
    personne = db.relationship('PERSONNE', back_populates='participer')
    campagne = db.relationship('CAMPAGNE', back_populates='participer')

    def __repr__(self):
        return f"<PARTICIPER {self.username} in {self.idCampagne}>"


class PLANIFIER(db.Model):
    __tablename__ = 'PLANIFIER'
    idPlateforme = db.Column(db.Integer,
                             db.ForeignKey('PLATEFORME.idPlateforme'),
                             primary_key=True)
    idCampagne = db.Column(db.Integer,
                           db.ForeignKey('CAMPAGNE.idCampagne'),
                           primary_key=True)
    plateforme = db.relationship('PLATEFORME', back_populates='planifier')
    campagne = db.relationship('CAMPAGNE', back_populates='planifier')

    def __repr__(self):
        return f"<PLANIFIER Plateforme {self.idPlateforme} for Campagne {self.idCampagne}>"


class SEJOURNER(db.Model):
    __tablename__ = 'SEJOURNER'
    idCampagne = db.Column(db.Integer,
                           db.ForeignKey('CAMPAGNE.idCampagne'),
                           primary_key=True)
    idLieu = db.Column(db.Integer,
                       db.ForeignKey('LIEU_FOUILLE.idLieu'),
                       primary_key=True)
    campagne = db.relationship('CAMPAGNE', back_populates='sejourner')
    lieu = db.relationship('LIEU_FOUILLE', back_populates='sejourner')

    def __repr__(self):
        return f"<SEJOURNER Campagne {self.idCampagne} at Lieu {self.idLieu}>"


class ECHANTILLON(db.Model):
    __tablename__ = 'ECHANTILLON'
    idEchantillon = db.Column(db.Integer, primary_key=True)
    fichierAdn = db.Column(db.String(100))
    commentairesEchantillion = db.Column(db.String(500))
    appartenir = db.relationship('APPARTENIR', back_populates='echantillon', cascade='all, delete-orphan')
    rapporter = db.relationship('RAPPORTER', back_populates='echantillon', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<ECHANTILLON {self.idEchantillon}>"


class ESPECE(db.Model):
    __tablename__ = 'ESPECE'
    idEspece = db.Column(db.Integer, primary_key=True)
    nomEspece = db.Column(db.String(100), nullable=False)
    caracteristiques = db.Column(db.String(500))
    appartenir = db.relationship('APPARTENIR', back_populates='espece', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<ESPECE {self.nomEspece}>"


class APPARTENIR(db.Model):
    __tablename__ = 'APPARTENIR'
    idEchantillon = db.Column(db.Integer,
                              db.ForeignKey('ECHANTILLON.idEchantillon'),
                              primary_key=True)
    idEspece = db.Column(db.Integer,
                         db.ForeignKey('ESPECE.idEspece'),
                         primary_key=True)
    echantillon = db.relationship('ECHANTILLON', back_populates='appartenir')
    espece = db.relationship('ESPECE', back_populates='appartenir')

    def __repr__(self):
        return f"<APPARTENIR Echantillon {self.idEchantillon} to Espece {self.idEspece}>"


class HABILITER(db.Model):
    __tablename__ = 'HABILITER'
    username = db.Column(db.String(50),
                         db.ForeignKey('PERSONNE.username'),
                         primary_key=True)
    idHabilitation = db.Column(db.Integer,
                               db.ForeignKey('HABILITATION.idHabilitation'),
                               primary_key=True)
    personne = db.relationship('PERSONNE', back_populates='habiliter')
    habilitation = db.relationship('HABILITATION', back_populates='habiliter')

    def __repr__(self):
        return f"<HABILITER {self.username} to Habilitation {self.idHabilitation}>"


class RAPPORTER(db.Model):
    __tablename__ = 'RAPPORTER'
    idEchantillon = db.Column(db.Integer,
                              db.ForeignKey('ECHANTILLON.idEchantillon'),
                              primary_key=True)
    idCampagne = db.Column(db.Integer,
                           db.ForeignKey('CAMPAGNE.idCampagne'),
                           primary_key=True)
    echantillon = db.relationship('ECHANTILLON', back_populates='rapporter')
    campagne = db.relationship('CAMPAGNE', back_populates='rapporter')

    def __repr__(self):
        return f"<RAPPORTER Echantillon {self.idEchantillon} from Campagne {self.idCampagne}>"


class UTILISER(db.Model):
    __tablename__ = 'UTILISER'
    idMateriel = db.Column(db.Integer,
                           db.ForeignKey('MATERIEL.idMateriel'),
                           primary_key=True)
    idPlateforme = db.Column(db.Integer,
                             db.ForeignKey('PLATEFORME.idPlateforme'),
                             primary_key=True)
    quantite = db.Column(db.Integer)
    materiel = db.relationship('MATERIEL', back_populates='utilisations')
    plateforme = db.relationship('PLATEFORME', back_populates='utilisations')

    def __repr__(self):
        return f"<UTILISER Materiel {self.idMateriel} sur Plateforme {self.idPlateforme}>"


class NECESSITER(db.Model):
    __tablename__ = 'NECESSITER'
    idHabilitation = db.Column(db.Integer,
                               db.ForeignKey('HABILITATION.idHabilitation'),
                               primary_key=True)
    idMateriel = db.Column(db.Integer,
                           db.ForeignKey('MATERIEL.idMateriel'),
                           primary_key=True)
    materiel = db.relationship('MATERIEL', back_populates='necessites')
    habilitation = db.relationship('HABILITATION', back_populates='necessites')

    def __repr__(self):
        return f"<NECESSITER Habilitation {self.idHabilitation} for Materiel {self.idMateriel}>"


class statut(enum.Enum):
    PLANIFIEE = "PLANIFIEE"
    EN_COURS = "EN_COURS"
    TERMINEE = "TERMINEE"


class MAINTENANCE(db.Model):
    __tablename__ = 'MAINTENANCE'
    idMaintenance = db.Column(db.Integer, primary_key=True)
    dateMaintenance = db.Column(db.Date, nullable=False)
    duree_maintenance = db.Column(db.Integer, nullable=False)
    statut = db.Column(db.Enum(statut), nullable=False)
    idPlateforme = db.Column(db.Integer,
                             db.ForeignKey('PLATEFORME.idPlateforme'))
    plateforme = db.relationship('PLATEFORME', back_populates='maintenance')

    def __repr__(self):
        return f"<MAINTENANCE {self.idMaintenance} on {self.dateMaintenance}>"

class HISTORIQUE(db.Model):
    __tablename__ = 'HISTORIQUE'
    idHistorique = db.Column(db.Integer, primary_key=True)
    nom_fichier_base = db.Column(db.String(255))
    proba = db.Column(db.Float)
    nb_remplacement = db.Column(db.Integer)
    nb_insertion = db.Column(db.Integer)
    nb_deletion = db.Column(db.Integer)
    note = db.Column(db.String(255))
    date_enregistrement = db.Column(db.DateTime)

    def __repr__(self):
        return f"<HISTORIQUE {self.idHistorique} {self.nom_fichier_base}>"
