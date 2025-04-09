from time import sleep

from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework import status

from core.test_base.test_models import TestPropertiesModelsBase, TestPostsModelBase
from core.test_base.test_admin import TestAdminBase


class TestApiViewsMethods(APITestCase, TestAdminBase):
    """Base class for testing api views that only allows get views"""

    def setUp(
        self,
        endpoint="/api/",
        restricted_get: bool = True,
        restricted_post: bool = True,
        restricted_put: bool = True,
        restricted_delete: bool = True,
    ):
        """Initialize test data

        restricted_get (bool): If the get method is restricted
        restricted_post (bool): If the post method is restricted
        restricted_put (bool): If the put method is restricted
        restricted_delete (bool): If the delete method is restricted
        """

        # Create user and login
        user = User.objects.create_superuser(
            username="admin",
            email="test@gmail.com",
            password="test pass",
        )
        self.token = str(AccessToken.for_user(user))
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")

        # Save data
        self.endpoint = endpoint
        self.restricted_get = restricted_get
        self.restricted_post = restricted_post
        self.restricted_put = restricted_put
        self.restricted_delete = restricted_delete

    def validate_invalid_method(self, method: str):
        """Validate that the given method is not allowed on the endpoint"""

        response = getattr(self.client, method)(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_authenticated_user_post(self):
        """Test that authenticated users can not post to the endpoint"""

        if self.restricted_post:
            self.validate_invalid_method("post")

    def test_authenticated_user_put(self):
        """Test that authenticated users can not put to the endpoint"""

        if self.restricted_put:
            self.validate_invalid_method("put")

    def test_authenticated_user_patch(self):
        """Test that authenticated users can not patch to the endpoint"""

        if self.restricted_put:
            self.validate_invalid_method("patch")

    def test_unauthenticated_user_get(self):
        """Test unauthenticated user get request"""

        # Remove authentication
        self.client.logout()

        # Make request
        response = self.client.get(self.endpoint)

        # Check response
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TestPropertiesViewsBase(TestApiViewsMethods, TestPropertiesModelsBase):
    """Base class for testing views"""

    def setUp(self, endpoint="/api/"):
        """Initialize test data"""

        # Create initial data
        self.location = self.create_location()
        self.category = self.create_category()
        self.seller = self.create_seller()
        self.company = self.create_company()
        self.tag1 = self.create_tag(
            name="Test tag 1", es="Etiqueta de prueba 1", en="Test tag 1"
        )
        self.tag2 = self.create_tag(
            name="Test tag 2", es="Etiqueta de prueba 2", en="Test tag 2"
        )
        self.property_1 = self.create_property(
            name="Test property 1",
            company=self.company,
            location=self.location,
            category=self.category,
            seller=self.seller,
        )
        self.property_1.tags.add(self.tag1, self.tag2)
        self.property_1.save()
        sleep(0.1)
        self.property_2 = self.create_property(
            name="Test property 2",
            company=self.company,
            location=self.location,
            category=self.category,
            seller=self.seller,
        )

        # Update restricted methods
        self.restricted_get = False

        # Global data
        self.langs = ["es", "en"]

        # Send enpoint to parent
        super().setUp()
        self.endpoint = endpoint


class TestPostsViewsBase(TestApiViewsMethods, TestPostsModelBase):
    
    def setUp(self, endpoint="/api/"):
        """Initialize test data"""

        # Create initial data
        self.post_1 = self.create_post(
            title="Test post 1",
            lang="es",
        )
        sleep(0.1)
        self.post_2 = self.create_post(
            title="Test post 2",
            lang="en",
        )

        # Update restricted methods
        self.restricted_get = False

        # Send enpoint to parent
        super().setUp()
        self.endpoint = endpoint