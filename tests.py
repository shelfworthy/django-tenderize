from django.conf import settings
from django.test import TestCase
from api import Client

from tenderize.helpers import tender_hash

class TestTenderClient(TestCase):
    def setUp(self):
        self.client = Client(user=settings.TENDER_EMAIL, password=settings.TENDER_PASSWORD)

    class TenderHashTestCase(TestCase):
        def testTenderHash(self):
            email = 'user@gmail.com'
            tender = 'help.yourapp.com'
            expires = 1228117891
            secret = 'monkey'
            self.assertEquals(tender_hash(email, expires, tender, secret), '1937bf7e8dc9f475cc9490933eb36e5f7807398a')

    def test_get_sites(self):
        result = self.client.get_sites()

        self.assertEquals(result['website'], 'http://tenderapp.com')
        self.assertEquals(result['permalink'], 'help')
        self.assertEquals(result['discussions_href'], 'http://api.tenderapp.com/help/discussions{-opt|/|state}{state}{-opt|?|page,user_email}{-join|&|page,user_email}')
        self.assertEquals(result['sections_href'], 'http://api.tenderapp.com/help/sections{-opt|?|page}{-join|&|page}')
        self.assertEquals(result['categories_href'], 'http://api.tenderapp.com/help/categories{-opt|?|page}{-join|&|page}')
        self.assertEquals(result['href'], 'http://api.tenderapp.com/help')
        self.assertEquals(result['profile_href'], 'http://api.tenderapp.com/help/profile')
        self.assertEquals(result['name'], 'Tender')

    def test_get_categories(self):
        result = self.client.get_categories()

        keys = (u'per_page', u'total', u'categories', u'offset')

#        import pprint
#        pp = pprint.PrettyPrinter(indent=4)
#        pp.pprint(result)

        for k in keys:
            assert result.has_key(k)

            if k == 'categories':
                for category in result[k]:
                    for ck in ('discussions_href', 'href', 'last_updated_at',
                                'name', 'permalink'):
                        assert category.has_key(ck)

    def test_get_discussions(self):
        result = self.client.get_discussions()

#        import pprint
#        pp = pprint.PrettyPrinter(indent=4)
#        pp.pprint(result)

        keys = (u'per_page', u'total', u'discussions', u'offset')
        for k in keys:
            assert result.has_key(k)

            if k == 'discussions':
                for discussion in result[k]:
                    for dk in ('author_email', 'author_name', 'category_href',
                                'comments_count', 'comments_href', 'created_at',
                                'href', 'last_author_email', 'last_author_name',
                                'last_comment_id', 'last_updated_at',
                                'last_user_id', 'last_via', 'number',
                                'permalink', 'public', 'resolve_href', 'state',
                                'title', 'toggle_href', 'via'):
                        assert discussion.has_key(dk)

#    def test_get_queues(self):
#        result = self.client.get_queues()

#        import pprint
#        pp = pprint.PrettyPrinter(indent=4)
#        pp.pprint(result)