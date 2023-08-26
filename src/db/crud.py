from db.database import SessionLocal

db = SessionLocal()

# Read Operations
def dbGet(model:any, columnName: str, value: any):
    dbModel = db.query(model).filter(getattr(model, columnName) == value).first()
    return dbModel

def dbGetAll(model:any):
    dbModel = db.query(model).all()
    return dbModel

# Create Operation
def dbCreate(model:any, data: dict):
    dbModel = model(**data)
    db.add(dbModel)
    db.commit()
    return dbModel

# Update Operation
def dbUpdate(model:any, data: dict):
    dbModel = db.query(model).filter(model.id == data['id']).first()
    dbModel = model(**data)
    db.commit()
    return dbModel

# Delete Operation
def dbDelete(model:any, id: int):
    dbModel = db.query(model).filter(model.id == id).first()
    db.delete(dbModel)
    db.commit()
    