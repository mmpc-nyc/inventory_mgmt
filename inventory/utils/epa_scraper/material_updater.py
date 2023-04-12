import requests
import os

from django.core.files import File
from django.utils.text import slugify
from selenium.common import NoSuchElementException

from core import settings
from inventory.utils.epa_scraper import SeleniumScraper
import inflect
from inventory.models.material import Material, MaterialCategory
from common.models.target import Target
from common.models.unit import Unit
from inventory.models.brand import Brand
import json
import csv

MATERIAL_PATH = settings.BASE_DIR / 'media' / 'materials' / 'documentation'


class MaterialUpdater:
    def __init__(self):
        self.PESTICIDE_CATEGORY = MaterialCategory.objects.get(name='Pesticide')
        self.UNSET_UNIT = Unit.objects.get(name='Unspecified')
        self.UNSPECIFIED_BRAND = Brand.objects.get(name='Unspecified')
        self.scraper = SeleniumScraper()
        self.p = inflect.engine()

    def download_documentation_to_temporary_location(self, download_url) -> str:
        response = requests.get(download_url)
        filepath = MATERIAL_PATH / 'temp_file.pdf'
        with open(filepath, 'wb') as f:
            f.write(response.content)
        return filepath

    def attach_material_documentation(self, material, documentation_url):
        temporary_pdf_filepath = self.download_documentation_to_temporary_location(documentation_url)
        with open(temporary_pdf_filepath, 'rb') as f:
            material.documentation.save(f'{slugify(material.name)}.pdf', File(f))
            material.save()
        os.remove(temporary_pdf_filepath)
        return material

    def create_or_update_pesticide(self, epa_registration_number: str, name: str) -> Material:
        pesticide = self.scraper.parse_pesticide(epa_registration_number)
        pests = {self.p.singular_noun(pest).title() if self.p.singular_noun(pest) else pest.title() for pest in
                 pesticide.pests}
        sites = [site.title() for site in pesticide.sites]
        category_field_values = {
            'epa_registration_number': pesticide.registration_number,
            'pests': ', '.join(pests),
            'sites': ', '.join(sites),
            'restricted_use': bool(pesticide.restricted_use),
            'active_ingredients': json.dumps(pesticide.active_ingredients)

        }
        material, missing = Material.objects.get_or_create(
            name=name.title(),
            defaults={
                'description': pesticide.label.capitalize(),
                'brand': self.UNSPECIFIED_BRAND,
                'category': self.PESTICIDE_CATEGORY,
                'retail_unit': self.UNSET_UNIT,
                'usage_unit': self.UNSET_UNIT,
            }
        )
        if missing:
            for field in self.PESTICIDE_CATEGORY.fields.all():
                material.materialfield_set.get_or_create(
                    field=field,
                    defaults={'value': category_field_values[field.name]}
                )
            for pest in pests:
                target, created = Target.objects.get_or_create(name=pest, defaults={'description': pest})
                material.targets.add(target)
            print(f'Added {material.name}')
        else:
            print(f'Passed {material.name}')
        material = self.attach_material_documentation(material, pesticide.documentation_url)
        return material

    def get_or_update_materials_and_targets_from_list(self, epa_registration_numbers: list[list[str, str]]):
        failed_chemicals = []
        successful_chemicals = []
        for epa_registration_number, name in epa_registration_numbers:
            try:
                successful_chemicals.append(self.create_or_update_pesticide(epa_registration_number, name))
            except NoSuchElementException:
                failed_chemicals.append((epa_registration_number, name))
        self.scraper.driver.close()
        return successful_chemicals, failed_chemicals

    def get_or_update_pesticides_and_targets_from_filepath(self, filepath: str):
        failed_chemicals = []
        successful_chemicals = []
        with open(filepath, 'r') as f:
            for epa_registration_number, name in csv.reader(f):
                try:
                    successful_chemicals.append(self.create_or_update_pesticide(epa_registration_number, name))
                except NoSuchElementException:
                    failed_chemicals.append((epa_registration_number, name))
        self.scraper.driver.close()
        return successful_chemicals, failed_chemicals

    def close(self):
        self.scraper.driver.close()