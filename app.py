import re
import time
from datetime import datetime

from dotenv import load_dotenv
import os
from twilio.rest import Client

from resource import Resource, load_park_resources
from reservation import Reservation
from prettyprint import print_with_border

load_dotenv()

# Access environment variables
twilio_sid = os.getenv("TWILIO_SID")
twilio_key = os.getenv("TWILIO_KEY")
twilio_no = os.getenv("TWILIO_NUMBER")
phone_number = os.getenv("PERSONAL_NUMBER")
client = Client(twilio_sid, twilio_key)

# Load resources into memory
parks = load_park_resources()
parks_dict = {}
idx = 0
for p in parks:
    for r in p.resources:
        idx += 1
        parks_dict[idx] = {
            "name": r.name,
            "select_name": f"{r.name} ({p.name})",
            "id": r.id,
        }


def format_for_sms(name, available_dates):
    response = f"Found {len(available_dates)} new day(s) for {name}:\n\n"
    response += "\n".join(available_dates)
    return response


def validate_date_input(date_text):
    try:
        date_obj = datetime.strptime(date_text, "%Y-%m-%d")
        if date_obj <= datetime.now():
            raise ValueError("Date must be in the future.")
        return date_obj
    except ValueError as e:
        print(f"Invalid date: {e}")
        return None


def get_resource_selection():
    print('List of available places to monitor:')
    for i, park in parks_dict.items():
        print(f"{i}) {park['select_name']}")
    while True:
        try:
            choice = int(input("Enter your choice: "))
            if choice in parks_dict:
                return parks_dict[choice]
            else:
                print(f"Invalid input. Please enter a number between 1 and {len(parks_dict)}.")
        except ValueError:
            print("Invalid input. Please enter a number.")


def get_date_range():
    while True:
        start_date_input = input("Enter the start date (YYYY-MM-DD): ")
        start_date = validate_date_input(start_date_input)
        if start_date:
            break
    while True:
        end_date_input = input("Enter the end date (YYYY-MM-DD): ")
        end_date = validate_date_input(end_date_input)
        if end_date and end_date > start_date:
            return start_date, end_date
        else:
            print("End date must be after the start date.")


def monitor_reservations(resource, reservation):
    i = 0
    print_with_border(f"\nChecking for available spots in\n{resource.name}\n\n")
    while True:
        i += 1
        avail = reservation.find_availability()
        if avail:
            print(avail)
            client.messages.create(
                from_=twilio_no,
                body=format_for_sms(resource.name, avail),
                to=phone_number
            )
            break
        else:
            print(f"\rRecheck count: {i} | Last checked at: {time.strftime('%b %d - %H:%M:%S')}", end="", flush=True)
            time.sleep(300)


def main():
    try:
        while True:
            selected_park = get_resource_selection()
            print(f"You selected {selected_park['name']}")
            start_date, end_date = get_date_range()

            resource = Resource(selected_park["name"], selected_park["id"])
            reservation = Reservation(resource.id, start_date, end_date)
            monitor_reservations(resource, reservation)
    except KeyboardInterrupt:
        print("\nStopped by user.")


if __name__ == "__main__":
    main()
