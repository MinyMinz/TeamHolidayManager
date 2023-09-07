import unittest
from unittest.mock import patch
from fastapi.testclient import TestClient
from main import app
from unittest import TestCase
from fastapi import status


class Test_Team_Valdiators(TestCase):
    """
    The following tests are for the Team Validators
    """

    @classmethod
    def setUpClass(cls):
        """Setup the test environment once before all tests"""
        cls.client = TestClient(app)
        pass

    def test_team_validator_name_empty(self):
        # test team validator based on team.py Schema
        response = self.client.post(
            "/teams", json={"name": "", "description": "test_description"}
        )
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        self.assertEqual(
            response.json()["detail"][0]["msg"], "Value error, Name cannot be empty",
        )

    @patch("db.crud.create")
    def test_team_validator_description_empty(self, mock_return):
        # test team validator based on team.py Schema with name but description empty returns 200
        # this is because description is not required

        # mock the create method to return a team
        mock_return.return_value = None

        response = self.client.post(
            "/teams",
            json={
                "name": "test_name",
                "description": "",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


if __name__ == "__main__":
    unittest.main()
