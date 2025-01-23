import time
from resource import Resource
from reservation import Reservation
from prettyprint import print_with_border

#  Change to whatever resource Name and ID you desire
resource = Resource("Lake O'Hara Backcountry Camping", "-2147471963")
reservation = Reservation(resource.resource_id)
print_with_border(f"\nChecking for available spots in\n{resource.name}\n\n")
while True:
    avail = reservation.find_availability()
    if avail:
        print(avail)
    else:
        time.sleep(60)
