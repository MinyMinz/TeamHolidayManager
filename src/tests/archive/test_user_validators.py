from ddt import ddt, data, unpack
from fastapi.testclient import TestClient
from main import app
from unittest import TestCase
from fastapi import status

import unittest


@ddt
class Test_Role_Valdiators(TestCase):
    """
    The following tests are for the Role Validators
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
    def test_user_validator_empty_fields(self, field_name, field_value):
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


if __name__ == "__main__":
    unittest.main()
