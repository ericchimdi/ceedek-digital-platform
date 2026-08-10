from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Quote

User = get_user_model()


class QuoteSubmissionTests(TestCase):

    def valid_quote_data(self):
        return {
            'name': 'Jane Doe',
            'email': 'jane@example.com',
            'company': '',
            'service': Quote.Service.WEB_DEVELOPMENT,
            'project_description': 'I need a new company website.',
            'budget': '',
            'timeline': '',
            'additional_info': '',
        }

    def test_anonymous_can_submit_valid_quote(self):
        response = self.client.post(reverse('website:quote'), self.valid_quote_data())
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('website:quote_success'))

        self.assertEqual(Quote.objects.count(), 1)
        quote = Quote.objects.first()
        self.assertIsNone(quote.user)
        self.assertEqual(quote.name, 'Jane Doe')

    def test_authenticated_user_quote_is_linked(self):
        user = User.objects.create_user(
            email='client@example.com',
            password='testpass123',
            first_name='Client',
            last_name='User',
        )
        self.client.force_login(user)

        response = self.client.post(reverse('website:quote'), self.valid_quote_data())
        self.assertEqual(response.status_code, 302)

        quote = Quote.objects.first()
        self.assertEqual(quote.user, user)

    def test_invalid_submission_does_not_create_quote(self):
        data = self.valid_quote_data()
        data['email'] = 'not-a-valid-email'

        response = self.client.post(reverse('website:quote'), data)
        self.assertEqual(response.status_code, 200)  # re-renders form, no redirect
        self.assertEqual(Quote.objects.count(), 0)

    def test_missing_required_field_does_not_create_quote(self):
        data = self.valid_quote_data()
        data['project_description'] = ''

        response = self.client.post(reverse('website:quote'), data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Quote.objects.count(), 0)

    def test_new_quote_has_default_status(self):
        self.client.post(reverse('website:quote'), self.valid_quote_data())
        quote = Quote.objects.first()
        self.assertEqual(quote.status, Quote.Status.NEW)

    def test_cannot_spoof_another_users_id(self):
        real_user = User.objects.create_user(
            email='real@example.com', password='pass123',
            first_name='Real', last_name='User',
        )
        other_user = User.objects.create_user(
            email='other@example.com', password='pass123',
            first_name='Other', last_name='User',
        )
        self.client.force_login(real_user)

        data = self.valid_quote_data()
        data['user'] = other_user.pk  # attempt to spoof — 'user' is not a real form field

        response = self.client.post(reverse('website:quote'), data)
        self.assertEqual(response.status_code, 302)

        quote = Quote.objects.first()
        self.assertEqual(quote.user, real_user)
        self.assertNotEqual(quote.user, other_user)

    def test_success_page_loads(self):
        response = self.client.get(reverse('website:quote_success'))
        self.assertEqual(response.status_code, 200)

    def test_get_request_does_not_create_quote(self):
        self.client.get(reverse('website:quote'))
        self.assertEqual(Quote.objects.count(), 0)


class QuoteAdminTests(TestCase):

    def test_quote_str_representation(self):
        quote = Quote.objects.create(
            name='Jane Doe',
            email='jane@example.com',
            service=Quote.Service.AI_SOLUTIONS,
            project_description='Test',
        )
        self.assertIn('Jane Doe', str(quote))