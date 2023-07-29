from sqlalchemy.orm import Session
from . import models, schemas


def dbGet(model:any, columnName: str, value: any):
    return model.query.filter(getattr(model, columnName) == value).first()

def dbGetAll(model:any):
    return model.query.all()

def dbCreate(model:any, data: dict):
    model = model(**data)
    return model.save()