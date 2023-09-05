from db.database import SessionLocal
from fastapi import HTTPException, status

db = SessionLocal()


# Read Operations
def dbGetOneRecordByColumnName(model: any, columnName: str, value: any):
    """Get one record from the database based on the model, column name and value
    \n :param model: type any
    \n :param columnName: type str
    \n :param value: type any"""
    try:
        # get the first result from the query and return it
        result = (
            db.query(*model.__table__.columns)
            .filter(getattr(model, columnName) == value)
            .first()
        )
    except Exception:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "Internal Error")
    checkIfResultIsEmpty(result)
    return result


def dbGetAllRecords(model: any):
    """Get all records from the database based the model
    \n :param model: type any"""
    try:
        result = db.query(*model.__table__.columns).all()
    except Exception:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "Internal Error")
    checkIfResultIsEmpty(result)
    return result


# get all the results from the query and return it based on the column name and value
def dbGetAllRecordsByColumnName(model: any, columnName: str, value: any):
    """Get all records from the database based the model, column name and value
    \n :param model: type any
    \n :param columnName: type str
    \n :param value: type any"""
    try:
        result = (
            db.query(*model.__table__.columns)
            .filter(getattr(model, columnName) == value)
            .all()
        )
    except Exception:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "Internal Error")
    checkIfResultIsEmpty(result)
    return result


# Create Operations
def dbCreate(model: any, data: dict):
    """Create a record in the database based on the model and data
    \n :param model: type any
    \n :param data: type dict"""
    try:
        mappedModel = model(**data)
        db.add(mappedModel)
        db.commit()
    except Exception as e:
        print(e)
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "Internal Error")


# Update Operation
def dbUpdate(model: any, columnName: str, data: dict):
    """Update a record in the database based on the model, column name and data
    \n :param model: type any
    \n :param columnName: type str
    \n :param data: type dict"""
    try:
        db.query(model).filter(getattr(model, columnName) == data[columnName]).update(
            data
        )
        db.commit()
    except Exception:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "Internal Error")


# Delete Operations
def dbDelete(model: any, uid: any):
    """delete a record in the database based on the model and uid
    \n :param model: type any
    \n :param uid: type any"""
    try:
        db.query(model).filter(model.id == uid).delete()
        db.commit()
    except Exception:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "Internal Error")


# Helper Functions
def checkIfResultIsEmpty(result: any):
    """@Helper Function
    \n Check if the result is empty and raise an exception if it is
    \n :param result: type any"""
    if not result or len(result) == 0:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "No records found")
