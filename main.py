import geocoder
import requests
from ics import Calendar, Event
from datetime import datetime, timedelta
import re
import pytz


def get_latitude_longitude():
    g = geocoder.ip("me")
    latitude = g.latlng[0]
    longitude = g.latlng[1]
    return latitude, longitude


def get_data(latitude, longitude, method):
    url = f"http://api.aladhan.com/v1/calendar/2023?latitude={latitude}&longitude={longitude}&method=2"

    response = requests.get(url)
    data = response.json()

    return data


def extract_prayer_times_and_dates(data):
    desired_prayers = {"Fajr", "Dhuhr", "Asr", "Maghrib", "Isha"}
    prayer_times_and_dates = []

    data_entries = data.get("data", {})
    for key, value in data_entries.items():
        if isinstance(value, list):
            for daily_data in value:
                timings = daily_data.get("timings", {})
                date_info = (
                    daily_data.get("date", {}).get("gregorian", {}).get("date", "")
                )
                timezone = daily_data.get("meta", {}).get("timezone", "")
                if timings and date_info and timezone:
                    for prayer, time in timings.items():
                        if prayer not in desired_prayers:
                            continue
                        time = re.sub(r"\s\(.*\)", "", time)
                        datetime_str = f"{date_info} {time}"
                        dt = datetime.strptime(datetime_str, "%d-%m-%Y %H:%M")
                        tz = pytz.timezone(timezone)
                        localized_dt = tz.localize(dt)
                        prayer_times_and_dates.append((prayer, localized_dt))

    return prayer_times_and_dates


def generate_ical(prayer_times_and_dates):
    ical_header = "BEGIN:VCALENDAR\nVERSION:2.0\nCALSCALE:GREGORIAN\nX-WR-CALNAME:Salah"
    ical_events = []

    for prayer, dt in prayer_times_and_dates:
        dt_end = dt + timedelta(minutes=10)  # Extending prayer time by 10 minutes
        ical_event = [
            "BEGIN:VEVENT",
            f"DTSTART;TZID={dt.tzinfo.zone}:{dt.strftime('%Y%m%dT%H%M%S')}",
            f"DTEND;TZID={dt.tzinfo.zone}:{dt_end.strftime('%Y%m%dT%H%M%S')}",
            f"SUMMARY:{prayer} Prayer",
            f"DESCRIPTION:{prayer} Prayer",
            "STATUS:CONFIRMED",
            "END:VEVENT",
        ]
        ical_events.append("\n".join(ical_event))

    ical_content = "{}\n{}\nEND:VCALENDAR".format(ical_header, "\n".join(ical_events))
    ical_file_path = "/Users/hudzah/Documents/Work/SalahCal/prayer_times.ics"
    with open(ical_file_path, "w") as ical_file:
        ical_file.write(ical_content)


def main():
    latitude, longitude = get_latitude_longitude()
    data = get_data(latitude, longitude, 2)
    prayer_times_and_dates = extract_prayer_times_and_dates(data)
    generate_ical(prayer_times_and_dates)


if __name__ == "__main__":
    main()
