from django.core.management.base import BaseCommand
from marlin_app.models import UserType

class Command(BaseCommand):
    help = 'Creacion de tipos de usuario'

    def handle(self, *args, **kwargs):
        types = [
            'Dueño',
            'Repartidor',
            'Cliente',
        ]

        types_to_create = []
        
        for utype in types:
            new_type = UserType(name = utype)
            types_to_create.append(new_type)
            
        UserType.objects.bulk_create(types_to_create)


        self.stdout.write(self.style.SUCCESS(f'Se crearon {len(types_to_create)} tipos de usuario.'))