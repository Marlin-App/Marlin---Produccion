import os
from django.core.management.base import BaseCommand
from marlin_app.models import ItemTag, Store
import random
from django.contrib.auth.models import User
from django.conf import settings

class Command(BaseCommand):
    help = 'Creacion de tiendas'

    def handle(self, *args, **kwargs):
        
        types = ItemTag.objects.all()
        stores = []
        user = User.objects.get(id=1)
        images_dir = os.path.join(settings.MEDIA_ROOT, 'tiendas')
        image_files = os.listdir(images_dir)
        for stype in types:
            for i in range(0,2):
                store = (
                    Store(
                        name=f'Tienda {i+1} del tipo {stype.name}',
                        description=f'descripcion de la tienda {i+1} del tipo {stype.name}',
                        location = 'Puntarenas',
                        user_id = user,
                        picture=f'tiendas/{image_files[random.randint(0, len(image_files)-1)]}'))
                store.save()
                store.store_type.set([stype])
                stores.append(store)
        self.stdout.write(self.style.SUCCESS(f'Se crearon {len(stores)} tiendas.'))