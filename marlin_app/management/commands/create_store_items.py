import os
import random
from django.core.management.base import BaseCommand
from marlin_app.models import Atribute, AtributeValue, Store, StoreItem, ItemTag
from django.conf import settings
from cloudinary.uploader import upload

class Command(BaseCommand):
    help = 'Creacion de tiendas'

    def handle(self, *args, **kwargs):
        stores = Store.objects.all()
        tags = ItemTag.objects.all()
        images_dir = os.path.join(settings.MEDIA_ROOT, 'productos')
        image_files = os.listdir(images_dir)

        # Listas de colores y tamaños
        colors = ['red', 'blue', 'green', 'yellow', 'black', 'white', 'orange', 'purple']
        sizes = ['s', 'm', 'l', 'xl', 'xxl']

        for store in stores:
            for i in range(0, 5):
                # Seleccionar una imagen aleatoria
                with open(os.path.join(images_dir, image_files[random.randint(0, len(image_files) - 1)]), 'rb') as image_file:
                    image_uploaded = upload(image_file, folder="items", public_id=f"{store.name}_{i}_image", format="webp")

                    # Crear un nuevo StoreItem con atributos aleatorios
                    store_item = StoreItem(
                        name=f'Item{i + 1} de {store.name}',
                        description=f'Descripcion de item {i + 1} de {store.name}',
                        price=random.randint(1000, 30000),
                        stock=random.randint(1, 100),
                        picture=image_uploaded['url'],
                        store_id=store,
                        item_type=random.choice(tags),
                    )

                    # Guardar la instancia del StoreItem
                    store_item.save()

                    # Crear atributos
                    atributes = {"color": random.choice(colors), "size": random.choice(sizes)}

                    for attr_name, attr_value in atributes.items():
                        attribute, created = Atribute.objects.get_or_create(name=attr_name)

                        AtributeValue.objects.create(
                            attribute=attribute,
                            storeItem=store_item,  # Aquí usamos store_item directamente
                            value=attr_value
                        )

        self.stdout.write(self.style.SUCCESS(f'Se crearon items.'))