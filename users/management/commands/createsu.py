from django.core.management import BaseCommand
from users.models import models as user_models

class Command(BaseCommand):
    help = 'This command creates superuser'
    username = 'hj'
    email = 'hajeong@gmail.com'
    password = '1234'

    def handle(self, *args, **options):
        try:
            user_models.User.objects.get(username=self.username)
            self.stdout.write(self.style.SUCCESS(f"Superuser Exists"))

        except user_models.User.DoesNotExist:
            user_models.User.objects.create_superuser(
                username=self.username,
                email=self.email,
                password=self.password,
            )

            self.stdout.write(self.style.SUCCESS(f"Superuser Created"))
        except Exception as error:
            self.stdout.write(
                self.style.ERROR(f"Unknown Error caused: {error}")
            )