# telegraf-cloudflare
[![Build Status](https://travis-ci.org/SebastianCzoch/telegraf-cloudflare.svg?branch=master)](https://travis-ci.org/SebastianCzoch/telegraf-cloudflare/branches) [![PyPI version](https://badge.fury.io/py/telegraf-cloudflare.svg)](https://badge.fury.io/py/telegraf-cloudflare) [![License](https://img.shields.io/badge/license-MIT-brightgreen.svg)](https://github.com/SebastianCzoch/telegraf-cloudflare/blob/master/LICENSE)

Plugin for Telegraf for gathering statistics from Cloudflare

This script is in beta version, use with caution

## Installation
```bash
$ pip install telegraf-cloudflare
```

## Usage
```bash
$ telegraf-cloudflare --zone-id ZONE_ID --email you@example.com --api-key SECRET
```

### Optional parameters
* `--interval` (int)
  * Last 60 minutes (value from 59 to 1): 1 minute resolution
  * Last 7 hours (value from 419 to 60): 15 minutes resolution
  * Last 15 hours (value from 899 to 420): 30 minutes resolution
  * Last 72 hours (value from 4320 to 900): 1 hour resolution
  * Older than 3 days (value 525600 to 4320): 1 day resolution

  Not all intervals are available in all plans, more information available [here](https://api.cloudflare.com/#zone-analytics-dashboard)

### Example telegraf configuration
```
[[inputs.exec]]
  interval = 6h
  commands = ["telegraf-cloudflare telegraf-cloudflare --zone-id ZONE_ID --email you@example.com --api-key SECRET"]
  data_format = "influx"
```

## License
See [LICENSE](https://github.com/SebastianCzoch/telegraf-cloudflare/blob/master/LICENSE) file.
