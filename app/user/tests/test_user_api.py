from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')
URL_ME = reverse('user:me')

def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserAPITests(TestCase):
    """Tests the users API (public)"""

    def setUp(self):
        self.client = APIClient()

    def test_create_user_valid_success(self):
        """Test creating user with valid payload is sucessful"""
        payload = {
            'email': 'test@testdomain.com',
            'name': 'Testuser Test',
            'password': 'TestPassword'
        }

        resp = self.client.post(CREATE_USER_URL, payload)
    
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**resp.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', resp.data)

    def test_user_exists(self):
        """Test creating a duplicate user"""
        payload = {
            'email': 'test@testdomain.com',
            'password': 'TestPassword'
        }       
        create_user(**payload)
        resp = self.client.post(CREATE_USER_URL, **payload)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_password_too_short(self):
        """Test if password in less than 5 characters"""
        payload = {
            'email': 'test@testdomain.com',
            'name': 'TestUser Test',
            'password': 'Te'
        }       
        resp = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        ## Check if user created
        user_exists = get_user_model().objects.filter(
            email = payload['email']
        ).exists()
        self.assertFalse(user_exists)

    # zaten token isteği public bir request o yüzden bu sınıfın altında 
    def test_create_token_for_user(self):
        """tests that the token is created for the user"""
        payload = {
            'email': 'test@testdomain.com',
            'password': 'TestUser321..'
        }

        create_user(**payload)
        resp = self.client.post(TOKEN_URL, payload)
        self.assertIn('token', resp.data) #build in token function kullandığımuz için çalışacağını umuyoruz
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_create_token_with_invalid_credentials(self):
        """Test token is NOT created if invalid credentials are given"""
        create_user(email='test@testdomain.com', password='TestUser321..')
        resp = self.client.post(TOKEN_URL, {'email':'test@testdomain.com', 'password':'User321..'})

        self.assertNotIn('token', resp.data)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_if_no_user(self):
        """Test if no token created if user doesnt exist"""
        payload = {
            'email': 'notexistinguser@testdomain.com',
            'password': 'TestUser321..'
        }
        resp = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', resp.data)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_with_missing_field(self):
        """Test token email and password required"""
        resp = self.client.post(TOKEN_URL, {'email': 'one', 'password':''})
        self.assertNotIn('token', resp.data)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_user_unauthorized(self):
        """Test if authentication is required for user"""
        resp = self.client.get(URL_ME)
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserAPITests(TestCase):
    """Tests the users API that reuqires Authentication"""
    def setUp(self):
        self.user = create_user(
            email='testuser@demo.com',
            name='Test User',
            password='Testing321..'
            )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_succes(self):
        """Test retrieving profile for authenticated user"""
        resp = self.client.get(URL_ME)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(
            resp.data,
            {
                'name': self.user.name,
                'email': self.user.email,
            }
        )

    def test_post_me_not_allowed(self):
        """Test that POST request not allowed"""
        resp = self.client.post(URL_ME, {})
        self.assertEqual(resp.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile_update(self):
        """Test updating User Profile for Authenticated User"""
        payload = {
            'name': 'New Test User',
            'password': 'NewTesting321..'
        }
        resp = self.client.patch(URL_ME, payload)
        
        self.user.refresh_from_db()
        self.assertEqual(self.user.name, payload['name'])
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)