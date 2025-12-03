import logging as lg
from .app import app, db
from .models import HABILITATION


@app.cli.command()
def syncdb():
    '''Creates all missing tables.'''
    db.create_all()
    if HABILITATION.query.count() == 0:
        defaults = [
            ("electrique", "Électrique"),
            ("chimique", "Chimique"),
            ("biologique", "Biologique"),
            ("radiations", "Radiations"),
        ]
        for key, label in defaults:
            db.session.add(HABILITATION(nom_habilitation=label, description=key))
        db.session.commit()
    lg.warning('Database synchronized!')

@app.cli.command()
def dropdb():
    '''Drops all tables.'''
    db.drop_all()
    lg.warning('Database dropped!')
