from db.database import SessionLocal
from fastapi import HTTPException, status

db = SessionLocal()

# Read Operations

# get one result from the query and return it
def getOneRecordByColumnName(model: any, columnName: str, value: any):
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
        db.rollback()
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "Internal Error")
    checkIfResultIsEmpty(result)
    return result

# get all the results from the query and return it
def getAllRecords(model: any, columnToOrderBy: str = None):
    """Get all records from the database based the model Order by the column name
    \n :param model: type any"""
    try:
        query = db.query(*model.__table__.columns)
        if columnToOrderBy is not None:
            query = query.order_by(getattr(model, columnToOrderBy))
        result = query.all()
    except Exception:
        db.rollback()
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "Internal Error")
    checkIfResultIsEmpty(result)
    return result

# get all the results from the query and return it based on the column name and value
def getAllRecordsByColumnName(
    model: any,
    columnName: str,
    value: any,
    columnToOrderBy: str = None,
):
    """Get all records from the database based the model, column name and value
    \n :param model: type any
    \n :param columnName: type str
    \n :param value: type any"""
    try:
        query = db.query(*model.__table__.columns).filter(
            getattr(model, columnName) == value
        )
        if columnToOrderBy is not None:
            query = query.order_by(getattr(model, columnToOrderBy))
        result = query.all()
    except Exception:
        db.rollback()
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "Internal Error")
    checkIfResultIsEmpty(result)
    return result

# Create Operations
# create a record in the database based on the model and data
def create(model: any, data: dict):
    """Create a record in the database based on the model and data
    \n :param model: type any
    \n :param data: type dict"""
    try:
        # model(**data) unpacks the dictionary and maps it to the model
        db.add(model(**data))
        db.commit()
    except Exception:
        db.rollback()
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "Internal Error")

# Update Operation
def update(model: any, columnName: str, data: dict):
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
        db.rollback()
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "Internal Error")

# Delete Operation
def delete(model: any, columnName: str, uid: any):
    """delete a record in the database based on the model and uid
    \n :param model: type any
    \n :param columnName: type str
    \n :param uid: type any"""
    try:
        db.query(model).filter(getattr(model, columnName) == uid).delete()
        db.commit()
    except Exception:
        db.rollback()
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "Internal Error")

# User Specific update password only
def updatePassword(model: any, id: int, data: dict):
    """Update a record in the database based on the model, column name and data
    \n :param model: type any
    \n :param columnName: type str
    \n :param data: type dict"""
    try:
        db.query(model).filter(getattr(model, "id") == id).update(
            {"password": data["password"]}
        )
        db.commit()
    except Exception as e:
        print(e)
        db.rollback()
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "Internal Error")

# holidayRequest Specific
from models.holidayRequests import HolidayRequests as holidayModel
from models.user import Users as userModel

# get all holiday requests for a specific user or team and return full name with user id
def getHolidayRequestsByField(columnName: str, value: any, columnToOrderBy: str = None):
    try:
        fields = [*holidayModel.__table__.columns, getattr(userModel, "full_name")]
        query = (
            db.query(*fields)
            .filter(getattr(holidayModel, columnName) == value)
            .join(userModel, isouter=True)
        )
        if columnToOrderBy is not None:
            query = query.order_by(getattr(holidayModel, columnToOrderBy))
        result = query.all()
    except Exception:
        db.rollback()
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "Internal Error")
    checkIfResultIsEmpty(result)
    return result

# get all holiday requests return full name with user id
def getAllHolidayRequests(columnToOrderBy: str = None):
    try:
        fields = [*holidayModel.__table__.columns, getattr(userModel, "full_name")]
        query = db.query(*fields).join(userModel, isouter=True)
        if columnToOrderBy is not None:
            query = query.order_by(getattr(holidayModel, columnToOrderBy))
        result = query.all()
    except Exception:
        db.rollback()
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "Internal Error")
    checkIfResultIsEmpty(result)
    return result

# Helper Functions
def checkIfResultIsEmpty(result: any):
    """@Helper Function
    \n Check if the result is empty and raise an exception if it is
    \n :param result: type any"""
    if not result or len(result) == 0:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "No records found")
