from django.contrib.auth import get_user_model
from django.test import TestCase

User = get_user_model()


class UserModelTests(TestCase):

    def test_create_user_with_email(self):
        user = User.objects.create_user(
            email='client@example.com',
            password='testpass123',
            first_name='Jane',
            last_name='Doe',
        )
        self.assertEqual(user.email, 'client@example.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_email_is_normalised(self):
        user = User.objects.create_user(
            email='client@EXAMPLE.COM',
            password='testpass123',
            first_name='Jane',
            last_name='Doe',
        )
        self.assertEqual(user.email, 'client@example.com')

    def test_password_is_hashed(self):
        user = User.objects.create_user(
            email='client@example.com',
            password='testpass123',
            first_name='Jane',
            last_name='Doe',
        )
        self.assertNotEqual(user.password, 'testpass123')
        self.assertTrue(user.password.startswith('pbkdf2_'))

    def test_authentication_with_correct_password(self):
        user = User.objects.create_user(
            email='client@example.com',
            password='testpass123',
            first_name='Jane',
            last_name='Doe',
        )
        self.assertTrue(user.check_password('testpass123'))

    def test_authentication_with_incorrect_password_fails(self):
        user = User.objects.create_user(
            email='client@example.com',
            password='testpass123',
            first_name='Jane',
            last_name='Doe',
        )
        self.assertFalse(user.check_password('wrongpassword'))

    def test_email_uniqueness_enforced(self):
        User.objects.create_user(
            email='client@example.com',
            password='testpass123',
            first_name='Jane',
            last_name='Doe',
        )
        with self.assertRaises(Exception):
            User.objects.create_user(
                email='client@example.com',
                password='anotherpass',
                first_name='John',
                last_name='Smith',
            )

    def test_create_superuser(self):
        admin = User.objects.create_superuser(
            email='admin@example.com',
            password='adminpass123',
            first_name='Admin',
            last_name='User',
        )
        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)
        self.assertEqual(admin.role, User.Role.STAFF)

    def test_username_field_is_email(self):
        self.assertEqual(User.USERNAME_FIELD, 'email')

    def test_default_role_is_client(self):
        user = User.objects.create_user(
            email='client@example.com',
            password='testpass123',
            first_name='Jane',
            last_name='Doe',
        )
        self.assertEqual(user.role, User.Role.CLIENT)

    def test_role_can_be_set_to_staff(self):
        user = User.objects.create_user(
            email='staff@example.com',
            password='testpass123',
            first_name='Staff',
            last_name='Member',
            role=User.Role.STAFF,
        )
        self.assertEqual(user.role, User.Role.STAFF)

    def test_custom_user_model_is_active(self):
        from django.conf import settings
        self.assertEqual(settings.AUTH_USER_MODEL, 'accounts.User')