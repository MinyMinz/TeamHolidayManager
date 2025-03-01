import pytest
import httpx
from fastapi import status
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from alembic import command
from alembic.config import Config
# from main import app

# DATABASE_URL = "postgresql://testuser:testpassword@db/testdb"

# @pytest.fixture(scope="session")
# def db_session():
#     engine = create_engine(DATABASE_URL)
#     Session = sessionmaker(bind=engine)
#     session = Session()
    
#     # Run Alembic migrations
#     alembic_cfg = Config("alembic.ini")
#     command.upgrade(alembic_cfg, "head")
    
#     yield session
#     session.close()

# @pytest.fixture(scope="module")
# def client():
#     with httpx.Client(base_url="http://localhost:8000") as client:
#         yield client

# def test_create_holiday_request(client, db_session):
#     # Create a user
#     user_data = {
#         "id": 1,
#         "name": "Test User",
#         "role_name": "User",
#         "number_of_allocated_holidays": 20,
#         "number_of_remaining_holidays": 20,
#     }
#     db_session.execute(
#         "INSERT INTO users (id, name, role_name, number_of_allocated_holidays, number_of_remaining_holidays) VALUES (:id, :name, :role_name, :number_of_allocated_holidays, :number_of_remaining_holidays)",
#         user_data
#     )
#     db_session.commit()
    
#     # Create a holiday request
#     holiday_request_data = {
#         "user_id": 1,
#         "start_date": "2025-03-01",
#         "end_date": "2025-03-05",
#         "status": "Pending"
#     }
#     response = client.post("/holidayRequests", json=holiday_request_data)
#     assert response.status_code == status.HTTP_201_CREATED

#     # Fetch the holiday request
#     response = client.get("/holidayRequests")
#     assert response.status_code == status.HTTP_200_OK
#     assert len(response.json()) == 1
#     assert response.json()[0]["user_id"] == 1
#     assert response.json()[0]["status"] == "Pending"