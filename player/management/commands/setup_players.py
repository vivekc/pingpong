import os

from django.core.management import BaseCommand

from pingpong.settings import BASE_DIR
from player.models import Player


class Command(BaseCommand):
    CONF_FILE_PATH = os.path.join(os.path.join(BASE_DIR, 'player', 'player_config.ini'))

    def handle(self, *args, **options):
        help = 'Setup players from configuration File'

        with open(self.CONF_FILE_PATH) as config_file:
            _ = config_file.readline()  # skip header
            for line in config_file:
                config_row = line.strip("\n").split(" ")
                player_id = int(config_row[0].strip())
                player_name = config_row[1].strip()
                set_size = int(config_row[2].strip())

                # UPSERT if player id exists, update else create

                try:
                    player = Player.objects.get(player_id=player_id)
                    player.name = player_name
                    player.defense_size = set_size
                    player.save()
                    player.set_defence()
                except Player.DoesNotExist:
                    player = Player.objects.create(player_id=player_id, name=player_name, defense_size=set_size)
                    player.set_defence()