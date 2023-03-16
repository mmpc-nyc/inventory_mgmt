import datetime
from unittest import TestCase
from inventory.utils.epa_scraper import SeleniumScraper, Pesticide

pesticides = [Pesticide(
    registration_number='54471-10',
    label='BORAX-COPPER HYDROXIDE WOOD PRESERVATIVE PASTE',
    company_name='COPPER CARE WOOD PRESERVATIVES, INC,',
    address='',
    po_box='707',
    city='Columbus',
    state='NE',
    zipcode='686020707',
    first_registered_date=datetime.datetime(year=1997, month=6, day=25).date(),
    current_registered_date=datetime.datetime(year=1997, month=6, day=25).date(),
    registered=True,
    restricted_use=False,
    active_ingredients={
        'Borax (B4Na2O7.10H2O)':
            {
                'name': 'Borax (B4Na2O7.10H2O)',
                'concentration': 43.5,
                'url': 'https://iaspub.epa.gov/apex/pesticides/f?p=CHEMICALSEARCH:3:::NO::P3_XCHEMICAL_ID:1572'
            },
        'Copper hydroxide':
            {
                'name': 'Copper hydroxide',
                'concentration': 3.1,
                'url': 'https://iaspub.epa.gov/apex/pesticides/f?p=CHEMICALSEARCH:3:::NO::P3_XCHEMICAL_ID:1895'
            }
    },
    sites=[
        'LUMBER',
        'TIMBERS',
        'WOOD PILINGS (SOIL CONTACT NONFUMIGATION TREATMENT)',
        'WOOD POLES/POSTS (SOIL CONTACT NONFUMIGATION TREATMENT)',
        'WOOD PRODUCTS (UNSEASONED)',
        'WOOD PROTECTION TRT TO FOREST PRODUCTS BY PRESSURE',
        'WOOD PROTECTION TRT TO SEASONED FOREST PRODUCTS',
        'WOOD STRUCTURES (SOIL CONTACT NONFUMIGATION TREATMENT)',
        'WOOD UTILITY POLES (SOIL CONTACT NONFUMIGATION TREATMENT)',
    ],
    pests=[
        'CARPENTER ANTS',
        'ROT FUNGI',
        'SOFT ROT/DECAY',
        'TERMITES',
        'WOOD BORING BEETLES',
        'WOOD BORING INSECTS',
        'WOOD ROT/DECAY FUNGI',
    ]
)]


class TestBrowser(TestCase):
    browser = None
    pesticide = pesticides[0]

    @classmethod
    def setUpClass(cls) -> None:
        cls.browser = SeleniumScraper()
        cls.browser._lookup_epa_number(pesticides[0].registration_number)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.browser.driver.close()

    def test_lookup_epa_number(self):
        for pesticide in pesticides:
            self.browser._lookup_epa_number(pesticide.registration_number)

    def test__get_pesticide_label(self):
        self.assertEqual(self.pesticide.label, self.browser._get_pesticide_label())

    def test__get_pesticide_registration_number(self):
        self.assertEqual(self.pesticide.registration_number, self.browser._get_pesticide_registration_number())

    def test__get_pesticide_company_name(self):
        self.assertEqual(self.pesticide.company_name, self.browser._get_pesticide_company_name())

    def test__get_pesticide_address(self):
        self.assertEqual( self.pesticide.address, self.browser._get_pesticide_address())

    def test__get_pesticide_po_box(self):
        self.assertEqual(self.pesticide.po_box, self.browser._get_pesticide_po_box())

    def test__get_pesticide_city(self):
        self.assertEqual(self.pesticide.city, self.browser._get_pesticide_city())

    def test__get_pesticide_state(self):
        self.assertEqual(self.pesticide.state, self.browser._get_pesticide_state())

    def test__get_pesticide_zip(self):
        self.assertEqual(self.pesticide.zipcode, self.browser._get_pesticide_zipcode())

    def test__get_pesticide_first_registered_date(self):
        self.assertEqual(self.pesticide.first_registered_date, self.browser._get_pesticide_first_registered_date())

    def test__get_pesticide_current_registered_date(self):
        self.assertEqual(self.pesticide.current_registered_date, self.browser._get_pesticide_current_registered_date())

    def test__get_pesticide_registered(self):
        self.assertEqual(self.pesticide.registered, self.browser._get_pesticide_registered())

    def test__get_pesticide_restricted_use(self):
        self.assertEqual(self.pesticide.restricted_use, self.browser._get_pesticide_restricted_use())

    def test__get_pesticide_active_ingredients(self):
        self.assertEqual(self.pesticide.active_ingredients, self.browser._get_pesticide_active_ingredients())

    def test__get_pesticide_sites(self):
        self.assertEqual(self.pesticide.sites, self.browser._get_pesticide_sites())

    def test__get_pesticide_pests(self):
        self.assertEqual(self.pesticide.pests, self.browser._get_pesticide_pests())

    def test__get_basic_epa_information_from_source(self):
        self.assertEqual(self.pesticide, self.browser._parse_pesticide())