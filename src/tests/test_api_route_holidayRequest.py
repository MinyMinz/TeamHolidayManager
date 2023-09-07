from ddt import ddt, data, unpack
from unittest.mock import patch
from fastapi.testclient import TestClient
from main import app
from unittest import TestCase
from fastapi import HTTPException, status

# from datetime import date

import unittest


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
    @patch("db.crud.getAllRecords")
    def test_get_all_holiday_request_sucessful(self, mock_return):
        # Mock the return value of the getAllRecords function
        # based on holidayReuqest.py Schema
        mock_return.return_value = [
            {
                "id": 1,
                "description": "test_description",
                "start_date": "2021-01-01",
                "end_date": "2021-01-01",
                "morning_or_afternoon": "AM",
                "team_name": "test_team",
                "user_id": 1,
            },
            {
                "id": 1,
                "description": "test_description",
                "start_date": "2023-01-01",
                "end_date": "2023-01-31",
                "morning_or_afternoon": None,
                "team_name": "test_team",
                "user_id": 1,
            },
            {
                "id": 2,
                "description": "test_description",
                "start_date": "2022-12-31",
                "end_date": "2022-12-31",
                "morning_or_afternoon": "PM",
                "team_name": "test_team",
                "user_id": 2,
            },
        ]

        # call the API endpoint
        response = self.client.get(
            "/holiday-request",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 3)
        self.assertEqual(response.json()[0]["id"], 1)
        self.assertEqual(response.json()[0]["description"], "test_description")

    @patch("db.crud.getAllRecords")
    def test_get_all_holiday_request_where_no_holiday_request_exist(self, mock_return):
        # Mock the return value of the getAllRecords function to return HTTPException 404
        mock_return.side_effect = HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No records found"
        )

        # call the API endpoint
        response = self.client.get(
            "/holiday-request",
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # Get all holiday-request by team name route tests
    @patch("db.crud.getAllRecordsByColumnName")
    def test_get_all_holiday_request_by_team_name_sucessful(self, mock_return):
        # Mock the return value of the getAllRecordsByColumnName function
        mock_return.return_value = [
            {
                "id": 1,
                "description": "test_description1",
                "start_date": "2021-01-01",
                "end_date": "2021-01-01",
                "morning_or_afternoon": "AM",
                "team_name": "test_team",
                "user_id": 1,
            },
            {
                "id": 2,
                "description": "test_description2",
                "start_date": "2022-12-31",
                "end_date": "2022-12-31",
                "morning_or_afternoon": "PM",
                "team_name": "test_team",
                "user_id": 1,
            },
        ]

        response = self.client.get(
            "/holiday-request?team_name=test_team",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 2)
        self.assertEqual(response.json()[0]["id"], 1)
        self.assertEqual(response.json()[0]["description"], "test_description1")
        self.assertEqual(response.json()[1]["id"], 2)
        self.assertEqual(response.json()[1]["description"], "test_description2")

    @patch("db.crud.getAllRecordsByColumnName")
    def test_get_all_holiday_request_by_team_name_where_no_holiday_request_exist(
        self, mock_return
    ):
        # Mock the return value of the getAllRecordsByColumnName function to return HTTPException 404
        mock_return.side_effect = HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No records found"
        )

        response = self.client.get(
            "/holiday-request?team_name=test_team",
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # Get all holiday-request by user id route tests
    @patch("db.crud.getAllRecordsByColumnName")
    def test_get_all_holiday_request_by_user_id_sucessful(self, mock_return):
        # Mock the return value of the getAllRecordsByColumnName function
        mock_return.return_value = [
            {
                "id": 1,
                "description": "test_description1",
                "start_date": "2021-01-01",
                "end_date": "2021-01-01",
                "morning_or_afternoon": "AM",
                "team_name": "test_team",
                "user_id": 1,
            },
            {
                "id": 2,
                "description": "test_description2",
                "start_date": "2022-12-31",
                "end_date": "2022-12-31",
                "morning_or_afternoon": "PM",
                "team_name": "test_team",
                "user_id": 1,
            },
        ]

        response = self.client.get(
            "/holiday-request?user_id=1",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 2)
        self.assertEqual(response.json()[0]["id"], 1)
        self.assertEqual(response.json()[0]["description"], "test_description1")
        self.assertEqual(response.json()[0]["user_id"], 1)
        self.assertEqual(response.json()[1]["id"], 2)
        self.assertEqual(response.json()[1]["description"], "test_description2")
        self.assertEqual(response.json()[0]["user_id"], 1)

    # Create holidayRequest route tests
    @patch("db.crud.create")
    def test_create_holidayRequest_sucessful(self, mock_return):
        # Mock the return value of the create function
        mock_return.return_value = None

        response = self.client.post(
            "/holiday-request",
            json={
                "description": "test_description",
                "start_date": "2021-01-01",
                "end_date": "2021-01-01",
                "morning_or_afternoon": "AM",
                "team_name": "test_team",
                "user_id": 1,
            },
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # Update holidayRequest route tests
    @patch("db.crud.getOneRecordByColumnName")
    @patch("db.crud.update")
    def test_update_holidayRequest_sucessful(self, mock_get, mock_update):
        # Mock the return value of the getOneRecordByColumnName function
        mock_get.return_value = {
            "id": 1,
            "description": "test_description",
            "start_date": "2021-01-01",
            "end_date": "2021-01-01",
            "morning_or_afternoon": "AM",
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
                "morning_or_afternoon": "AM",
                "team_name": "test_team",
                "user_id": 1,
            },
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
                "morning_or_afternoon": "AM",
                "team_name": "test_team",
                "user_id": 1,
            },
        )
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)

    # Delete holidayRequest route tests
    @patch("db.crud.getOneRecordByColumnName")
    @patch("db.crud.delete")
    def test_delete_holidayRequest_sucessful(self, mock_get, mock_delete):
        # Mock the return value of the getOneRecordByColumnName function
        mock_get.return_value = {
            "id": 1,
            "description": "test_description",
            "start_date": "2021-01-01",
            "end_date": "2021-01-01",
            "morning_or_afternoon": "AM",
            "team_name": "test_team",
            "user_id": 1,
        }

        # Mock the return value of the delete function
        mock_delete.return_value = None

        response = self.client.delete(
            "/holiday-request?holiday_id=1",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)


