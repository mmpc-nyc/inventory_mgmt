from unittest import TestCase

from api.serializers import CustomerSerializer


class TestCustomerSerializer(TestCase):
    def test_create(self):
        json_data = """[{
    "first_name": "Marek",
    "last_name": "Schir",
    "company_name": "MMPC",
    "contact_same_as_customer": true,
    "contacts": [
        {
            "first_name": "",
            "last_name": "",
            "email": "schir2@gmail.com",
            "phone": "7189093737"
        }
    ],
    "service_locations": [
        {
            "contact_same_as_customer": true,
            "line_one": "31-75 29th Street, Astoria NY 11106",
            "line_two": "Apt E8",
            "contacts": [
                {
                    "first_name": "",
                    "last_name": "",
                    "email": "",
                    "phone": ""
                }
            ],
            "name": "Home"
        }
    ],
    "billing_location": {
        "location_same_as_service_location": true,
        "contact_same_as_customer": true,
        "line_one": "",
        "line_two": "",
        "contacts": [
            {
                "first_name": "",
                "last_name": "",
                "email": "",
                "phone": ""
            },
            {
                "first_name": "",
                "last_name": "",
                "email": "",
                "phone": ""
            }
        ]
    }
}]"""

