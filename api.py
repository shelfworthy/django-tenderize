from django.utils import simplejson

class Client:
    def __init__(self, user, password):
        self.user = user
        self.password = password

    def _send_query(self, url, data=None):
        '''
        Send a query to Tender API
        '''
        import urllib2
        from base64 import b64encode

        req = urllib2.Request(url=url)
        req.add_header('Accept', 'application/vnd.tender-v1+json')
        req.add_header(
            'Authorization', 'Basic %s' % b64encode(
                '%s:%s' % (self.user, self.password)
            )
        )
        if data:
            req.add_header('Content-Type', 'application/json')
            req.add_data(simplejson.dumps(data))

        #print req.get_method(), req.get_data(), req.get_full_url()

        f = urllib2.urlopen(req)
        return f.read()

    def _parse_response(self, response):
        '''
        Parse JSON response
        '''
        return simplejson.loads(response)

    def __get__(self, url, data=None):
        response = self._send_query(url, data)
        return self._parse_response(response)

    def get_sites(self):
        return self.__get__('http://api.tenderapp.com/shelfworthy')

    def get_categories(self):
        return self.__get__('http://api.tenderapp.com/shelfworthy/categories')

    def get_discussions(self):
        return self.__get__('http://api.tenderapp.com/shelfworthy/discussions')

    def get_queues(self):
        '''
        Have no idea why but it always returns 401: Unauthorized
        '''
        return self.__get__('http://api.tenderapp.com/shelfworthy/queues')

    def create_discussion(self, data, category=None):
        '''
        Creates a discussion from POST data
        '''
        url = 'http://api.tenderapp.com/shelfworthy/categories/10267/discussions'
        #if category:
        #    url = '%s/%s' % (url, category)

        return self.__get__(url, data)