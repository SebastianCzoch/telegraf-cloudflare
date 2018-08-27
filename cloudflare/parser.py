import calendar
from dateutil import parser
from influx import Metric, MetricCollection


class Parser(object):

    NANOSECONDS_MULTIPILER = 10 ** 9

    def parse_dashboard(self, zone_id, dashboard):
        collections = MetricCollection()
        [collections.append(self.parse_timeserie(zone_id, timeserie)) for timeserie in dashboard['timeseries']]

        return collections

    def parse_timeserie(self, zone_id, timeserie):
        metric = Metric('cloudflare')
        metric.with_timestamp(self.parse_time(timeserie['until']))
        metric.add_tag('zone_id', zone_id)
        metric.add_value('uniques', timeserie['uniques']['all'])
        self.__parse_requests(metric, timeserie['requests'])
        self.__parse_bandwidth(metric, timeserie['bandwidth'])

        return metric

    def __parse_requests(self, metric, requests):
        metric.add_value('requests_all', requests['all'])
        metric.add_value('requests_cached', requests['cached'])
        metric.add_value('requests_uncached', requests['uncached'])
        metric.add_value('requests_encrypted', requests['ssl']['encrypted'])
        metric.add_value('requests_unencrypted', requests['ssl']['unencrypted'])

        for status in requests['http_status']:
            metric.add_value('requests_status_%s' % status, requests['http_status'][status])

        for content_type in requests['content_type']:
            metric.add_value('requests_content_type_%s' % content_type, requests['content_type'][content_type])

        for country in requests['country']:
            metric.add_value('requests_country_%s' % country.lower(), requests['country'][country])

        for ip_class in requests['ip_class']:
            metric.add_value('requests_ip_class_%s' % ip_class, requests['ip_class'][ip_class])

    def __parse_bandwidth(self, metric, bandwidth):
        metric.add_value('bandwidth_all', bandwidth['all'])
        metric.add_value('bandwidth_cached', bandwidth['cached'])
        metric.add_value('bandwidth_uncached', bandwidth['uncached'])
        metric.add_value('bandwidth_encrypted', bandwidth['ssl']['encrypted'])
        metric.add_value('bandwidth_unencrypted', bandwidth['ssl']['unencrypted'])

        for content_type in bandwidth['content_type']:
            metric.add_value('bandwidth_content_type_%s' % content_type, bandwidth['content_type'][content_type])

        for country in bandwidth['country']:
            metric.add_value('bandwidth_country_%s' % country.lower(), bandwidth['country'][country])

    def parse_time(self, datetime):
        d = parser.parse(datetime)
        return int(calendar.timegm(d.timetuple())) * self.NANOSECONDS_MULTIPILER
