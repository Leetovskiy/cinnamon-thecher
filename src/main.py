from datetime import datetime, timezone, timedelta

from thecher import load_config, get_sunrise_time, get_sunset_time, \
    suntime_switch_theme, wait_until

config = load_config()
tz_utc = timezone(timedelta(hours=0))

while True:
    sunrise_time = get_sunrise_time(lat=config['location']['latitude'],
                                    lon=config['location']['longitude'])
    sunset_time = get_sunset_time(lat=config['location']['latitude'],
                                  lon=config['location']['longitude'])

    suntime_switch_theme(sunrise=sunrise_time,
                         sunset=sunset_time,
                         themes=config['themes'])

    if sunset_time < datetime.now(tz_utc) < sunrise_time:
        wait_until(sunrise_time)
    else:
        wait_until(sunset_time + timedelta(days=1))
