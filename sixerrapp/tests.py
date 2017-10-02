from django.test import TestCase
from django.conf import settings

# Test #0 - Index sanity test
class IndexViewSanityTestCase(TestCase):
    def test_browser_get_index_page_return_status_200(self):
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)
