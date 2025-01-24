from enum import Enum
from datetime import datetime, timedelta, timezone
import requests
import json

BASE_API_URL = "https://reservation.pc.gc.ca/api/availability/resourcedailyavailability"
HEADERS = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip,deflate,utf-8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, '
                  'like Gecko) Chrome/115.0.0.0 Safari/537.36',
}


class AvailabilityStatus(Enum):
    AVAILABLE = 0  # this is the only one we care about
    UNAVAILABLE = 1
    CLOSED = 2
    NOT_RESERVABLE = 3
    BOOKED = 4  # maybe...
    RESTRICTED = 5
    UNAVAILABLE_DUE_TO = 6  # unavailable due to something with the reservation request
    PARTIAL = 7


def _format_date_to_string(date: datetime) -> str:
    return date.strftime("%Y-%m-%d")


def _start_of_year_utc():
    current_year = datetime.now(timezone.utc).year
    start_of_year = datetime(current_year, 1, 1, 0, 0, 0)
    return start_of_year


def _end_of_year_utc():
    current_year = datetime.now(timezone.utc).year
    end_of_year = datetime(current_year, 12, 31, 0, 0, 0)
    return end_of_year


class Reservation(object):
    def __init__(self, resource_id: str, start_day: datetime = None, end_day: datetime = None):
        self.resource_id = resource_id
        if start_day is None:
            start_day = _start_of_year_utc()
        if end_day is None:
            end_day = _end_of_year_utc()
        if start_day > end_day:
            raise ValueError("The start date must be before or equal to the end date.")
        self.start_day_str = _format_date_to_string(start_day)
        self.end_day_str = _format_date_to_string(end_day)
        self.start_day = start_day
        self.end_day = end_day

    def find_availability(self):
        resp = self._connect()
        available_days = []
        if resp and isinstance(resp, list):
            days_from_start = 0
            for item in resp:
                if item['availability'] == AvailabilityStatus.AVAILABLE.value:
                    available_days.append(_format_date_to_string(self.start_day + timedelta(days=days_from_start)))
                days_from_start += 1
        return available_days

    def __repr__(self):
        return (f"Reservation("
                f"resource_id={self.resource_id}, "
                f"start_day={self.start_day_str}, "
                f"end_day={self.end_day_str})"
                )

    def __str__(self):
        return self.__repr__()

    def _connect(self):
        response = None
        url = f"{BASE_API_URL}?resourceId={self.resource_id}&startDate={self.start_day_str}&endDate={self.end_day_str}"
        try:
            response = requests.get(url, headers=HEADERS)
            if response:
                response = json.loads(response.text)
        except Exception as e:
            print('ERROR', e)
        return response
