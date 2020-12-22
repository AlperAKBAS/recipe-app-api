from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

# Cient Doc: https://docs.djangoproject.com/en/2.2/topics/testing/tools/#overview-and-a-quick-example

class AdminSiteTests(TestCase):
    
    def setUp(self):
        # before every test in our TestCase Class
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@testdomain.com',
            password =  'Testing321..'
        )
        self.client.force_login(self.admin_user)
        self.user =   get_user_model().objects.create_user(
            email = 'user@testdomain.com',
            password = 'Testing321..',
            name = 'Test User Full Name'
        )

    def test_users_listed(self):
        """Test that users are listed on users page"""

        url = reverse('admin:core_user_changelist')
        resp = self.client.get(url)
        # assertContains make some additional checks like status_code
        self.assertContains(resp, self.user.name)
        self.assertContains(resp, self.user.email)


    def test_user_change_page(self):
        """Test if user edit / change page workds correclty """
        url = reverse('admin:core_user_change', args=[self.user.id])
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)

    def test_create_user_page(self):
        """Test the add user page on admin """
        url = reverse('admin:core_user_add')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)