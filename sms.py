from ipaddress import IPv4Address
from pyairmore.request import AirmoreSession
from pyairmore.services.messaging import MessagingService, MessageRequestGSMError

ip = IPv4Address("10.0.0.89")
session = AirmoreSession(ip)
service = MessagingService(session)
try:
    service.send_message("+33651216491", "Hello5")
except MessageRequestGSMError:
    print("Envoi échoué")