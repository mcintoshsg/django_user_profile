from django.test import TestCase

from profiler.views import home

class HomePageTest(TestCase):
    ''' test of URL and html for home page '''
    def test_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

   