@ddt
class Test_HolidayRequest_Valdiators(TestCase):
    """
    The following tests are for the HolidayRequest Validator
    """

    @classmethod
    def setUpClass(cls):
        """Setup the test environment once before all tests"""
        cls.client = TestClient(app)
        pass

    def test_holiday_request_validator_empty_standard_fields_on_create(self):
        """Parameterized test for HolidayRequest validator when doing POST request based on HolidayRequest.py Schema"""

        # test user validator based on user.py Schema
        response = self.client.post(
            "/holiday-request",
            json={
                "id": None,
                "description": "description",
                "start_date": "2021-01-01",
                "end_date": "2021-01-01",
                "morning_or_afternoon": "AM",
                "team_name": "",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        self.assertEqual(
            response.json()["detail"][0]["msg"],
            f"Value error, team_name cannot be empty",
        )

    @data(
        ("start_date", "2021-01-01"),
        ("end_date", "2023-12-12"),
    )
    @unpack
    def test_holiday_request_validator_empty_date_fields_on_create(
        self, field_name, field_value
    ):
        """Parameterized test for HolidayRequest validator when doing POST request based on HolidayRequest.py Schema"""

        # test user validator based on user.py Schema
        response = self.client.post(
            "/holiday-request",
            json={
                "id": None,
                field_name: None,
                "description": "description",
                "start_date": field_value if field_name != "start_date" else None,
                "end_date": "2023-12-12" if field_name != "end_date" else None,
                "morning_or_afternoon": "AM",
                "team_name": "team_name",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        self.assertEqual(
            response.json()["detail"][0]["msg"], "Input should be a valid date"
        )

    def test_holiday_request_validator_date_fields_are_equal_and_morning_or_afternoon_field_not_set_on_create(
        self,
    ):
        """Parameterized test for HolidayRequest validator when doing POST request based on HolidayRequest.py Schema"""

        # test user validator based on user.py Schema
        response = self.client.post(
            "/holiday-request",
            json={
                "id": None,
                "description": "description",
                "start_date": "2021-01-01",
                "end_date": "2021-01-01",
                "morning_or_afternoon": None,
                "team_name": "team_name",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        self.assertEqual(
            response.json()["detail"][0]["msg"],
            "Value error, Field is required when start_date and end_date are the same",
        )

    def test_holiday_request_validator_date_fields_are_equal_and_morning_or_afternoon_field_invalid_create(
        self,
    ):
        """Parameterized test for HolidayRequest validator when doing POST request based on HolidayRequest.py Schema"""

        # test user validator based on user.py Schema
        response = self.client.post(
            "/holiday-request",
            json={
                "id": None,
                "description": "description",
                "start_date": "2021-01-01",
                "end_date": "2021-01-01",
                "morning_or_afternoon": "AB",
                "team_name": "team_name",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        self.assertEqual(
            response.json()["detail"][0]["msg"],
            "Value error, morning_or_afternoon must be either 'AM' or 'PM'.",
        )


if __name__ == "__main__":
    unittest.main()
