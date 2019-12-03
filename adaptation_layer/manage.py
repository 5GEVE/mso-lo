from flask_script import Manager
from app import app, db
from models import NFVO, NFVO_CREDENTIALS
manager = Manager(app)


@manager.command
def seed():
    turin_osm = NFVO(id=1, name="turin_osm", nfvo_type="OSM", uri="https://osm-turin.5g-eve.eu", site="Italy")
    turin_os_cred = NFVO_CREDENTIALS(
        nfvo_id=1, host='localhost', user='admin',
        password='admin', project='admin')
    db.session.add(turin_osm)
    db.session.commit()
    db.session.add(turin_os_cred)
    db.session.commit()


if __name__ == "__main__":
    manager.run()
