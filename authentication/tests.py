from django.test import TestCase
from django.contrib.auth import get_user_model

# Create your tests here.

class UserTests(TestCase):
    def test_create_user(self):
        user = User.objects.create(full_name='Test User', email='abc@xyz.com', password='123password@')
        self.assertIsInstance(user, User)
        self.assertEqual(user.email, 'abc@xyz.com')
        self.assertEqual(user.full_name, 'Test User')
        self.assertFalse(user.is_staff)
        self.assertTrue(user.is_active)
    
    def test_create_superuser(self):
        admin_user = User.objects.create_superuser(full_name='Test Admin' ,email='admin@xyz.com', password='123password@')
        self.assertEqual(admin_user.email, 'admin@xyz.com')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
    
    def test_raises_error_when_no_email_is_supplied(self):
        with self.assertRaisesMessage(ValueError, 'The given email must be set'):
            User.objects.create_user(email='', password="123password@")