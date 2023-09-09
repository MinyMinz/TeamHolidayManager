from ddt import ddt, data, unpack
from unittest.mock import patch
from fastapi.testclient import TestClient
from main import app
from unittest import TestCase
from fastapi import HTTPException, status

import unittest


class Test_Api_User(TestCase):
    """
    The following tests are for the User API endpoints
    """

    @classmethod
    def setUpClass(cls):
        """Setup the test environment once before all tests"""
        cls.client = TestClient(app)
        pass

    # Login route tests
    @patch("db.crud.getOneRecordByColumnName")
    def test_login_user_sucessful(self, mock_return):
        # Mock the return value of the getOneRecordByColumnName function
        mock_return.return_value = {
            "id": 1,
            "email": "test_email",
            "password": "test_password",
            "full_name": "full_name",
            "team_name": "test_team",
            "role_name": "test_role",
        }

        # call the API endpoint
        response = self.client.post(
            "/users/login", json={"email": "test_email", "password": "test_password"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch("db.crud.getOneRecordByColumnName")
    def test_login_user_where_user_does_not_exist(self, mock_return):
        # Mock the return value of the getOneRecordByColumnName function to return HTTPException 404
        mock_return.side_effect = HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No records found"
        )

        # call the API endpoint
        response = self.client.post(
            "/users/login",
            json={"email": "test_email", "password": "test_password"},
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # Get all users route tests
    @patch("db.crud.getAllRecords")
    def test_get_all_users_sucessful(self, mock_return):
        # Mock the return value of the getAllRecords function
        mock_return.return_value = [
            {
                "id": 1,
                "email": "test_email",
                "password": "test_password",
                "full_name": "full_name",
                "team_name": "test_team",
                "role_name": "test_role",
            },
            {
                "id": 2,
                "email": "test_email2",
                "password": "test_password2",
                "full_name": "full_name2",
                "team_name": "test_team2",
                "role_name": "test_role2",
            },
        ]

        # call the API endpoint
        response = self.client.get(
            "/users",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 2)
        self.assertEqual(response.json()[0]["id"], 1)
        self.assertEqual(response.json()[0]["email"], "test_email")

    @patch("db.crud.getAllRecords")
    def test_get_all_users_where_no_users_exist(self, mock_return):
        # Mock the return value of the getAllRecords function to return HTTPException 404
        mock_return.side_effect = HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No records found"
        )

        # call the API endpoint
        response = self.client.get(
            "/users",
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # Get user by id route tests
    @patch("db.crud.getOneRecordByColumnName")
    def test_get_user_by_id_sucessful(self, mock_return):
        # Mock the return value of the getOneRecordByColumnName function
        mock_return.return_value = {
            "id": 1,
            "email": "test_email",
            "password": "test_password",
            "full_name": "full_name",
            "team_name": "test_team",
            "role_name": "test_role",
        }

        # call the API endpoint
        response = self.client.get(
            "/users?user_id=1",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["id"], 1)
        self.assertEqual(response.json()["email"], "test_email")

    @patch("db.crud.getOneRecordByColumnName")
    def test_get_user_by_id_where_user_does_not_exist(self, mock_return):
        # Mock the return value of the getOneRecordByColumnName function to return HTTPException 404
        mock_return.side_effect = HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No records found"
        )

        # call the API endpoint
        response = self.client.get(
            "/users?user_id=1",
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # Get user by email route tests
    @patch("db.crud.getOneRecordByColumnName")
    def test_get_user_by_email_sucessful(self, mock_return):
        # Mock the return value of the getOneRecordByColumnName function
        mock_return.return_value = {
            "id": 1,
            "email": "test_email",
            "password": "test_password",
            "full_name": "full_name",
            "team_name": "test_team",
            "role_name": "test_role",
        }

        # call the API endpoint
        response = self.client.get(
            "/users?email=test_email",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["id"], 1)
        self.assertEqual(response.json()["email"], "test_email")

    @patch("db.crud.getOneRecordByColumnName")
    def test_get_user_by_email_where_user_does_not_exist(self, mock_return):
        # Mock the return value of the getOneRecordByColumnName function to return HTTPException 404
        mock_return.side_effect = HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No records found"
        )

        response = self.client.get(
            "/users?email=test_email",
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # Get all users by team name route tests
    @patch("db.crud.getAllRecordsByColumnName")
    def test_get_all_users_by_team_name_sucessful(self, mock_return):
        # Mock the return value of the getAllRecordsByColumnName function
        mock_return.return_value = [
            {
                "id": 1,
                "email": "test_email",
                "password": "test_password",
                "full_name": "full_name",
                "team_name": "test_team",
                "role_name": "test_role",
            },
            {
                "id": 2,
                "email": "test_email2",
                "password": "test_password2",
                "full_name": "full_name2",
                "team_name": "test_team",
                "role_name": "test_role",
            },
        ]

        response = self.client.get(
            "/users?team=test_team",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 2)
        self.assertEqual(response.json()[0]["id"], 1)
        self.assertEqual(response.json()[0]["email"], "test_email")

    @patch("db.crud.getAllRecordsByColumnName")
    def test_get_all_users_by_team_name_where_no_users_exist(self, mock_return):
        # Mock the return value of the getAllRecordsByColumnName function to return HTTPException 404
        mock_return.side_effect = HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No records found"
        )

        response = self.client.get(
            "/users?team=test_team",
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # Create user route tests
    @patch("db.crud.create")
    @patch("db.crud.getOneRecordByColumnName")
    def test_create_user_sucessful(self, mock_get, mock_create):
        # Mock the return value of the getOneRecordByColumnName function
        mock_get.return_value = None

        # Mock the return value of the create function
        mock_create.return_value = None

        response = self.client.post(
            "/users",
            json={
                "id": None,
                "email": "test_email",
                "password": "test_password",
                "full_name": "full_name",
                "team_name": "test_team",
                "role_name": "test_role",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # Update user route tests
    @patch("db.crud.getOneRecordByColumnName")
    @patch("db.crud.update")
    def test_update_user_sucessful(self, mock_get, mock_update):
        # Mock the return value of the getOneRecordByColumnName function
        mock_get.return_value = {
            "id": 1,
            "email": "test_email",
            "password": "test_password",
            "full_name": "full_name",
            "team_name": "test_team",
            "role_name": "test_role",
        }

        # Mock the return value of the update function
        mock_update.return_value = None

        response = self.client.put(
            "/users",
            json={
                "id": 1,
                "email": "test_email",
                "password": "test_password",
                "full_name": "full_name",
                "team_name": "test_team",
                "role_name": "test_role",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Delete user route tests
    @patch("db.crud.delete")
    @patch("db.crud.getOneRecordByColumnName")
    def test_delete_user_sucessful(self, mock_get, mock_delete):
        # Mock the return value of the getOneRecordByColumnName function
        mock_get.return_value = {
            "id": 2,
            "email": "test_email",
            "password": "test_password",
            "full_name": "full_name",
            "team_name": "test_team",
            "role_name": "SuperAdmin",
        }

        # Mock the return value of the delete function
        mock_delete.return_value = None

        response = self.client.delete(
            "/users?user_id=1",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)


@ddt
class Test_User_Valdiators(TestCase):
    """
    The following tests are for the User Validator
    """

    @classmethod
    def setUpClass(cls):
        """Setup the test environment once before all tests"""
        cls.client = TestClient(app)
        pass

    @data(
        ("email", "test_email"),
        ("password", "test_password"),
        ("full_name", "test_name"),
        ("team_name", "test_team"),
        ("role_name", "test_role"),
    )
    @unpack
    def test_user_validator_empty_fields_on_create(self, field_name, field_value):
        """Parameterized test for user validator based on user.py Schema"""

        # test user validator based on user.py Schema
        response = self.client.post(
            "/users",
            json={
                "id": None,
                field_name: None,
                "email": field_value if field_name != "email" else "",
                "password": field_value if field_name != "password" else "",
                "full_name": field_value if field_name != "full_name" else "",
                "team_name": field_value if field_name != "team_name" else "",
                "role_name": field_value if field_name != "role_name" else "",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        self.assertEqual(
            response.json()["detail"][0]["msg"],
            f"Value error, {field_name} cannot be empty",
        )

    @data(
        ("email", "test_email"),
        ("password", "test_password"),
        ("full_name", "test_name"),
        ("team_name", "test_team"),
        ("role_name", "test_role"),
    )
    @unpack
    def test_user_validator_empty_fields_on_update(self, field_name, field_value):
        """Parameterized test for user validator based on user.py Schema"""

        # test user validator based on user.py Schema
        response = self.client.put(
            "/users",
            json={
                "id": 1,
                field_name: None,
                "email": field_value if field_name != "email" else "",
                "password": field_value if field_name != "password" else "",
                "full_name": field_value if field_name != "full_name" else "",
                "team_name": field_value if field_name != "team_name" else "",
                "role_name": field_value if field_name != "role_name" else "",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        self.assertEqual(
            response.json()["detail"][0]["msg"],
            f"Value error, {field_name} cannot be empty",
        )


if __name__ == "__main__":
    unittest.main()
