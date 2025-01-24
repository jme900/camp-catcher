import re
import time
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
twilio_no = os.getenv("TWILIO_NO")
client = Client(twilio_sid, twilio_key)

validate_phone_number_pattern = "^\\+?[1-9][0-9]{7,14}$"
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
    for date in available_dates:
        response += f"{date}\n"
    return response


try:
    while True:
        try:
            # Display the list of park names for selection
            print('List of available places to monitor:')
            for i, park in parks_dict.items():
                print(f"{i}) {park.get('select_name')}")
            choice = int(input("Enter your choice: "))
            if choice in parks_dict.keys():
                selected_park = parks_dict[choice]
                print(f"You selected {selected_park['name']}")
                resource = Resource(selected_park["name"], selected_park["id"])
                reservation = Reservation(resource.id)
                while True:
                    val = input("Enter your phone number for notification: ")
                    number = re.match(validate_phone_number_pattern, val)
                    if number:
                        phone_number = number.group()
                        i = 0
                        print_with_border(f"\nChecking for available spots in\n{resource.name}\n\n")
                        while True:
                            i += 1
                            avail = reservation.find_availability()
                            if avail:
                                print(avail)
                                message = client.messages.create(
                                  from_=twilio_no,
                                  body=format_for_sms(resource.name, avail),
                                  to=str(phone_number)
                                )
                                break
                            else:
                                print(f"\rRecheck count: {i} | Last checked at: {time.strftime('%b %d - %H:%M:%S')}", end="", flush=True)
                                time.sleep(300)
                    else:
                        print("Invalid phone number. Please try again.")
            else:
                print(f"Invalid input. Please enter a number between 1 and {len(parks_dict.keys())}.")
        except ValueError:
            print("Invalid input. Please enter a number.")
except KeyboardInterrupt:
    print("\nStopped by user.")
