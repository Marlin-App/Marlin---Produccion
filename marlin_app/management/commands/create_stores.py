from datetime import time
import os
from django.core.management.base import BaseCommand
from marlin_app.models import StoreType, Store
import random
from django.contrib.auth.models import User
from django.conf import settings
from cloudinary.uploader import upload


class Command(BaseCommand):
    help = 'Creacion de tiendas'

    def handle(self, *args, **kwargs):
        types = StoreType.objects.all()
        stores = []
        user = User.objects.get(id=1)
        images_dir = os.path.join(settings.MEDIA_ROOT, 'tiendas')
        image_files = os.listdir(images_dir)
        opening_time = time(hour=7, minute=0)
        clossing_time = time(hour=17, minute=0)
        for stype in types:
            for i in range(0,2):
                with open(os.path.join(images_dir, image_files[random.randint(0, len(image_files)-1)]), 'rb') as image_file, \
                 open(os.path.join(images_dir, image_files[random.randint(0, len(image_files)-1)]), 'rb') as image_banner:
                    
                    image_uploaded = upload(image_file, folder="stores", public_id=f"{stype.name}_{i}_image", format="webp")
                    image_banner_uploaded = upload(image_banner, folder="stores", public_id=f"{stype.name}_{i}_selected_image", format="webp")

                    store = (
                    Store(
                        user_id = user,
                        name=f'Tienda {i+1} del tipo {stype.name}',
                        description=f'descripcion de la tienda {i+1} del tipo {stype.name}',
                        coodernates = '9.972207, -84.732302',
                        canton = 'Puntarenas',
                        opening_hour = opening_time,
                        closing_hour = clossing_time,
                        district = 'Puntarenas',
                        picture=image_uploaded['secure_url'],
                        banner=image_banner_uploaded['secure_url']))
                    store.save()
                    store.store_type.set([stype])
                    stores.append(store)


                


        self.stdout.write(self.style.SUCCESS(f'Se crearon {len(stores)} tiendas.'))