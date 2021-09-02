from os import system as os_system
from datetime import datetime, timedelta, timezone
from suntime import Sun
import json
from typing import Optional, Dict
from time import sleep

__all__ = ['load_config', 'suntime_switch_theme', 'get_sunrise_time',
           'get_sunset_time', 'wait_until']
THEMES_PREFERS_TYPE = Dict[str, Dict[str, str]]


def switch_themes(desktop: str,
                  win_borders: str,
                  controls: Optional[str] = None,
                  icons: Optional[str] = None,
                  cursor: Optional[str] = None) -> None:
    """Switch themes to passed values"""
    os_system(f'gsettings set org.cinnamon.theme name \'{desktop}\'')
    os_system(f'gsettings set org.cinnamon.desktop.wm.preferences theme \'{win_borders}\'')
    os_system(f'gsettings set org.cinnamon.desktop.interface gtk-theme \'{controls}\'')

    if icons:
        os_system(f'gsettings set org.cinnamon.desktop.interface icon-theme \'{icons}\'')

    if cursor:
        os_system(f'gsettings set org.cinnamon.desktop.interface cursor-theme \'{cursor}\'')


def load_config() -> Dict[str, dict]:
    """Return a dict contains config settings"""
    with open('data/config.json') as config_file:
        return json.load(config_file)


def suntime_switch_theme(sunrise: datetime,
                         sunset: datetime,
                         themes: THEMES_PREFERS_TYPE) -> None:
    """
    Switch themes according to the current time

    Pass sunrise and sunset times of the place user's located and function will
    switch the themes according this info.

    The `themes` are the presets of the themes you prefer to use. The parameter
    must contain a dict with the keys `light` and `dark`. Each of them must
    contain another dict with the keys:
        - `desktop`
        - `win_borders`
        - `controls`
        - 'icons'
        - `cursor`.
    Each of them must contain a line with the name of the theme (exclude
    icons and cursor: they can be None value)
    """

    utc = timezone(timedelta(hours=0))

    if sunrise < datetime.now(utc) < sunset:
        theme_type = 'light'
    else:
        theme_type = 'dark'
    switch_themes(**themes[theme_type])


def get_sunrise_time(lat: float, lon: float) -> datetime:
    """
    Get the time of sunrise

    Takes the latitude and longitude of a location and returns the
    sunrise time for that location. The time is a datetime object in UTC
    format.
    """

    sun = Sun(lat, lon)
    sunrise = sun.get_sunrise_time()
    return sunrise


def get_sunset_time(lat: float, lon: float) -> datetime:
    """
    Get the time of sunset

    Takes the latitude and longitude of a location and returns the
    sunset time for that location. The time is a time object in local
    format.
    """

    sun = Sun(lat, lon)
    sunset = sun.get_sunset_time()
    return sunset


def wait_until(time: datetime) -> None:
    """
    Sleep until specific time

    `time` parameter must be a datetime-object in UTC format
    """

    utc = timezone(timedelta(hours=0))
    sleep(
        (time - datetime.now(utc)).total_seconds()
    )
