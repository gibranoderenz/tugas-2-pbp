from django.test import TestCase, Client


class MyWatchListTestCase(TestCase):
    def test_html_route_is_working(self):
        res = Client().get('/mywatchlist/html/')
        self.assertEqual(res.status_code, 200)

    def test_json_route_is_working(self):
        res = Client().get('/mywatchlist/json/')
        self.assertEqual(res.status_code, 200)

    def test_xml_route_is_working(self):
        res = Client().get('/mywatchlist/xml/')
        self.assertEqual(res.status_code, 200)

    def test_mywatchlist_html_using_mywatchlist_template(self):
        res = Client().get('/mywatchlist/html/')
        self.assertTemplateUsed(res, 'mywatchlist.html')
