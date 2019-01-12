
# coding: utf-8

# In[31]:

import logging

logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='dav.log')

logger = logging.getLogger(__name__)


from datetime import datetime
import caldav
from caldav.elements import dav, cdav

# Caldav url
# url = "https://caldav.yandex.ru"
# url = 'https://caldav.yandex.ru/calendars/madhape@yandex.ru/events-default'
url = 'http://localhost:5232/123456/00bbdf0b-c94d-7041-6001-e98eb5f39dda/'

vcal = """BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Example Corp.//CalDAV Client//EN
BEGIN:VEVENT
UID:1234567890
DTSTAMP:20181222T180000Z
DTSTART:20181222T180000Z
DTEND:20181222T180000Z
SUMMARY:This is an event
END:VEVENT
END:VCALENDAR
"""
#client=caldav.DAVClient(url, username='madhape@yandex.ru', password='vtlbfyf12', ssl_verify_cert=False)  

client=caldav.DAVClient(url, username='123456', password='123456')


# In[33]:

principal = client.principal()


# In[34]:

calendars = principal.calendars()


# In[35]:
print(len(calendars))
if len(calendars) > 0:
    calendar = calendars[0]
    print("Using calendar", calendar)

    print("Renaming")
    calendar.set_properties([dav.DisplayName("Test calendar"),])
    print(calendar.get_properties([dav.DisplayName(),]))

    event = calendar.add_event(vcal)
    print("Event", event, "created")

    print("Looking for events in 2018-12")
    results = calendar.date_search(
        datetime(2018, 12, 1), datetime(2019,1, 10))

    for event in results:
        print("Found", event)

