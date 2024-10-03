from django.core.management.base import BaseCommand
from marlin_app.models import ItemTag

class Command(BaseCommand):
    help = 'Creacion de tipos de tienda'

    def handle(self, *args, **kwargs):
        tags = [
            'Camisa',
            'Tennis',
            'Gorra',
            'Pantalón',
            'Vestido',
            'Chaqueta',
            'Reloj',
            'Bolso',
            'Zapatos',
            'Accesorios'
        ]

        tags_to_create = []
        
        for tag in tags:
            new_tag = ItemTag(name = tag)
            tags_to_create.append(new_tag)
            
        ItemTag.objects.bulk_create(tags_to_create)


        self.stdout.write(self.style.SUCCESS(f'Se crearon {len(tags_to_create)} tags de productos.'))