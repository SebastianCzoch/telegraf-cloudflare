import sys
import unittest
from .client import Client

if sys.version_info >= (3, 3):
    from unittest import mock
else:
    import mock


class TestClient(unittest.TestCase):

    @mock.patch('requests.get')
    def test_get_dashboard_non_200_response_without_errors(self, mock_get):
        mock_resp = self.__mock_response(status=500)
        mock_get.return_value = mock_resp

        client = Client("zone", "email", "key")
        self.assertRaises(Exception,
                          client.get_dashboard, 1,
                          msg="Invalid status code, got 500, expected 200")

    @mock.patch('requests.get')
    def test_get_dashboard_non_200_response_with_empty_errors(self, mock_get):
        mock_resp = self.__mock_response(status=500, json_data={'errors': []})
        mock_get.return_value = mock_resp

        client = Client("zone", "email", "key")
        self.assertRaises(Exception,
                          client.get_dashboard, 1,
                          msg="Invalid status code, got 500, expected 200")

    @mock.patch('requests.get')
    def test_get_dashboard_non_200_response_with_errors(self, mock_get):
        mock_get.return_value = self.__mock_response(
          status=500, json_data={'errors': [
                                {'code': 10, 'message': 'test'},
                                {'code': 11, 'message': 'test1'}]})

        client = Client("zone", "email", "key")
        self.assertRaises(Exception,
                          client.get_dashboard, 1,
                          msg="Error: 10 - test, Error 11 - test1")

    @mock.patch('requests.get')
    def test_get_dashboard_success(self, mock_get):
        expected_url = 'https://api.cloudflare.com/client/v4/zones/zone' \
                        '/analytics/dashboard?since=-1&continuous=true'
        expected_headers = {
            'X-Auth-Email': 'email',
            'X-Auth-Key': 'key',
            'Content-Type': 'application/json',
        }

        mock_get.return_value = self.__mock_response(
          status=200, json_data={'result': {'success': True}})

        client = Client("zone", "email", "key")
        self.assertEqual({'success': True}, client.get_dashboard(1))
        mock_get.assert_called_with(expected_url, headers=expected_headers)

    def __mock_response(self, status=200, json_data=None, raise_on_json=None):
        response = mock.Mock()
        response.status_code = status
        response.json = mock.Mock()
        if json_data:
            response.json = mock.Mock(
                return_value=json_data
            )

        if raise_on_json is not None:
            response.json.side_effect = raise_on_json

        return response
