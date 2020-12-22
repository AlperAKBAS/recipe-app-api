from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):

    def test_create_user_with_email_address(self):
        """Test creating a new user with the email address, checks password and email"""
        email = 'test@testdomain.com'
        password = 'Testing321..'
        user = get_user_model().objects.create_user(
            email = email,
            password = password
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
        
    
    def test_new_user_email_address_normalized(self):
        """Test if the new user email address is normalized"""
        email = 'test@TESTDOMAIN.COM'
        user = get_user_model().objects.create_user(email=email, password = 'Testing321..')

        self.assertEqual(user.email, email.lower())


    def test_new_user_invalid_email(self):
        """Test creating user with no email raises error"""

        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'Testing321..')


    def test_create_super_user(self):
        """Test create a super user. When create_superuser is called, Is it correct: is_staff=True & is_superuser=True"""
        user = get_user_model().objects.create_superuser(
            'test@testdomain.com',
            'Testing321..'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)