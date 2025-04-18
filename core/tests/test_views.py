from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import AccessToken


class CustomJWTViewTests(APITestCase):
    
    @classmethod
    def setUpTestData(cls):
        # Create a test user
        cls.username = "testuser"
        cls.password = "testpassword"
        cls.user = User.objects.create_user(
            username="testuser",
            password="testpassword"
        )
        
        # Setup endpoints
        cls.token_obtain_url = "/api/token/"
        cls.token_refresh_url = "/api/token/refresh/"
        cls.token_validate_url = "/api/token/validate/"

    def test_token_obtain_pair(self):
        """
        Test that a token pair can be obtained with valid credentials
        and that the custom response structure is returned.
        """
        response = self.client.post(self.token_obtain_url, {
            "username": self.username,
            "password": self.password
        })

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("status", response.data)
        self.assertIn("message", response.data)
        self.assertIn("data", response.data)
        self.assertEqual(response.data["status"], "ok")
        self.assertEqual(response.data["message"], "generated")
        self.assertIn("access", response.data["data"])
        self.assertIn("refresh", response.data["data"])

    def test_token_obtain_pair_invalid_credentials(self):
        """
        Test that the API returns a 401 error for invalid credentials.
        """
        response = self.client.post(self.token_obtain_url, {
            "username": "wronguser",
            "password": "wrongpassword"
        })

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data["status"], "error")
        self.assertEqual(
            response.data["message"],
            "La combinación de credenciales no tiene una cuenta activa"
        )
        self.assertNotIn("access", response.data["data"])
        self.assertNotIn("refresh", response.data["data"])

    def test_token_refresh(self):
        """
        Test that an access token can be refreshed using a valid refresh token
        and that the custom response structure is returned.
        """
        # Obtain token pair
        token_response = self.client.post(self.token_obtain_url, {
            "username": self.username,
            "password": self.password
        })
        refresh_token = token_response.data["data"]["refresh"]

        # Refresh the token
        response = self.client.post(self.token_refresh_url, {
            "refresh": refresh_token
        })

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("status", response.data)
        self.assertIn("message", response.data)
        self.assertIn("data", response.data)
        self.assertEqual(response.data["status"], "ok")
        self.assertEqual(response.data["message"], "generated")
        self.assertIn("access", response.data["data"])

    def test_token_refresh_invalid_token(self):
        """
        Test that the API returns a 401 error for an invalid refresh token.
        """
        response = self.client.post(self.token_refresh_url, {
            "refresh": "invalid_refresh_token"
        })

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data["status"], "error")
        self.assertEqual(response.data["message"], "El token es inválido o ha expirado")
        self.assertNotIn("access", response.data["data"])
        self.assertNotIn("refresh", response.data["data"])
        
    def test_validate_refresh_valid(self):
        """ Test that the validate refresh endpoint returns a
        200 OK response with a valid token. """
        
        # Get token
        token = str(AccessToken.for_user(self.user))
        
        # Obtain token pair
        response = self.client.get(
            self.token_validate_url,
            HTTP_AUTHORIZATION=f"Bearer {token}"
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("status", response.data)
        self.assertIn("message", response.data)
        self.assertIn("data", response.data)
        self.assertEqual(response.data["status"], "ok")
        self.assertEqual(response.data["message"], "Token is valid")
        self.assertEqual(response.data["data"], {})
        
    def test_validate_refresh_invalid(self):
        """ Test that the validate refresh endpoint returns a
        401 error response with a invalid token. """
        
        # Get token
        token = "faketoken123"
        
        # Obtain token pair
        response = self.client.get(
            self.token_validate_url,
            HTTP_AUTHORIZATION=f"Bearer {token}"
        )
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("status", response.data)
        self.assertIn("message", response.data)
        self.assertIn("data", response.data)
        self.assertEqual(response.data["status"], "error")
        self.assertEqual(
            response.data["message"],
            "El token dado no es valido para ningun tipo de token"
        )
        self.assertEqual(response.data["data"]["code"], "token_not_valid")