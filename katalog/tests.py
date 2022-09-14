from django.test import TestCase, Client


class GetCatalogItemsTestCase(TestCase):
    def test_katalog_route_is_working(self):
        res = Client().get('/katalog/')
        self.assertEqual(res.status_code, 200)

    def test_katalog_using_katalog_template(self):
        res = Client().get('/katalog/')
        self.assertTemplateUsed(res, 'katalog.html')
