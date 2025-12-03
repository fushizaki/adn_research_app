from appJurassique.models import HABILITATION


def test_syncdb(runner, testapp):
    with testapp.app_context():
        result = runner.invoke(args=['syncdb'])
        # Command executed successfully
        assert result.exit_code == 0


def test_syncdb_creates_default_habilitations(runner, testapp):
    with testapp.app_context():
        from appJurassique.app import db
        assert HABILITATION.query.count() == 0
        runner.invoke(args=['syncdb'])
        assert HABILITATION.query.count() == 4
        habs = [h.nom_habilitation for h in HABILITATION.query.all()]
        assert "Électrique" in habs
        assert "Chimique" in habs
        assert "Biologique" in habs
        assert "Radiations" in habs


def test_syncdb_no_duplicate_habilitations(runner, testapp):
    with testapp.app_context():
        from appJurassique.app import db
        runner.invoke(args=['syncdb'])
        runner.invoke(args=['syncdb'])
        assert HABILITATION.query.count() == 4


def test_dropdb(runner, testapp):
    with testapp.app_context():
        result = runner.invoke(args=['dropdb'])
        # Command executed successfully
        assert result.exit_code == 0
