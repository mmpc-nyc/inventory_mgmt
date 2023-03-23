from dataclasses import dataclass
from datetime import datetime

from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By

from inventory.utils.datetime_utils import date_from_string

SEARCH_URL = 'https://ordspub.epa.gov/ords/pesticides/f?p=PPLS:1'
SEARCH_INPUT_ID = 'P1_EPA_REG_NO'

@dataclass
class Pesticide:
    registration_number: str
    label: str
    company_name: str
    address: str
    po_box: str
    city: str
    state: str
    zipcode: str
    first_registered_date: datetime.date
    current_registered_date: datetime.date
    registered: bool
    restricted_use: bool
    active_ingredients: dict[str, dict]
    sites: list[str]
    pests: list[str]


class SeleniumScraper:

    def __init__(self):
        self.driver = webdriver.Chrome()

    def parse_pesticide(self, epa_number: str | int):
        self._lookup_epa_number(epa_number=epa_number)
        return self._parse_pesticide()

    def _lookup_epa_number(self, epa_number: str | int):

        self.driver.get(SEARCH_URL)
        search_input = self.driver.find_element(By.ID, SEARCH_INPUT_ID)
        search_input.send_keys(epa_number)
        search_input.send_keys(Keys.RETURN)

    def _get_pesticide_label(self):
        self.driver.find_element(By.LINK_TEXT, 'Labels').click()
        try:
            value = self.driver.find_element(By.XPATH, "//td[@headers='RIN_NAME']")
        except NoSuchElementException:
            return ''
        return value.text

    def _get_pesticide_registration_number(self):
        try:
            value = self.driver.find_element(By.ID, 'P8_RI_NUM')
        except NoSuchElementException:
            return ''
        return value.text

    def _get_pesticide_company_name(self):
        try:
            value = self.driver.find_element(By.ID, 'P8_CO_NAME')
        except NoSuchElementException:
            return ''
        return value.text

    def _get_pesticide_address(self):
        try:
            value = self.driver.find_element(By.ID, 'P8_CO_ADDRESS')
        except NoSuchElementException:
            return ''
        return value.text

    def _get_pesticide_po_box(self):
        try:
            value = self.driver.find_element(By.ID, 'P8_CO_PO_BOX')
        except NoSuchElementException:
            return ''
        return value.text

    def _get_pesticide_city(self):
        try:
            value = self.driver.find_element(By.ID, 'P8_CO_FULL_CITY')
        except NoSuchElementException:
            return ''
        return value.text.split(',')[0].title()

    def _get_pesticide_state(self):
        try:
            value = self.driver.find_element(By.ID, 'P8_CO_FULL_CITY')
        except NoSuchElementException:
            return ''
        return value.text.split(', ')[1].split(' ')[0]

    def _get_pesticide_zipcode(self):
        try:
            value = self.driver.find_element(By.ID, 'P8_CO_FULL_CITY')
        except NoSuchElementException:
            return ''
        return value.text.split(', ')[1].split(' ')[1]

    def _get_pesticide_first_registered_date(self):
        try:
            value = self.driver.find_element(By.ID, 'P8_FIRST_REGISTERED').text
        except NoSuchElementException:
            return ''
        return date_from_string(value)

    def _get_pesticide_current_registered_date(self):
        try:
            value = self.driver.find_element(By.ID, 'P8_CNT_STATUS')
        except NoSuchElementException:
            return ''
        return date_from_string(value.text.split('(')[1][:-1])

    def _get_pesticide_registered(self):
        try:
            value = self.driver.find_element(By.ID, 'P8_CNT_STATUS')
        except NoSuchElementException:
            return ''
        return True if 'Registered' in value.text else False

    def _get_pesticide_restricted_use(self):
        try:
            value = self.driver.find_element(By.ID, 'P8_RUP_YN')
        except NoSuchElementException:
            return ''
        return True if value.text == 'YES' else False

    def _get_pesticide_active_ingredients(self):
        self.driver.find_element(By.LINK_TEXT, 'Chemical').click()
        try:
            chemicals = self.driver.find_elements(By.XPATH, "//td[@headers='CHEM_LINK']")
            concentrations = self.driver.find_elements(By.XPATH, "//td[@headers='RII_PERCENT_WT_WT_VAL']")
        except NoSuchElementException:
            return []
        return {
            chemical.text: {
                'name': chemical.text,
                'url': chemical.find_element(By.TAG_NAME, 'a').get_attribute('href'),
                'concentration': float(concentration.text)
            } for chemical, concentration in zip(chemicals, concentrations)
        }

    def _get_pesticide_sites(self):
        self.driver.find_element(By.LINK_TEXT, 'Site').click()
        try:
            sites = self.driver.find_elements(By.XPATH, "//td[@headers='SITE_DESC']")
        except NoSuchElementException:
            return []
        return [site.text for site in sites]

    def _get_pesticide_pests(self):
        self.driver.find_element(By.LINK_TEXT, 'Pest').click()
        try:
            pests = self.driver.find_elements(By.XPATH, "//td[@headers='PEST_DESC']")
        except NoSuchElementException:
            return []
        return [pest.text for pest in pests]

    def _parse_pesticide(self) -> Pesticide:
        return Pesticide(
            label=self._get_pesticide_label(),
            registration_number=self._get_pesticide_registration_number(),
            company_name=self._get_pesticide_company_name(),
            address=self._get_pesticide_address(),
            po_box=self._get_pesticide_po_box(),
            city=self._get_pesticide_city(),
            state=self._get_pesticide_state(),
            zipcode=self._get_pesticide_zipcode(),
            first_registered_date=self._get_pesticide_first_registered_date(),
            current_registered_date=self._get_pesticide_current_registered_date(),
            registered=self._get_pesticide_registered(),
            restricted_use=self._get_pesticide_restricted_use(),
            active_ingredients=self._get_pesticide_active_ingredients(),
            sites=self._get_pesticide_sites(),
            pests=self._get_pesticide_pests(),
        )


