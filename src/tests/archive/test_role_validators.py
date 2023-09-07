import unittest
from unittest.mock import patch
from fastapi.testclient import TestClient
from main import app
from unittest import TestCase
from fastapi import status


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
            response.json()["detail"][0]["msg"], "Value error, Name cannot be empty",
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
