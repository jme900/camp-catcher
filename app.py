import time
from datetime import datetime

from resource import Resource
from reservation import Reservation
from prettyprint import print_with_border

#  Change to whatever resource Name and ID you desire
resource = Resource("Lake O'Hara Backcountry Camping", "-2147471963")
start_date = datetime(2025, 7, 20, 0, 0, 0)
end_date = datetime(2025, 10, 1, 0, 0, 0)
reservation = Reservation(resource.resource_id, start_date, end_date)
print_with_border(f"\nChecking for available spots in\n{resource.name}\n\n")
i = 0
try:
    while True:
        i += 1
        avail = reservation.find_availability()
        if avail:
            print(avail)
            break
        else:
            print(f"\rRecheck count: {i} | Last checked at: {time.strftime('%b %d - %H:%M:%S')}", end="", flush=True)
            time.sleep(300)
except KeyboardInterrupt:
    print("\nStopped by user.")
