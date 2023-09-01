from db.database import SessionLocal

db = SessionLocal()


# Read Operations
def dbGetOneRecordByColumnName(model: any, columnName: str, value: any):
    return (
        db.query(*model.__table__.columns)
        .filter(getattr(model, columnName) == value)
        .first()
    )


def dbGetAllRecords(model: any):
    # get all the results from the query and return it
    result = db.query(*model.__table__.columns).all()
    return result


def dbGetAllRecordsByColumnName(model: any, columnName: str, value: any):
    # get all the results from the query and return it
    return (
        db.query(*model.__table__.columns)
        .filter(getattr(model, columnName) == value)
        .all()
    )


# Create Operations
def dbCreate(model: any, data: dict):
    result = model(**data)
    db.add(result)
    db.commit()
    return result


# Update Operation
def dbUpdate(model: any, columnName: str, data: dict):
    db.query(model).filter(getattr(model, columnName) == data[columnName]).update(data)
    db.commit()


# Delete Operations
def dbDelete(model: any, id: any):
    db.query(model).filter(model.id == id).delete()
    db.commit()
