import requests


class Client(object):

    CLOUDFLARE_API_URL = 'https://api.cloudflare.com/client/v4'

    def __init__(self, zone_id, email, api_key):
        self.zone_id = zone_id
        self.email = email
        self.api_key = api_key

    def get_dashboard(self, interval):
        url = '%s/zones/%s/analytics/dashboard?since=-%d&continuous=true' % (
            self.CLOUDFLARE_API_URL, self.zone_id, interval)

        return self.__make_call(url)

    def __make_call(self, url):
        headers = {
            'X-Auth-Email': self.email,
            'X-Auth-Key': self.api_key,
            'Content-Type': 'application/json',
        }

        resp = requests.get(url, headers=headers)
        if resp.status_code != 200:
            self.__raise_error(resp)

        return resp.json()['result']

    def __raise_error(self, response):
        try:
            resp = response.json()
        except Exception:
            raise Exception(
                'Invalid status code, got %s, expected 200' %
                response.status_code)

            if len(resp['errors']) > 0:
                messages = ["Error: %d - %s" % (msg.code, msg.message)
                            for msg in resp['errors']]

                raise Exception(", ".join(messages))

        raise Exception(
            'Invalid status code, got %s, expected 200' %
            response.status_code)
