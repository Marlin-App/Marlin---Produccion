from django.core.management.base import BaseCommand
from marlin_app.models import Atribute

class Command(BaseCommand):
    help = 'Creacion de tipos de tienda'

    def handle(self, *args, **kwargs):
        attributes = [
            'color',
            'size'
        ]

        attributes_to_create = []
        
        for attribute in attributes:
            new_attribute = Atribute(name = attribute)
            attributes_to_create.append(new_attribute)
            
        Atribute.objects.bulk_create(attributes_to_create)


        self.stdout.write(self.style.SUCCESS(f'Se crearon {len(attributes_to_create)} tags de productos.'))