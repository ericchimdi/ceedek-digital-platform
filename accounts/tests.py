from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from organizations.models import Organization

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


class AuthenticationTests(TestCase):

    def valid_registration_data(self):
        return {
            'first_name': 'New',
            'last_name': 'Client',
            'email': 'newclient@example.com',
            'phone': '',
            'country': '',
            'password1': 'StrongPass123!',
            'password2': 'StrongPass123!',
        }

    # --- Registration ---

    def test_valid_registration_creates_user(self):
        response = self.client.post(reverse('accounts:register'), self.valid_registration_data())
        self.assertTrue(User.objects.filter(email='newclient@example.com').exists())
        self.assertRedirects(response, reverse('accounts:account'))

    def test_registered_user_has_client_role(self):
        self.client.post(reverse('accounts:register'), self.valid_registration_data())
        user = User.objects.get(email='newclient@example.com')
        self.assertEqual(user.role, User.Role.CLIENT)

    def test_registered_user_is_not_staff(self):
        self.client.post(reverse('accounts:register'), self.valid_registration_data())
        user = User.objects.get(email='newclient@example.com')
        self.assertFalse(user.is_staff)

    def test_registered_user_is_not_superuser(self):
        self.client.post(reverse('accounts:register'), self.valid_registration_data())
        user = User.objects.get(email='newclient@example.com')
        self.assertFalse(user.is_superuser)

    def test_registered_user_password_is_hashed(self):
        self.client.post(reverse('accounts:register'), self.valid_registration_data())
        user = User.objects.get(email='newclient@example.com')
        self.assertNotEqual(user.password, 'StrongPass123!')
        self.assertTrue(user.password.startswith('pbkdf2_'))

    def test_duplicate_email_rejected(self):
        User.objects.create_user(
            email='newclient@example.com', password='pass12345',
            first_name='Existing', last_name='User',
        )
        response = self.client.post(reverse('accounts:register'), self.valid_registration_data())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.filter(email='newclient@example.com').count(), 1)

    def test_invalid_email_rejected(self):
        data = self.valid_registration_data()
        data['email'] = 'not-an-email'
        response = self.client.post(reverse('accounts:register'), data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(first_name='New').exists())

    def test_weak_password_rejected(self):
        data = self.valid_registration_data()
        data['password1'] = '12345678'
        data['password2'] = '12345678'
        response = self.client.post(reverse('accounts:register'), data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(email='newclient@example.com').exists())

    def test_password_mismatch_rejected(self):
        data = self.valid_registration_data()
        data['password2'] = 'DifferentPass456!'
        response = self.client.post(reverse('accounts:register'), data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(email='newclient@example.com').exists())

    # --- Security: cannot escalate privileges via crafted POST data ---

    def test_cannot_assign_staff_role_via_post(self):
        data = self.valid_registration_data()
        data['role'] = 'STAFF'
        self.client.post(reverse('accounts:register'), data)
        user = User.objects.get(email='newclient@example.com')
        self.assertEqual(user.role, User.Role.CLIENT)

    def test_cannot_assign_is_staff_via_post(self):
        data = self.valid_registration_data()
        data['is_staff'] = 'True'
        self.client.post(reverse('accounts:register'), data)
        user = User.objects.get(email='newclient@example.com')
        self.assertFalse(user.is_staff)

    def test_cannot_assign_is_superuser_via_post(self):
        data = self.valid_registration_data()
        data['is_superuser'] = 'True'
        self.client.post(reverse('accounts:register'), data)
        user = User.objects.get(email='newclient@example.com')
        self.assertFalse(user.is_superuser)

    def test_cannot_assign_organization_via_post(self):
        org = Organization.objects.create(name='Some Company')
        data = self.valid_registration_data()
        data['organization'] = org.pk
        self.client.post(reverse('accounts:register'), data)
        user = User.objects.get(email='newclient@example.com')
        self.assertIsNone(user.organization)

    # --- Login ---

    def test_valid_login_succeeds(self):
        User.objects.create_user(
            email='client@example.com', password='testpass123',
            first_name='Jane', last_name='Doe',
        )
        response = self.client.post(reverse('accounts:login'), {
            'username': 'client@example.com', 'password': 'testpass123',
        })
        self.assertRedirects(response, reverse('accounts:account'))

    def test_login_with_wrong_password_fails(self):
        User.objects.create_user(
            email='client@example.com', password='testpass123',
            first_name='Jane', last_name='Doe',
        )
        response = self.client.post(reverse('accounts:login'), {
            'username': 'client@example.com', 'password': 'wrongpassword',
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_login_with_nonexistent_email_fails(self):
        response = self.client.post(reverse('accounts:login'), {
            'username': 'nobody@example.com', 'password': 'whatever123',
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_inactive_user_cannot_log_in(self):
        user = User.objects.create_user(
            email='inactive@example.com', password='testpass123',
            first_name='Inactive', last_name='User',
        )
        user.is_active = False
        user.save()
        response = self.client.post(reverse('accounts:login'), {
            'username': 'inactive@example.com', 'password': 'testpass123',
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    # --- Logout ---

    def test_logout_ends_session(self):
        user = User.objects.create_user(
            email='client@example.com', password='testpass123',
            first_name='Jane', last_name='Doe',
        )
        self.client.force_login(user)
        self.client.post(reverse('accounts:logout'))
        response = self.client.get(reverse('accounts:account'))
        self.assertNotEqual(response.status_code, 200)

    # --- Account page ---

    def test_authenticated_user_can_access_account_page(self):
        user = User.objects.create_user(
            email='client@example.com', password='testpass123',
            first_name='Jane', last_name='Doe',
        )
        self.client.force_login(user)
        response = self.client.get(reverse('accounts:account'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Jane')

    def test_anonymous_user_redirected_from_account_page(self):
        response = self.client.get(reverse('accounts:account'))
        self.assertNotEqual(response.status_code, 200)
        self.assertIn('/accounts/login/', response.url)

    def test_account_page_does_not_show_password(self):
        user = User.objects.create_user(
            email='client@example.com', password='testpass123',
            first_name='Jane', last_name='Doe',
        )
        self.client.force_login(user)
        response = self.client.get(reverse('accounts:account'))
        self.assertNotContains(response, user.password)