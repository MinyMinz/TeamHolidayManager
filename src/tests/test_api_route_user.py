import unittest
from unittest.mock import patch
from fastapi.testclient import TestClient
from main import app
from unittest import TestCase
from fastapi import HTTPException, status


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

    #TODO: Fix this test
    # Create user route tests
    @patch("db.crud.create")
    def test_create_user_sucessful(self, mock_return):
        # Mock the return value of the create function
        mock_return.return_value = None

        response = self.client.post(
            "/users",
            json={
                "email": "test_email",
                "password": "test_password",
                "full_name": "full_name",
                "team_name": "test_team",
                "role_name": "test_role",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # Update user route tests
    @patch("db.crud.update")
    def test_update_user_sucessful(self, mock_return):
        # Mock the return value of the update function
        mock_return.return_value = None

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
    def test_delete_user_sucessful(self, mock_return):
        # Mock the return value of the delete function
        mock_return.return_value = None

        response = self.client.delete(
            "/users?user_id=1",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)


if __name__ == "__main__":
    unittest.main()
