from django.core.management.base import BaseCommand
from authentication.models import User


class Command(BaseCommand):
    help = 'Create default super user'

    def handle(self, *args, **options):
        if not User.objects.filter(email="admin").exists():
            User.objects.create_superuser("admin", "admin@admin.com", "admin")
