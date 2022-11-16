from django.core.management.base import BaseCommand, CommandError
from voting.models import User
import csv
import json


class Command(BaseCommand):
    help = 'Import users'

    def add_arguments(self, parser):
        parser.add_argument('file', type=str)

    def handle(self, *args, **options):
        out = [
            ['FirstName', 'Email', 'Id']]
        with open(options['file']) as fh:
            reader = csv.reader(fh)
            next(reader, None)
            for entry in reader:
                facebook_name = entry[1]
                email = entry[2]
                is_active = entry[6] == "ACTIVE"
                if not is_active:
                    continue
                try:
                    user = User.objects.create_user(email)
                    out.append([
                        facebook_name.split(' ')[0],
                        email,
                        str(user.user_id)
                    ])
                    self.stdout.write(self.style.SUCCESS(f'{email}'))
                except:
                    self.stdout.write(self.style.WARNING(f'could not {email}'))
        with open('users.json', 'w', encoding='utf-8') as fh:
            json.dump(out, fh)
        self.stdout.write(self.style.SUCCESS('all done.'))
