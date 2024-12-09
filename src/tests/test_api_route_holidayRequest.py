from os import environ as env
from unittest.mock import patch
from fastapi.testclient import TestClient
from main import app
from unittest import TestCase
from fastapi import HTTPException, status
from jose import jwt

import unittest

SECRET_KEY = env["SECRET_KEY"]
ALGORITHM = env["ALGORITHM"]

token = jwt.encode({"sub": "test_email", "id": 1}, SECRET_KEY, algorithm=ALGORITHM)
headers = {"Authorization": f"Bearer {token}"}

class Test_Api_HolidayRequest(TestCase):
    """
    The following tests are for the HolidayRequest API endpoints
    """

    @classmethod
    def setUpClass(cls):
        """Setup the test environment once before all tests"""
        cls.client = TestClient(app)
        pass

    # Get all holiday-request route tests
    @patch("db.crud.getAllHolidayRequests")
    def test_get_all_holiday_request_successful(self, mock_return):
        # Mock the return value of the getAllRecords function
        # based on holidayReuqest.py Schema
        mock_return.return_value = [
            {
                "id": 1,
                "description": "test_description",
                "start_date": "2021-01-01",
                "end_date": "2021-01-01",
                "time_of_day": "AM",
                "team_name": "test_team",
                "user_id": 1,
                "full_name": "test_user1",
            },
            {
                "id": 1,
                "description": "test_description",
                "start_date": "2023-01-01",
                "end_date": "2023-01-31",
                "time_of_day": None,
                "team_name": "test_team",
                "user_id": 1,
                "full_name": "test_user1",
            },
            {
                "id": 2,
                "description": "test_description",
                "start_date": "2022-12-31",
                "end_date": "2022-12-31",
                "time_of_day": "PM",
                "team_name": "test_team",
                "user_id": 2,
                "full_name": "test_user2",
            },
        ]

        # call the API endpoint
        response = self.client.get(
            "/holiday-request",
            headers = headers
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 3)
        self.assertEqual(response.json()[0]["id"], 1)
        self.assertEqual(response.json()[0]["description"], "test_description")

    @patch("db.crud.getAllHolidayRequests")
    def test_get_all_holiday_request_where_no_holiday_request_exist(self, mock_return):
        # Mock the return value of the getAllRecords function to return HTTPException 404
        mock_return.side_effect = HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No records found"
        )

        # call the API endpoint
        response = self.client.get(
            "/holiday-request",
            headers = headers
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # Get all holiday-request by team name route tests
    @patch("db.crud.getHolidayRequestsByField")
    def test_get_all_holiday_request_by_team_name_successful(self, mock_return):
        token = jwt.encode({"id": 1, "sub": "test_email", "role_name": "Admin", "team_name": "test_team"}, SECRET_KEY, algorithm=ALGORITHM)
        headers = {"Authorization": f"Bearer {token}"}
        # Mock the return value of the getAllRecordsByColumnName function
        mock_return.return_value = [
            {
                "id": 1,
                "description": "test_description1",
                "start_date": "2021-01-01",
                "end_date": "2021-01-01",
                "time_of_day": "AM",
                "team_name": "test_team",
                "user_id": 1,
                "full_name": "test_user1",
            },
            {
                "id": 2,
                "description": "test_description2",
                "start_date": "2022-12-31",
                "end_date": "2022-12-31",
                "time_of_day": "PM",
                "team_name": "test_team",
                "user_id": 1,
                "full_name": "test_user1",
            },
        ]

        response = self.client.get(
            "/holiday-request",
            headers = headers
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 2)
        self.assertEqual(response.json()[0]["id"], 1)
        self.assertEqual(response.json()[0]["description"], "test_description1")
        self.assertEqual(response.json()[0]["user_id"], 1)
        self.assertEqual(response.json()[0]["full_name"], "test_user1")
        self.assertEqual(response.json()[1]["id"], 2)
        self.assertEqual(response.json()[1]["description"], "test_description2")
        self.assertEqual(response.json()[1]["user_id"], 1)
        self.assertEqual(response.json()[1]["full_name"], "test_user1")

    @patch("db.crud.getHolidayRequestsByField")
    def test_get_all_holiday_request_by_team_name_where_no_holiday_request_exist(self, mock_return):
        token = jwt.encode({"id": 1, "sub": "test_email", "role_name": "Admin", "team_name": "test_team"}, SECRET_KEY, algorithm=ALGORITHM)
        headers = {"Authorization": f"Bearer {token}"}
        # Mock the return value of the getAllRecordsByColumnName function to return HTTPException 404
        mock_return.side_effect = HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No records found"
        )

        response = self.client.get(
            "/holiday-request",
            headers = headers
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # Get all holiday-request by user id route tests
    @patch("db.crud.getHolidayRequestsByField")
    def test_get_all_holiday_request_by_user_id_successful(self, mock_return):
        token = jwt.encode({"id": 1, "sub": "test_email", "role_name": "User", "team_name": "test_team"}, SECRET_KEY, algorithm=ALGORITHM)
        headers = {"Authorization": f"Bearer {token}"}
        # Mock the return value of the getAllRecordsByColumnName function
        mock_return.return_value = [
            {
                "id": 1,
                "description": "test_description1",
                "start_date": "2021-01-01",
                "end_date": "2021-01-01",
                "time_of_day": "AM",
                "team_name": "test_team",
                "user_id": 1,
                "full_name": "test_user1",
            },
            {
                "id": 2,
                "description": "test_description2",
                "start_date": "2022-12-31",
                "end_date": "2022-12-31",
                "time_of_day": "PM",
                "team_name": "test_team",
                "user_id": 1,
                "full_name": "test_user1",
            },
        ]

        response = self.client.get(
            "/holiday-request?user_id=1",
            headers = headers
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 2)
        self.assertEqual(response.json()[0]["id"], 1)
        self.assertEqual(response.json()[0]["description"], "test_description1")
        self.assertEqual(response.json()[0]["user_id"], 1)
        self.assertEqual(response.json()[0]["full_name"], "test_user1")
        self.assertEqual(response.json()[1]["id"], 2)
        self.assertEqual(response.json()[1]["description"], "test_description2")
        self.assertEqual(response.json()[0]["user_id"], 1)
        self.assertEqual(response.json()[0]["full_name"], "test_user1")

    # Create holidayRequest route tests
    @patch("db.crud.create")
    def test_create_holidayRequest_successful(self, mock_return):
        # Mock the return value of the create function
        mock_return.return_value = None

        response = self.client.post(
            "/holiday-request",
            json={
                "description": "test_description",
                "start_date": "2021-01-01",
                "end_date": "2021-01-01",
                "time_of_day": "AM",
                "team_name": "test_team",
                "user_id": 1,
            },
            headers = headers
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # Update holidayRequest route tests
    @patch("db.crud.getOneRecordByColumnName")
    @patch("db.crud.update")
    def test_update_holidayRequest_successful(self, mock_get, mock_update):
        # Mock the return value of the getOneRecordByColumnName function
        mock_get.return_value = {
            "id": 1,
            "description": "test_description",
            "start_date": "2021-01-01",
            "end_date": "2021-01-01",
            "time_of_day": "AM",
            "team_name": "test_team",
            "user_id": 1,
        }

        # Mock the return value of the update function
        mock_update.return_value = None

        response = self.client.put(
            "/holiday-request",
            json={
                "id": 1,
                "description": "test_description",
                "start_date": "2021-01-01",
                "end_date": "2021-01-01",
                "time_of_day": "AM",
                "team_name": "test_team",
                "user_id": 1,
            },
            headers = headers
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Test holidayReuqest validator
    def test_holidayRequest_validator(self):
        # Test that the validator returns an error if the start date is after the end date
        response = self.client.post(
            "/holiday-request",
            json={
                "description": "test_description",
                "start_date": "2021-01-02",
                "end_date": "2021-01-01",
                "time_of_day": "AM",
                "team_name": "test_team",
                "user_id": 1,
            },
            headers = headers
        )
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)

    # Delete holidayRequest route tests
    @patch("db.crud.delete")
    @patch("db.crud.getOneRecordByColumnName")
    def test_delete_holidayRequest_successful(self, mock_get, mock_delete):
        # Mock the return value of the getOneRecordByColumnName function
        mock_get.return_value = {
            "id": 1,
            "description": "test_description",
            "start_date": "2021-01-01",
            "end_date": "2021-01-01",
            "time_of_day": "AM",
            "team_name": "test_team",
            "user_id": 1,
        }

        # Mock the return value of the delete function
        mock_delete.return_value = None

        response = self.client.delete(
            "/holiday-request?holiday_id=1",
            headers = headers
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class Test_HolidayRequest_Valdiators(TestCase):
    """
    The following tests are for the HolidayRequest Validator
    """

    @classmethod
    def setUpClass(cls):
        """Setup the test environment once before all tests"""
        cls.client = TestClient(app)
        pass

    def test_holiday_request_validator_empty_team_name_on_create(self):
        """Test for HolidayRequest validator based on HolidayRequest.py Schema"""

        # test user validator based on user.py Schema
        response = self.client.post(
            "/holiday-request",
            json={
                "id": None,
                "description": "description",
                "start_date": "2021-01-01",
                "end_date": "2021-01-01",
                "time_of_day": "AM",
                "team_name": "",
                "user_id": 1,
            },
            headers = headers
        )
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        self.assertEqual(
            response.json()["detail"][0]["msg"],
            f"Value error, team_name cannot be empty",
        )
    
    def test_holiday_request_validator_empty_user_id_on_create(self):
        """Test for HolidayRequest validator based on HolidayRequest.py Schema"""

        # test user validator based on user.py Schema
        response = self.client.post(
            "/holiday-request",
            json={
                "id": None,
                "description": "description",
                "start_date": "2021-01-01",
                "end_date": "2021-01-01",
                "time_of_day": "AM",
                "team_name": "team_name",
                "user_id": None,
            },
            headers = headers
        )
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        self.assertEqual(
            response.json()["detail"][0]["msg"],
            f"Input should be a valid integer",
        )

    def test_holiday_request_validator_empty_start_date(self):
        """Test for HolidayRequest validator based on HolidayRequest.py Schema"""

        # test user validator based on user.py Schema
        response = self.client.post(
            "/holiday-request",
            json={
                "id": None,
                "description": "description",
                "start_date": None,
                "end_date": "2021-01-01",
                "time_of_day": "AM",
                "team_name": "team_name",
            },
            headers = headers
        )
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        self.assertEqual(
            response.json()["detail"][0]["msg"], "Input should be a valid date"
        )

    def test_holiday_request_validator_empty_end_date(self):
        """Test for HolidayRequest validator based on HolidayRequest.py Schema"""

        # test user validator based on user.py Schema
        response = self.client.post(
            "/holiday-request",
            json={
                "id": None,
                "description": "description",
                "start_date": None,
                "end_date": "2021-01-01",
                "time_of_day": "AM",
                "team_name": "team_name",
            },
            headers = headers
        )
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        self.assertEqual(
            response.json()["detail"][0]["msg"], "Input should be a valid date"
        )

    def test_holiday_request_validator_dates_are_equal_and_time_of_day_field_not_set(
        self,
    ):
        """Test for HolidayRequest validator based on HolidayRequest.py Schema"""

        # test user validator based on user.py Schema
        response = self.client.post(
            "/holiday-request",
            json={
                "id": None,
                "description": "description",
                "start_date": "2021-01-01",
                "end_date": "2021-01-01",
                "time_of_day": None,
                "team_name": "team_name",
            },
            headers = headers
        )
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        self.assertEqual(
            response.json()["detail"][0]["msg"],
            "Value error, TimeOfDay is required when start_date and end_date are the same",
        )

    def test_holiday_request_validator_date_fields_are_equal_and_time_of_day_field_invalid(
        self,
    ):
        """Test for HolidayRequest validator based on HolidayRequest.py Schema"""

        # test user validator based on user.py Schema
        response = self.client.post(
            "/holiday-request",
            json={
                "id": None,
                "description": "description",
                "start_date": "2021-01-01",
                "end_date": "2021-01-01",
                "time_of_day": "AB",
                "team_name": "team_name",
            },
            headers = headers
        )
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        self.assertEqual(
            response.json()["detail"][0]["msg"],
            "Value error, TimeOfDay must be either 'AM' or 'PM'.",
        )


if __name__ == "__main__":
    unittest.main()
