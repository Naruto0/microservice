import os
import pytest
import tempfile

from micro import app
from micro.database import db
from micro.models import Product


@pytest.fixture
def database_fixture():
    db_fd, app.config['DATABASE'] = tempfile.mkstemp()
    app.config['TESTING'] = True

    with app.test_client() as client:
        with app.app_context():
            app.init_db()
        yield client

    os.close(db_fd)
    os.unlink(app.config['DATABASE'])


def test_model_fit(database_fixture):
    p = Product(name="Qoza 3000- křovinořez", description="Super sekajda na trávu")
    db.session.add(p)
    db.session.commit()


def test_database(database_fixture):
    q = Product.query.all()
    assert len(q) == 1