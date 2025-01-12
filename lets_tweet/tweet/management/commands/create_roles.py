from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group

class Command(BaseCommand):
    help = 'Create default roles'

    def handle(self, *args, **kwargs):
        roles = ['Admin', 'Manager', 'Employee']
        for role in roles:
            group, created = Group.objects.get_or_create(name=role)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Role "{role}" created.'))
            else:
                self.stdout.write(self.style.WARNING(f'Role "{role}" already exists.'))
        self.stdout.write(self.style.SUCCESS('Roles setup complete!'))
