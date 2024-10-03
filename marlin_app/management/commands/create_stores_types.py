from django.core.management.base import BaseCommand
from marlin_app.models import ItemTag

class Command(BaseCommand):
    help = 'Creacion de tipos de tienda'

    def handle(self, *args, **kwargs):
        types = [
            'Zapateria',
            'Ferreteria',
            'Mascotas',
            'Ropa',
            'Surf',
            'Pesca',
            'Deporte',
            'Bisuteria',
            'Pasamaneria',
            'Floristeria'
        ]
        types_to_create = []
        
        for stype in types:
            new_type = ItemTag(name = stype)
            types_to_create.append(new_type)
            
        ItemTag.objects.bulk_create(types_to_create)


        self.stdout.write(self.style.SUCCESS(f'Se crearon {len(types_to_create)} tipos de tienda.'))