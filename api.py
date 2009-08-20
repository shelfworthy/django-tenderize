class Client:
    def __init__(self, user, password):
        self.user = user
        self.password = password

    def _send_query(self, url):
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

        f = urllib2.urlopen(req)
        return f.read()

    def _parse_response(self, response):
        '''
        Parse JSON response
        '''
        from django.utils import simplejson

        return simplejson.loads(response)

    def __get__(self, url):
        response = self._send_query(url)
        return self._parse_response(response)

    def get_sites(self):
        return self.__get__('http://api.tenderapp.com/help')

    def get_categories(self):
        return self.__get__('http://api.tenderapp.com/help/categories')

    def get_discussions(self):
        return self.__get__('http://api.tenderapp.com/help/discussions')

    def get_queues(self):
        '''
        Have no idea why but it always returns 401: Unauthorized
        '''
        return self.__get__('http://api.tenderapp.com/help/queues')