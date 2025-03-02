from os import environ as env
from ddt import ddt, data, unpack
from unittest.mock import patch
from fastapi.testclient import TestClient
from main import app
from unittest import TestCase
from fastapi import HTTPException, status
import jwt

import unittest

SECRET_KEY = env["SECRET_KEY"]
ALGORITHM = env["ALGORITHM"]

globalTestToken = jwt.encode({"sub": "test_email", "id": 1}, SECRET_KEY, algorithm=ALGORITHM)

headers = {"Authorization": f"Bearer {globalTestToken}"}

class Test_Api_Get_User(TestCase):
    """
    The following tests are for the Get User API endpoints
    """

    @classmethod
    def setUpClass(cls):
        """Setup the test environment once before all tests"""
        cls.client = TestClient(app)
        pass

    # Get all users route tests
    @patch("db.crud.getAllRecords")
    def test_get_all_users_successful(self, mock_return):
        token = jwt.encode({"id": 1, "sub": "test_email", "role_name": "SuperAdmin", "team_name": "test_team"}, SECRET_KEY, algorithm=ALGORITHM)
        headers = {"Authorization": f"Bearer {token}"}
        # Mock the return value of the getAllRecords function
        mock_return.return_value = [
            {
                "id": 1,
                "email": "test_email",
                "password": "test_password",
                "full_name": "full_name",
                "team_name": "test_team",
                "role_name": "User",
                "number_of_allocated_holdiays": 25,
                "number_of_remaining_holidays": 25
            },
            {
                "id": 2,
                "email": "test_email2",
                "password": "test_password2",
                "full_name": "full_name2",
                "team_name": "test_team2",
                "role_name": "User",
                "number_of_allocated_holdiays": 25,
                "number_of_remaining_holidays": 25
            },
        ]

        # call the API endpoint
        response = self.client.get("/users", headers=headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 2)
        self.assertEqual(response.json()[0]["id"], 1)
        self.assertEqual(response.json()[0]["email"], "test_email")

    @patch("db.crud.getAllRecords")
    def test_get_all_users_where_no_users_exist(self, mock_return):
        token = jwt.encode({"id": 1, "sub": "test_email", "role_name": "SuperAdmin", "team_name": "test_team"}, SECRET_KEY, algorithm=ALGORITHM)
        headers = {"Authorization": f"Bearer {token}"}
        # Mock the return value of the getAllRecords function to return HTTPException 404
        mock_return.side_effect = HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No records found"
        )
        
        # call the API endpoint
        response = self.client.get(
            "/users",
            headers = headers
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # Get user by id route tests
    @patch("db.crud.getOneRecordByColumnName")
    def test_get_user_by_id_successful(self, mock_return):
        # Mock the return value of the getOneRecordByColumnName function
        mock_return.return_value = {
            "id": 1,
            "email": "test_email",
            "password": "test_password",
            "full_name": "full_name",
            "team_name": "test_team",
            "role_name": "User",
            "number_of_allocated_holdiays": 25,
            "number_of_remaining_holidays": 25            
        }

        # call the API endpoint
        response = self.client.get(
            "/users?user_id=1",
            headers = headers
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
            headers = headers            
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # Get all users by team name route tests
    @patch("db.crud.getAllRecordsByColumnName")
    def test_get_all_users_by_team_name_successful(self, mock_return):
        token = jwt.encode({"id": 1, "sub": "test_email", "role_name": "Admin", "team_name": "test_team"}, SECRET_KEY, algorithm=ALGORITHM)
        headers = {"Authorization": f"Bearer {token}"}
        # Mock the return value of the getAllRecordsByColumnName function
        mock_return.return_value = [
            {
                "id": 1,
                "email": "test_email",
                "password": "test_password",
                "full_name": "full_name",
                "team_name": "test_team",
                "role_name": "User",
                "number_of_allocated_holdiays": 25,
                "number_of_remaining_holidays": 25
            },
            {
                "id": 2,
                "email": "test_email2",
                "password": "test_password2",
                "full_name": "full_name2",
                "team_name": "test_team",
                "role_name": "User",
                "number_of_allocated_holdiays": 25,
                "number_of_remaining_holidays": 25
            },
        ]

        response = self.client.get("/users",headers = headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 2)
        self.assertEqual(response.json()[0]["id"], 1)
        self.assertEqual(response.json()[0]["email"], "test_email")

    @patch("db.crud.getAllRecordsByColumnName")
    def test_get_all_users_by_team_name_where_no_users_exist(self, mock_return):
        token = jwt.encode({"id": 1, "sub": "test_email", "role_name": "Admin", "team_name": "test_team"}, SECRET_KEY, algorithm=ALGORITHM)
        headers = {"Authorization": f"Bearer {token}"}
        # Mock the return value of the getAllRecordsByColumnName function to return HTTPException 404
        mock_return.side_effect = HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No records found"
        )

        response = self.client.get("/users", headers = headers)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class Test_Api_Create_User(TestCase):
    """
    The following tests are for the Create User API endpoints
    """

    @classmethod
    def setUpClass(cls):
        """Setup the test environment once before all tests"""
        cls.client = TestClient(app)
        pass

    @patch("db.crud.create")
    def test_create_user_successful(self, mock_create):
        # Mock the return value of the create function
        mock_create.return_value = None
        
        token = jwt.encode({"sub": "test_email", "id": 1, "role_name":"SuperAdmin"}, SECRET_KEY, algorithm=ALGORITHM)
        header = {"Authorization": f"Bearer {token}"}

        response = self.client.post(
            "/users",
            json={
                "id": None,
                "email": "test_email",
                "password": "test_password",
                "full_name": "full_name",
                "team_name": "test_team",
                "role_name": "User",
                "allocated_holidays": 25,
                "remaining_holidays": 25
            },
            headers = header
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @patch("db.crud.create")
    def test_create_user_with_admin_role_UnAuthorized(self, mock_create):
        # Mock the return value of the create function
        mock_create.return_value = None

        token = jwt.encode({"sub": "test_email", "id": 1, "role_name":"Admin"}, SECRET_KEY, algorithm=ALGORITHM)
        header = {"Authorization": f"Bearer {token}"}

        response = self.client.post(
            "/users",
            json={
                "id": None,
                "email": "test_email",
                "password": "test_password",
                "full_name": "full_name",
                "team_name": "test_team",
                "role_name": "Admin",
                "allocated_holidays": 25,
                "remaining_holidays": 25                
            },
            headers = header
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    @patch("db.crud.create")
    def test_create_user_with_super_admin_role_Unauthorized(self, mock_create):
        # Mock the return value of the create function
        mock_create.return_value = None

        token = jwt.encode({"sub": "test_email", "id": 1, "role_name":"SuperAdmin"}, SECRET_KEY, algorithm=ALGORITHM)
        header = {"Authorization": f"Bearer {token}"}

        response = self.client.post(
            "/users",
            json={
                "id": None,
                "email": "test_email",
                "password": "test_password",
                "full_name": "full_name",
                "team_name": "test_team",
                "role_name": "SuperAdmin",
                "allocated_holidays": 25,
                "remaining_holidays": 25
            },
            headers = header
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class Test_Api_Update_User(TestCase):
    """
    The following tests are for the Update User API endpoints
    """

    @classmethod
    def setUpClass(cls):
        """Setup the test environment once before all tests"""
        cls.client = TestClient(app)
        pass

    @patch("db.crud.update")
    @patch("db.crud.getOneRecordByColumnName")
    def test_update_user_successful(self, mock_get, mock_update):
        token = jwt.encode({"sub": "test_email", "id": 1, "role_name":"SuperAdmin"}, SECRET_KEY, algorithm=ALGORITHM)
        header = {"Authorization": f"Bearer {token}"}
        # Mock the return value of the getOneRecordByColumnName function
        mock_get.return_value = {
            "id": 1,
            "email": "test_email",
            "password": "test_password",
            "full_name": "full_name",
            "team_name": "test_team",
            "role_name": "User",
            "number_of_allocated_holdiays": 25,
            "number_of_remaining_holdiays": 25
        }

        # Mock the return value of the update function
        mock_update.return_value = None

        response = self.client.put(
            "/users",
            json={
                "id": 1,
                "email": "test_email",
                "password": "test_password",
                "full_name": "full_name2",
                "team_name": "test_team",
                "role_name": "User",
                "allocated_holidays": 25,
                "remaining_holidays": 25
            },
            headers = header
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch("db.crud.update")
    @patch("db.crud.getOneRecordByColumnName")
    def test_update_user_where_role_is_changed_to_admin_successful(
        self, mock_get, mock_update
    ):
        token = jwt.encode({"sub": "test_email", "id": 1, "role_name":"SuperAdmin"}, SECRET_KEY, algorithm=ALGORITHM)
        header = {"Authorization": f"Bearer {token}"}
        # Mock the return value of the getOneRecordByColumnName function
        mock_get.return_value = {
            "id": 1,
            "email": "test_email",
            "password": "test_password",
            "full_name": "full_name",
            "team_name": "test_team",
            "role_name": "User",
            "number_of_allocated_holdiays": 25,
            "number_of_remaining_holdiays": 25
        }

        # Mock the return value of the update function
        mock_update.return_value = None

        response = self.client.put(
            "/users",
            json={
                "id": 1,
                "email": "test_email2",
                "password": "test_password2",
                "full_name": "full_name2",
                "team_name": "test_team",
                "role_name": "Admin",
                "allocated_holidays": 25,
                "remaining_holidays": 25
            },
            headers = header
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch("db.crud.update")
    @patch("db.crud.getOneRecordByColumnName")
    def test_update_user_where_role_is_changed_to_super_admin_unsuccessful(
        self, mock_get, mock_update
    ):
        # Mock the return value of the getOneRecordByColumnName function
        mock_get.return_value = {
            "id": 1,
            "email": "test_email",
            "password": "test_password",
            "full_name": "full_name",
            "team_name": "test_team",
            "role_name": "User"
        }

        # Mock the return value of the update function
        mock_update.return_value = None

        response = self.client.put(
            "/users",
            json={
                "id": 1,
                "email": "test_email2",
                "password": "test_password2",
                "full_name": "full_name2",
                "team_name": "test_team",
                "role_name": "SuperAdmin",
                "allocated_holidays": 25,
                "remaining_holidays": 25
            },
            headers = headers
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.json()["detail"], "You cannot assign this role to a user"
        )

    @patch("db.crud.update")
    @patch("db.crud.getOneRecordByColumnName")
    def test_update_user_where_user_is_super_admin_and_role_not_changed(self, mock_get, mock_update):
        token = jwt.encode({"sub": "test_email", "id": 1, "role_name":"SuperAdmin"}, SECRET_KEY, algorithm=ALGORITHM)
        header = {"Authorization": f"Bearer {token}"}
        
        # Mock the return value of the getOneRecordByColumnName function
        mock_get.return_value = {
            "id": 1,
            "email": "test_email",
            "password": "test_password",
            "full_name": "full_name",
            "team_name": "test_team",
            "role_name": "SuperAdmin"
        }

        # Mock the return value of the update function
        mock_update.return_value = None

        response = self.client.put(
            "/users",
            json={
                "id": 1,
                "email": "test_email2",
                "password": "test_password2",
                "full_name": "full_name2",
                "team_name": "test_team",
                "role_name": "Admin",
                "allocated_holidays": 25,
                "remaining_holidays": 25
            },
            headers = header
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch("db.crud.update")
    @patch("db.crud.getOneRecordByColumnName")
    def test_update_user_where_user_is_super_admin_and_role_is_changed_unsuccessful(
        self, mock_get, mock_update
    ):
        # Mock the return value of the getOneRecordByColumnName function
        mock_get.return_value = {
            "id": 1,
            "email": "test_email",
            "password": "test_password",
            "full_name": "full_name",
            "team_name": "test_team",
            "role_name": "SuperAdmin"
        }

        # Mock the return value of the update function
        mock_update.return_value = None

        response = self.client.put(
            "/users",
            json={
                "id": 1,
                "email": "test_email2",
                "password": "test_password2",
                "full_name": "full_name2",
                "team_name": "test_team",
                "role_name": "User",
                "allocated_holidays": 25,
                "remaining_holidays": 25
            },
            headers = headers
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.json()["detail"], "You cannot change the role of this user"
        )

class Test_Api_Update_User_Password(TestCase):
    """
    The following tests are for the Update User API endpoints
    """

    @classmethod
    def setUpClass(cls):
        """Setup the test environment once before all tests"""
        cls.client = TestClient(app)
        pass

    @patch("db.crud.updatePassword")
    @patch("db.crud.getOneRecordByColumnName")
    def test_update_user_password_as_user_successful(self, mock_get, mock_update):
        token = jwt.encode({"sub": "test_email", "id": 1, "role_name":"User"}, SECRET_KEY, algorithm=ALGORITHM)
        header = {"Authorization": f"Bearer {token}"}
        
        # Mock the return value of the getOneRecordByColumnName function
        mock_get.return_value = {
            "id": 1,
            "email": "test_email",
            "password": "test_password",
            "full_name": "full_name",
            "team_name": "test_team",
            "role_name": "User"
        }

        # Mock the return value of the update function
        mock_update.return_value = None

        response = self.client.patch(
            "/users/password?user_id=1&password=test_password123",
            headers = header
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch("db.crud.updatePassword")
    @patch("db.crud.getOneRecordByColumnName")
    def test_update_another_users_password_as_a_different_user_successful(self, mock_get, mock_update):
        token = jwt.encode({"sub": "test_email", "id": 1, "role_name":"User"}, SECRET_KEY, algorithm=ALGORITHM)
        header = {"Authorization": f"Bearer {token}"}
        
        # Mock the return value of the getOneRecordByColumnName function
        mock_get.return_value = {
            "id": 2,
            "email": "test_email",
            "password": "test_password",
            "full_name": "full_name",
            "team_name": "test_team",
            "role_name": "User",
        }

        # Mock the return value of the update function
        mock_update.return_value = None

        response = self.client.patch(
            "/users/password?user_id=2&password=test_password123",
            headers = header
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class Test_Api_Delete_User(TestCase):
    """
    The following tests are for the Delete User API endpoints
    """

    @classmethod
    def setUpClass(cls):
        """Setup the test environment once before all tests"""
        cls.client = TestClient(app)
        pass

    @patch("db.crud.delete")
    @patch("db.crud.getOneRecordByColumnName")
    def test_delete_user_where_user_is_standard_logged_in_as_user_unauthorised(self, mock_get, mock_delete):
        token = jwt.encode({"sub": "test_email", "id": 1, "role_name":"User"}, SECRET_KEY, algorithm=ALGORITHM)
        header = {"Authorization": f"Bearer {token}"}

        # Mock the return value of the getOneRecordByColumnName function of user to delete
        mock_get.return_value = {
            "id": 1,
            "email": "test_email",
            "password": "test_password",
            "full_name": "full_name",
            "team_name": "test_team",
            "role_name": "User",
        }

        # Mock the return value of the delete function
        mock_delete.return_value = None

        response = self.client.delete(
            "/users?user_id=2",
            headers = header
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @patch("db.crud.delete")
    @patch("db.crud.getOneRecordByColumnName")
    def test_delete_user_where_user_is_admin_logged_in_as_admin_unauthorised(self, mock_get, mock_delete):
        token = jwt.encode({"sub": "test_email", "id": 1, "role_name":"Admin"}, SECRET_KEY, algorithm=ALGORITHM)
        header = {"Authorization": f"Bearer {token}"}
        # Mock the return value of the getOneRecordByColumnName function of user to delete
        mock_get.return_value = {
            "id": 1,
            "email": "test_email",
            "password": "test_password",
            "full_name": "full_name",
            "team_name": "test_team",
            "role_name": "Admin",
        }

        # Mock the return value of the delete function
        mock_delete.return_value = None

        response = self.client.delete(
            "/users?user_id=2",
            headers = header
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @patch("db.crud.delete")
    @patch("db.crud.getOneRecordByColumnName")
    def test_delete_user_where_user_is_admin_logged_in_as_superadmin_unauthorised(self, mock_get, mock_delete):
        token = jwt.encode({"sub": "test_email", "id": 1, "role_name":"SuperAdmin"}, SECRET_KEY, algorithm=ALGORITHM)
        header = {"Authorization": f"Bearer {token}"}
        # Mock the return value of the getOneRecordByColumnName function of user to delete
        mock_get.return_value = {
            "id": 2,
            "email": "test_email2",
            "password": "test_password",
            "full_name": "full_name",
            "team_name": "test_team",
            "role_name": "Admin",
        }

        # Mock the return value of the delete function
        mock_delete.return_value = None

        response = self.client.delete(
            "/users?user_id=2",
            headers = header
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch("db.crud.delete")
    @patch("db.crud.getOneRecordByColumnName")
    def test_delete_user_where_user_is_super_admin_unsuccessful(self, mock_get, mock_delete):
        token = jwt.encode({"sub": "test_email", "id": 1, "role_name":"SuperAdmin"}, SECRET_KEY, algorithm=ALGORITHM)
        header = {"Authorization": f"Bearer {token}"}
        
        # Mock the return value of the getOneRecordByColumnName function of user to delete
        mock_get.return_value = {
            "id": 2,
            "email": "test_email2",
            "password": "test_password",
            "full_name": "full_name",
            "team_name": "test_team",
            "role_name": "SuperAdmin",
        }

        # Mock the return value of the delete function
        mock_delete.return_value = None

        response = self.client.delete(
            "/users?user_id=2",
            headers = header
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json()["detail"], "You cannot delete this user")

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
        ("role_name", "User"),
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
            headers = headers
        )
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        self.assertEqual(
            response.json()["detail"][0]["msg"],
            f"Value error, {field_name} cannot be empty",
        )

    @data(
        ("email", "test_email"),
        ("full_name", "test_name"),
        ("team_name", "test_team"),
        ("role_name", "User"),
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
                "full_name": field_value if field_name != "full_name" else "",
                "team_name": field_value if field_name != "team_name" else "",
                "role_name": field_value if field_name != "role_name" else "",
            },
            headers = headers
        )
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        self.assertEqual(
            response.json()["detail"][0]["msg"],
            f"Value error, {field_name} cannot be empty",
        )


if __name__ == "__main__":
    unittest.main()
