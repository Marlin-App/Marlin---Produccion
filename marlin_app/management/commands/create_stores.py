from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Creacion de tiendas aleatorias'

    def handle(self, *args, **kwargs):
        
        self.stdout.write('Comando Ejecutado exitosamente')