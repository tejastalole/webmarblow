from django.test import TestCase
from django.urls import reverse

from website.models import ContactInquiry, QuoteRequest, Service


class SitePagesTests(TestCase):
    def test_public_pages_render(self):
        names = ['home', 'services', 'portfolio', 'about', 'contact', 'quote']
        for name in names:
            response = self.client.get(reverse(f'website:{name}'))
            self.assertEqual(response.status_code, 200)

    def test_contact_form_creates_inquiry(self):
        response = self.client.post(reverse('website:contact'), {
            'name': 'Asha Patel',
            'email': 'asha@example.com',
            'phone': '9876543210',
            'subject': 'New website',
            'message': 'We need a site for our studio.',
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(ContactInquiry.objects.count(), 1)

    def test_quote_form_creates_request(self):
        service = Service.objects.create(
            title='Custom Website Design',
            slug='custom-website-design',
            icon='monitor',
            short_description='Design',
            description='Design work',
            features='Brand system',
        )
        response = self.client.post(reverse('website:quote'), {
            'name': 'Rohit Mehta',
            'email': 'rohit@example.com',
            'phone': '9876543210',
            'company': 'Mehta Goods',
            'service': service.pk,
            'budget': 'growth',
            'timeline': '1month',
            'project_details': 'Five-page brochure site with enquiry form.',
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(QuoteRequest.objects.count(), 1)
