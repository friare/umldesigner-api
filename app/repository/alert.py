from sqlalchemy.orm import Session
from fastapi import status, HTTPException, status
from ..datastruct import models
from ..schemas import schemas
from ..security.hashing import Hash
from datetime import datetime, time, timedelta


def get_alert(db, tokendata):
    alert = db.query(models.Alert).filter(models.Alert.project_owner_id == tokendata.id).all()
    return alert

def new_alert(version, diagram, main_diagram, db, tokendata) -> bool:
    try:
        alert = models.Alert(
            version_id=version.id,
            project_owner_id=main_diagram.author_id,
            id_project=main_diagram.project_id,
            date_update=datetime.now(),
            label=version.label
        )
        db.add(alert)
        db.commit()
        db.refresh(alert)
        return True
    except:
        return False

def update_alert(version, db) -> bool:
    try:
        alert = db.query(models.Alert).filter(models.Alert.version_id == version.first().id)
        if not alert.first():
            raise HTTPException(status_code=403, detail='Not allowed.')
        alert.update({
            'already_read': False,
            'type': "Nouvelle mise à jour",
            'date_update': datetime.now(),
        })
        db.commit()
        return True
    except Exception as e:
        print(e)
        return False

def read_alert(request, db, tokendata):
    alert = db.query(models.Alert).filter(models.Alert.id == request.alert_id).filter(models.Alert.project_owner_id == tokendata.id)
    if not alert.first():
        raise HTTPException(status_code=404, detail='Not found.')
    alert.update({
        'already_read': True
    })
    db.commit()
    return alert.first()