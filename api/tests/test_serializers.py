from unittest import TestCase

from api.serializers import CustomerSerializer


class TestCustomerSerializer(TestCase):
    def test_create(self):
        from api.serializers import CustomerSerializer
        import json
        json_data = """{
    "first_name": "Marek",
    "last_name": "Schir",
    "company_name": "MMPC",
    "customer_type": "Residential",
    "email": "schir2@gmail.com",
    "phone_number": "7189093737",
    "billing_contact_same_as_customer": true,
    "contacts": [
        {
            "first_name": "",
            "last_name": "",
            "emails": [
                ""
            ],
            "phone_numbers": [
                ""
            ]
        }
    ],
    "service_locations": [
        {
            "name": "31-75 29th St",
            "street_address": "31-75 29th St, Queens, NY 11106, USA",
            "address_line_2": "Apt E8",
            "city": "Queens",
            "state": "New York",
            "postal_code": "11106",
            "latitude": 40.7630659,
            "longitude": -73.9263678,
            "contact_same_as_customer": true,
            "contacts": [
                {
                    "first_name": "",
                    "last_name": "",
                    "emails": [
                        ""
                    ],
                    "phone_numbers": [
                        ""
                    ]
                }
            ]
        }
    ],
    "billing_location": {
        "name": "",
        "street_address": "",
        "address_line_2": "",
        "city": "",
        "state": "",
        "postal_code": "",
        "latitude": "",
        "longitude": "",
        "contact_same_as_customer": true,
        "contacts": [
            {
                "first_name": "",
                "last_name": "",
                "emails": [
                    ""
                ],
                "phone_numbers": [
                    ""
                ]
            }
        ]
    },
    "billing_location_same_as_service_location": true
}"""
        data = json.loads(json_data)
        customer = CustomerSerializer(data=data)
        if not customer.is_valid():
            print(customer.errors)
            self.assertTrue(customer.is_valid())
        print(customer.validated_data)
        customer.create(customer.validated_data)
