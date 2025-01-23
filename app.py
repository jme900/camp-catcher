import time
from resource import Resource
from reservation import Reservation

#  Change to whatever resource Name and ID you desire
resource = Resource("Lake O'Hara Backcountry Camping", "-2147471963")
reservation = Reservation(resource.resource_id)
print(resource.name)
while True:
    avail = reservation.find_availability()
    if avail:
        print(avail)
    else:
        time.sleep(60)
