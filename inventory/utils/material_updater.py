from inventory.utils.epa_scraper import SeleniumScraper
import inflect
from inventory.models.material import Material, MaterialCategory
from common.models.target import Target
from common.models.unit import Unit
from inventory.models.brand import Brand
import json


# TODO Make this a better function
def get_or_update_materials_and_targets(epa_registration_numbers: list[str]):
    p = inflect.engine()
    scraper = SeleniumScraper()
    pesticide_category = MaterialCategory.objects.get(name='Pesticide')
    unset_unit = Unit.objects.get(name='Unset')
    unspecified_brand = Brand.objects.get(name='Unspecified')
    failed_chemicals = []
    for epa_registration_number in epa_registration_numbers:
        try:
            pesticide = scraper.parse_pesticide(epa_registration_number)
        except:
            failed_chemicals.append(epa_registration_number)
        else:
            pests = {p.singular_noun(pest).title() if p.singular_noun(pest) else pest.title() for pest in
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
                name=pesticide.label.title(),
                defaults={
                    'description': pesticide.label.capitalize(),
                    'brand': unspecified_brand,
                    'category': pesticide_category,
                    'retail_unit': unset_unit,
                    'usage_unit': unset_unit
                }
            )
            if missing:
                for field in pesticide_category.fields.all():
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
    scraper.driver.close()
