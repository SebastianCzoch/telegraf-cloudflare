import unittest
from .parser import Parser
from influx import Metric
from influx import MetricCollection


class ParserTest(unittest.TestCase):
    timeserie = {
        "until": "2018-08-22T11:45:00Z",
        "requests": {
          "all": 258,
          "cached": 142,
          "uncached": 116,
          "ssl": {
            "encrypted": 255,
            "unencrypted": 3
          },
          "http_status": {
            "200": 229,
            "499": 2
          },
          "content_type": {
            "css": 10,
            "html": 96,
          },
          "country": {
            "PL": 183,
            "US": 14
          },
          "ip_class": {
            "monitoringService": 13,
            "noRecord": 215,
            "searchEngine": 30
          }
        },
        "bandwidth": {
          "all": 4607212,
          "cached": 2985600,
          "uncached": 1621612,
          "ssl": {
            "encrypted": 4606145,
            "unencrypted": 1067
          },
          "content_type": {
            "css": 273141,
            "html": 1618653,
          },
          "country": {
            "PL": 3712599,
            "US": 231584
          }
        },
        "uniques": {
          "all": 116
        }
      }

    def setUp(self):
        self.metric = Metric('cloudflare')
        self.metric.add_tag('zone_id', 'test')
        self.metric.with_timestamp(15376167000000000000)
        self.metric.values = {
            'uniques': '116',
            'requests_all': '258',
            'requests_cached': '142',
            'requests_uncached': '116',
            'requests_encrypted': '255',
            'requests_unencrypted': '3',
            'requests_status_200': '229',
            'requests_status_499': '2',
            'requests_content_type_css': '10',
            'requests_content_type_html': '96',
            'requests_country_us': '14',
            'requests_country_pl': '183',
            'requests_ip_class_monitoringService': '13',
            'requests_ip_class_noRecord': '215',
            'requests_ip_class_searchEngine': '30',
            'bandwidth_all': '4607212',
            'bandwidth_cached': '2985600',
            'bandwidth_uncached': '1621612',
            'bandwidth_encrypted': '4606145',
            'bandwidth_unencrypted': '1067',
            'bandwidth_content_type_css': '273141',
            'bandwidth_content_type_html': '1618653',
            'bandwidth_country_pl': '3712599',
            'bandwidth_country_us': '231584',

        }

    def test_only_one_serie(self):
        expectedCollection = MetricCollection()
        expectedCollection.append(self.metric)
        timeseries = {'timeseries': [self.timeserie]}

        a = Parser()
        collection = a.parse_dashboard("test", timeseries)

        self.maxDiff = None
        self.assertDictEqual(expectedCollection.metrics[0].values, collection.metrics[0].values)

    def test_multiple_series(self):
        expectedCollection = MetricCollection()
        expectedCollection.append(self.metric)
        expectedCollection.append(self.metric)

        timeseries = {'timeseries': [self.timeserie, self.timeserie]}

        a = Parser()
        collection = a.parse_dashboard("test", timeseries)

        self.maxDiff = None
        self.assertDictEqual(expectedCollection.metrics[0].values, collection.metrics[0].values)

    def test_parse_time(self):
        dtime = '2018-09-22T11:45:00Z'
        expected_timestamp = 1537616700 * 10**9

        p = Parser()
        self.assertEqual(p.parse_time(dtime), expected_timestamp)
