from flask_wtf import FlaskForm
from wtforms import DateField, IntegerField, SelectField, SelectMultipleField, StringField
from wtforms.validators import DataRequired, NumberRange, Optional


class CampagneForm(FlaskForm):
    """Formulaire WTForms pour la création d'une campagne."""

    titre = StringField("Titre", validators=[Optional()])
    dateDebut = DateField(
        "Date de début",
        format="%Y-%m-%d",
        validators=[DataRequired(message="La date de début est obligatoire.")],
    )
    duree = IntegerField(
        "Durée en heures",
        validators=[
            DataRequired(message="La durée est obligatoire."),
            NumberRange(min=1, message="La durée doit être d'au moins 1 heure."),
        ],
    )
    idLieu = SelectField(
        "Lieu de fouille",
        choices=[],
        coerce=str,
        validators=[DataRequired(message="Le lieu de fouille est obligatoire.")],
    )
    idPlateforme = SelectField(
        "Plateforme",
        choices=[],
        coerce=str,
        validators=[DataRequired(message="La plateforme est obligatoire.")],
    )
    membres = SelectMultipleField(
        "Membres",
        choices=[],
        coerce=str,
    )

    class Meta:
        csrf = False
