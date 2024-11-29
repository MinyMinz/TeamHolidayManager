from unittest.mock import patch
from fastapi.testclient import TestClient
from main import app
from unittest import TestCase
from fastapi import HTTPException, status

import unittest

class Test_Api_Role(TestCase):
    """
    The following tests are for the Role API endpoints
    """

    @classmethod
    def setUpClass(cls):
        """Setup the test environment once before all tests"""
        cls.client = TestClient(app)
        pass

    @patch("db.crud.getAllRecords")
    def test_get_all_roles(self, mock_return):
        """Test the get role route of the API"""

        # mock the getAllRecords method to return a list of roles
        mock_return.return_value = [
            {
                "name": "Admin",
                "description": "Admin user",
            },
            {
                "name": "User",
                "description": "Normal user",
            },
        ]

        # call the API endpoint
        response = self.client.get("/roles")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        result = response.json()
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["name"], "Admin")
        self.assertEqual(result[0]["description"], "Admin user")

    @patch("db.crud.getAllRecords")
    def test_get_all_roles_where_no_roles_exist(self, mock_return):
        """Test the get role route of the API"""

        # mock the getAllRecords method to return raised HTTPException 404
        mock_return.side_effect = HTTPException(
            status.HTTP_404_NOT_FOUND, detail="No records found"
        )

        # call the API endpoint
        response = self.client.get("/roles")
        self.assertEqual(response.status_code, 404)
        result = response.json()
        self.assertEqual(result["detail"], "No records found")

    @patch("db.crud.getOneRecordByColumnName")
    def test_get_role_by_name(self, mock_return):
        """Test the get role route of the API"""

        # mock the getOneRecordByColumnName method to return a role
        mock_return.return_value = {
            "name": "Admin",
            "description": "Admin user",
        }

        # call the API endpoint
        response = self.client.get("/roles?role_name=Admin")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        result = response.json()
        self.assertEqual(result["name"], "Admin")
        self.assertEqual(result["description"], "Admin user")

    @patch("db.crud.getOneRecordByColumnName")
    def test_get_role_by_name_where_name_does_not_exist(self, mock_return):
        """Test the get role route of the API"""

        # mock the getOneRecordByColumnName method to return raised HTTPException 404
        mock_return.side_effect = HTTPException(
            status.HTTP_404_NOT_FOUND, detail="No records found"
        )

        # call the API endpoint
        response = self.client.get("/roles?role_name=FakeRoleName")
        self.assertEqual(response.status_code, 404)
        result = response.json()
        self.assertEqual(result["detail"], "No records found")

    @patch("db.crud.create")
    def test_create_role(self, mock_return):
        # mock the create method to do nothing
        mock_return.return_value = None

        # call the API endpoint
        response = self.client.post(
            "/roles",
            json={
                "name": "Test",
                "description": "Test Role",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class Test_Role_Valdiators(TestCase):
    """
    The following tests are for the Role Validators
    """

    @classmethod
    def setUpClass(cls):
        """Setup the test environment once before all tests"""
        cls.client = TestClient(app)
        pass

    def test_role_validator_name_empty(self):
        # test role validator based on role.py Schema
        response = self.client.post(
            "/roles", json={"name": "", "description": "test_description"}
        )
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        self.assertEqual(
            response.json()["detail"][0]["msg"],
            "Value error, Name cannot be empty",
        )

    @patch("db.crud.create")
    def test_role_validator_description_empty(self, mock_return):
        # test role validator based on role.py Schema with name but description empty returns 200
        # this is because description is not required

        # mock the create method to return a role
        mock_return.return_value = None

        response = self.client.post(
            "/roles",
            json={
                "name": "test_name",
                "description": "",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


if __name__ == "__main__":
    unittest.main()
