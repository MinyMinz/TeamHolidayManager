import os
from unittest.mock import patch
from fastapi.testclient import TestClient
from main import app
from unittest import TestCase
from fastapi import HTTPException, status

import unittest

class Test_Api_Team(TestCase):
    """
    The following tests are for the Team API endpoints
    """

    @classmethod
    def setUpClass(cls):
        """Setup the test environment once before all tests"""
        os.environ['DATABASE_URL'] = "postgresql://user:password@postgresDB:5432/holidaymanager"
        cls.client = TestClient(app)
        pass

    @patch("db.crud.getAllRecords")
    def test_get_all_Teams(self, mock_return):
        # mock the getAllRecords method to return a list of Teams
        mock_return.return_value = [
            {
                "name": "GG",
                "description": "Team GG",
            },
            {
                "name": "HH",
                "description": "Team HH",
            },
            {
                "name": "II",
                "description": "Team II",
            },
        ]

        # call the API endpoint
        response = self.client.get("/teams")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        result = response.json()
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0]["name"], "GG")
        self.assertEqual(result[0]["description"], "Team GG")

    @patch("db.crud.getAllRecords")
    def test_get_all_Teams_where_no_teams_exist(self, mock_return):
        # mock the getAllRecords method to return a list of Teams
        mock_return.side_effect = HTTPException(
            status.HTTP_404_NOT_FOUND, detail="No records found"
        )

        # call the API endpoint
        response = self.client.get("/teams")
        self.assertEqual(response.status_code, 404)
        result = response.json()
        self.assertEqual(result["detail"], "No records found")

    @patch("db.crud.getOneRecordByColumnName")
    def test_get_Team_by_name(self, mock_return):
        # mock the getOneRecordByColumnName method to return a Team
        mock_return.return_value = {
            "name": "GG",
            "description": "Team GG",
        }

        response = self.client.get("/teams?team_name=GG")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        result = response.json()
        self.assertEqual(result["name"], "GG")
        self.assertEqual(result["description"], "Team GG")

    @patch("db.crud.getOneRecordByColumnName")
    def test_get_Team_by_name_where_name_does_not_exist(self, mock_return):
        # mock the getOneRecordByColumnName method to return a Team
        mock_return.side_effect = HTTPException(
            status.HTTP_404_NOT_FOUND, detail="No records found"
        )

        # call the API endpoint
        response = self.client.get("/teams?team_name=FakeTeamName")
        self.assertEqual(response.status_code, 404)
        result = response.json()
        self.assertEqual(result["detail"], "No records found")

    @patch("db.crud.create")
    def test_create_team(self, mock_return):
        # mock the create method to do nothing
        mock_return.return_value = None

        # call the API endpoint
        response = self.client.post(
            "/teams",
            json={
                "name": "TestTeam",
                "description": "Test Team",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @patch("db.crud.update")
    def test_update_team(self, mock_return):
        # mock the update method to do nothing
        mock_return.return_value = None

        # call the API endpoint
        response = self.client.put(
            "/teams",
            json={
                "name": "TestTeam",
                "description": "Test Team",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch("db.crud.getOneRecordByColumnName")
    @patch("db.crud.delete")
    def test_delete_team(self, mock_get, mock_delete):
        # mock the getOneRecordByColumnName method to return a Team
        mock_get.return_value = {
            "name": "TestTeam",
            "description": "Test Team",
        }

        # mock the delete method to do nothing
        mock_delete.return_value = None

        # call the API endpoint
        response = self.client.delete(
            "/teams?team_name=TestTeam",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class Test_Team_Valdiators(TestCase):
    """
    The following tests are for the Team Validator
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
            response.json()["detail"][0]["msg"],
            "Value error, Name cannot be empty",
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
