from django.test import TestCase
from django.urls import reverse


class WebsitePagesTests(TestCase):

    def test_home_page_loads(self):
        response = self.client.get(reverse('website:home'))
        self.assertEqual(response.status_code, 200)

    def test_services_page_loads(self):
        response = self.client.get(reverse('website:services'))
        self.assertEqual(response.status_code, 200)

    def test_solutions_page_loads(self):
        response = self.client.get(reverse('website:solutions'))
        self.assertEqual(response.status_code, 200)

    def test_projects_page_loads(self):
        response = self.client.get(reverse('website:projects'))
        self.assertEqual(response.status_code, 200)

    def test_about_page_loads(self):
        response = self.client.get(reverse('website:about'))
        self.assertEqual(response.status_code, 200)

    def test_contact_page_loads(self):
        response = self.client.get(reverse('website:contact'))
        self.assertEqual(response.status_code, 200)

    def test_quote_page_loads(self):
        response = self.client.get(reverse('website:quote'))
        self.assertEqual(response.status_code, 200)

    def test_contact_form_renders(self):
        response = self.client.get(reverse('website:contact'))
        self.assertContains(response, '<form')
        self.assertContains(response, 'name="message"')

    def test_quote_form_renders(self):
        response = self.client.get(reverse('website:quote'))
        self.assertContains(response, '<form')
        self.assertContains(response, 'name="service"')

    def test_contact_form_valid_submission(self):
        response = self.client.post(reverse('website:contact'), {
            'name': 'Jane Doe',
            'email': 'jane@example.com',
            'company': '',
            'subject': 'Test enquiry',
            'message': 'This is a test message.',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'received')

    def test_quote_form_valid_submission(self):
        response = self.client.post(reverse('website:quote'), {
            'name': 'Jane Doe',
            'email': 'jane@example.com',
            'company': '',
            'service': 'web_development',
            'project_description': 'A test project description.',
            'budget': '',
            'timeline': '',
            'additional_info': '',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'received')

    def test_contact_form_missing_required_field_shows_error(self):
        response = self.client.post(reverse('website:contact'), {
            'name': '',
            'email': '',
            'subject': '',
            'message': '',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'form-error')