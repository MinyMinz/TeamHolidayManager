from db.database import SessionLocal

db = SessionLocal()

def dbGet(model:any, columnName: str, value: any):
    return db.query.filter(getattr(model, columnName) == value).first()

def dbGetAll(model:any):
    return db.query(model).all()