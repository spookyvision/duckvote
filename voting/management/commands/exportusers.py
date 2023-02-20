from django.core.management.base import BaseCommand
from voting.models import User, UserProfile
import csv
import json


class Command(BaseCommand):
    help = 'Export users'

    def add_arguments(self, parser):
        parser.add_argument('file', type=str)

    def handle(self, *args, **options):
        out = [
            ['FirstName', 'Email', 'Id']]
        with open(options['file'], 'w', encoding='utf-8') as fh:
            for profile in UserProfile.objects.all():
                user = profile.user
                out.append([
                    profile.facebook_name.split(' ')[0],
                    user.username,
                    str(user.user_id)
                ])
            json.dump(out, fh, indent=4)
        self.stdout.write(self.style.SUCCESS('all done.'))
