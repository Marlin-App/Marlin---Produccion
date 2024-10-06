import os
from django.core.management.base import BaseCommand
from marlin_app.models import Store, StoreItem, ItemTag
import random
from django.contrib.auth.models import User
from django.conf import settings
from cloudinary.uploader import upload


class Command(BaseCommand):
    help = 'Creacion de tiendas'

    def handle(self, *args, **kwargs):
        stores = Store.objects.all()
        tags = ItemTag.objects.all()
        items = []
        images_dir = os.path.join(settings.MEDIA_ROOT, 'productos')
        image_files = os.listdir(images_dir)
        for store in stores:
            for i in range(0,5):
                with open(os.path.join(images_dir, image_files[random.randint(0, len(image_files)-1)]), 'rb') as image_file:
                    image_uploaded = upload(image_file, folder="items", public_id=f"{store.name}_{i}_image", format="webp")
                    url1 = image_uploaded.get('secure_url', image_uploaded.get('url', ''))
                    extracted_url1 = url1.split('image', 1)[1]
                    final_url1 = 'image' + extracted_url1


                    items.append(StoreItem(name=f'Item{i+1} de {store.name}',
                                    description = f'Descripcion de item {i+1} de {store.name}',
                                     price = random.randint(1000, 30000),
                                     stock = random.randint(1, 100),
                                     picture=final_url1,
                                     store_id = store,
                                     item_type = random.choice(tags)))
        
        StoreItem.objects.bulk_create(items)


        self.stdout.write(self.style.SUCCESS(f'Se crearon {len(items)} items.'))