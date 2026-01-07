from django.core.management.base import BaseCommand
from travelProject.models import Currency
from travelProject.services import fetch_currency_rates

class Command(BaseCommand):
    help = 'Updates currency rates from external API'

    def handle(self, *args, **options):
        self.stdout.write('Fetching currency rates...')
        
        rates = fetch_currency_rates()
        if not rates:
            self.stdout.write(self.style.ERROR('Failed to fetch rates'))
            return

        count = 0
        for code, rate in rates.items():
            obj, created = Currency.objects.update_or_create(
                code=code,
                defaults={
                    'name': code,
                    'rate_to_rub': rate
                }
            )
            count += 1
            
        self.stdout.write(self.style.SUCCESS(f'Successfully updated {count} currencies'))
